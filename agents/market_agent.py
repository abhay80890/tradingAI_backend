"""
Agent 1 — Market Research Agent (Pydantic + ReAct)
"""
from agents.state import AgentState
from agents.llm import get_llm, run_react_agent
from agents.tools.alpha_vantage import get_global_quote, get_company_overview
from agents.schemas import MarketDataSchema

MARKET_TOOLS = [get_global_quote, get_company_overview]

MARKET_PROMPT = """You are a Market Research Agent.

Goal: Gather live market data for stock symbol: {symbol}

1. Call get_global_quote(symbol='{symbol}')
2. Call get_company_overview(symbol='{symbol}')
3. Analyze the results.
"""

def market_research_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "Market Research Agent"
    try:
        llm = get_llm()
        raw_answer = run_react_agent(llm, MARKET_TOOLS, MARKET_PROMPT.format(symbol=symbol))
        
        # Enforce strict Pydantic structure
        structured_llm = llm.with_structured_output(MarketDataSchema)
        parsed = structured_llm.invoke(f"Extract market data for {symbol} from this raw output. If it mentions an API rate limit or error, put that in the 'error' field and fill numeric fields with 0.0. Raw output: {raw_answer}")
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "Market Research", "error": data["error"]})
        else:
            state["market_data"] = data
            
    except Exception as e:
        state["errors"].append({"agent": "Market Research", "error": f"Agent failed: {str(e)}"})
    return state
