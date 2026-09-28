"""
Agent 3 — Technical Analysis Agent (Pydantic + ReAct)
"""
from agents.state import AgentState
from agents.llm import get_llm, run_react_agent
from agents.tools.alpha_vantage import get_daily_prices
from agents.tools.technical_calc import calculate_technical_indicators
from agents.schemas import TechnicalSignalsSchema

TECHNICAL_TOOLS = [get_daily_prices, calculate_technical_indicators]

TECHNICAL_PROMPT = """You are a Technical Analysis Agent.

Goal: Get chart-based trading signals for: {symbol}

1. Call get_daily_prices(symbol='{symbol}')
2. Pass the JSON result into calculate_technical_indicators(daily_prices_json=...)
3. Review the returned RSI, SMA, and MACD indicators.
"""

def technical_analysis_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "Technical Analysis Agent"
    try:
        llm = get_llm()
        raw_answer = run_react_agent(llm, TECHNICAL_TOOLS, TECHNICAL_PROMPT.format(symbol=symbol))
        
        structured_llm = llm.with_structured_output(TechnicalSignalsSchema)
        parsed = structured_llm.invoke(f"Extract technical indicators for {symbol}. If there is an error or rate limit, populate the 'error' field and set numbers to 0.0. Raw output: {raw_answer}")
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "Technical Analysis", "error": data["error"]})
        else:
            state["technical_signals"] = data
            
    except Exception as e:
        state["errors"].append({"agent": "Technical Analysis", "error": f"Agent failed: {str(e)}"})
    return state
