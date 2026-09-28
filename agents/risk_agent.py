"""
Agent 6 — Risk Analysis Agent (Pydantic)
Goal: Analyze financial, technical, and sentiment data to output a strict risk score.
"""
from agents.state import AgentState
from agents.llm import get_llm
from agents.schemas import RiskScoreSchema

RISK_PROMPT = """You are a highly analytical Risk Analysis Agent.

Your job is to assess the overall investment risk for {symbol} based solely on the provided data.

DATA:
Financial Metrics: {financial_metrics}
Technical Signals: {technical_signals}
News Sentiment: {news_sentiment}

Evaluate the data and output a strictly formatted JSON response.
Determine a risk_score from 1 (Safest) to 10 (Highest Risk) and a corresponding risk_level (Low, Medium, High).
Provide a 2-3 sentence reasoning explaining your score.
If critical data is missing, assess based on what is available, but mention the missing data in your reasoning.
"""

def risk_analysis_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "Risk Analysis Agent"
    try:
        llm = get_llm()
        
        # Prepare the prompt with whatever data is currently in state
        prompt = RISK_PROMPT.format(
            symbol=symbol,
            financial_metrics=state.get("financial_metrics", "No data"),
            technical_signals=state.get("technical_signals", "No data"),
            news_sentiment=state.get("news_sentiment", "No data")
        )
        
        # We don't need tools here, just reasoning and structured output
        structured_llm = llm.with_structured_output(RiskScoreSchema)
        parsed = structured_llm.invoke(prompt)
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "Risk Analysis", "error": data["error"]})
        else:
            state["risk_score"] = data
            
    except Exception as e:
        state["errors"].append({"agent": "Risk Analysis", "error": f"Agent failed: {str(e)}"})
        
    return state
