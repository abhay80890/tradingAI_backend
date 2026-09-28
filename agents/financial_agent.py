"""
Agent 2 — Financial Analysis Agent (Pydantic + ReAct)
"""
from agents.state import AgentState
from agents.llm import get_llm, run_react_agent
from agents.tools.alpha_vantage import get_income_statement, get_balance_sheet
from agents.schemas import FinancialMetricsSchema

FINANCIAL_TOOLS = [get_income_statement, get_balance_sheet]

FINANCIAL_PROMPT = """You are a Financial Analysis Agent.

Goal: Analyze financial statements for: {symbol}

1. Call get_income_statement(symbol='{symbol}')
2. Call get_balance_sheet(symbol='{symbol}')
3. Analyze the most recent annual report and calculate gross margin, net margin, roe, and debt-to-equity using exact math.
"""

def financial_analysis_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "Financial Analysis Agent"
    try:
        llm = get_llm()
        raw_answer = run_react_agent(llm, FINANCIAL_TOOLS, FINANCIAL_PROMPT.format(symbol=symbol))
        
        structured_llm = llm.with_structured_output(FinancialMetricsSchema)
        parsed = structured_llm.invoke(f"Extract financial metrics for {symbol} from this raw output. If there is an error or rate limit, put it in the 'error' field and set numbers to 0.0. Raw output: {raw_answer}")
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "Financial Analysis", "error": data["error"]})
        else:
            state["financial_metrics"] = data
            
    except Exception as e:
        state["errors"].append({"agent": "Financial Analysis", "error": f"Agent failed: {str(e)}"})
    return state
