"""
Agent 7 — Portfolio Planning Agent (Pydantic)
Goal: Recommend an investment action and allocation size based on all previous data.
"""
from agents.state import AgentState
from agents.llm import get_llm
from agents.schemas import PortfolioPlanSchema

PORTFOLIO_PROMPT = """You are an expert Portfolio Manager and Financial Advisor.

Your job is to determine the optimal investment strategy for {symbol} based on the accumulated research.

DATA:
Risk Score: {risk_score}
Financial Metrics: {financial_metrics}
Technical Signals: {technical_signals}
News Sentiment: {news_sentiment}

Evaluate the profile. Is this a Buy, Hold, or Sell? 
How confident are you (1-100)?
What percentage of a standard portfolio should be allocated to this stock (e.g., '0%', '1-3%', '5-10%')?
Provide a brief reasoning.

Output MUST strictly adhere to the required JSON schema.
"""

def portfolio_planning_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "Portfolio Planning Agent"
    try:
        llm = get_llm()
        
        prompt = PORTFOLIO_PROMPT.format(
            symbol=symbol,
            risk_score=state.get("risk_score", "No data"),
            financial_metrics=state.get("financial_metrics", "No data"),
            technical_signals=state.get("technical_signals", "No data"),
            news_sentiment=state.get("news_sentiment", "No data")
        )
        
        structured_llm = llm.with_structured_output(PortfolioPlanSchema)
        parsed = structured_llm.invoke(prompt)
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "Portfolio Planning", "error": data["error"]})
        else:
            state["portfolio_plan"] = data
            
    except Exception as e:
        state["errors"].append({"agent": "Portfolio Planning", "error": f"Agent failed: {str(e)}"})
        
    return state
