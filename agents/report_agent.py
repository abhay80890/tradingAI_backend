"""
Agent 8 — Report Generation Agent (Pydantic)
Goal: Synthesize all gathered data into a final, readable Markdown report.
"""
from agents.state import AgentState
from agents.llm import get_llm
from agents.schemas import FinalReportSchema

REPORT_PROMPT = """You are an elite Wall Street Equity Analyst.

Your job is to write a highly professional, cohesive Markdown investment report for {symbol} based strictly on the structured data provided below. Do not invent new data.

DATA COMPILED:
- Market Data: {market_data}
- Financials: {financial_metrics}
- Technicals: {technical_signals}
- News Sentiment: {news_sentiment}
- Document Evidence: {rag_evidence}
- Risk Profile: {risk_score}
- Portfolio Strategy: {portfolio_plan}

INSTRUCTIONS:
1. Write a professional Markdown document.
2. Include sections like "Executive Summary", "Financial Health", "Technical & Market Sentiment", "Risk Analysis", and "Final Recommendation".
3. Use bullet points and bold text for readability.
4. Output the complete markdown string into the `markdown_report` field of the required JSON schema.
"""

def report_generation_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "Report Generation Agent"
    try:
        llm = get_llm()
        
        prompt = REPORT_PROMPT.format(
            symbol=symbol,
            market_data=state.get("market_data", "No data"),
            financial_metrics=state.get("financial_metrics", "No data"),
            technical_signals=state.get("technical_signals", "No data"),
            news_sentiment=state.get("news_sentiment", "No data"),
            rag_evidence=state.get("rag_evidence", "No data"),
            risk_score=state.get("risk_score", "No data"),
            portfolio_plan=state.get("portfolio_plan", "No data")
        )
        
        structured_llm = llm.with_structured_output(FinalReportSchema)
        parsed = structured_llm.invoke(prompt)
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "Report Generation", "error": data["error"]})
        else:
            state["final_report"] = data.get("markdown_report", "Report generation failed.")
            
    except Exception as e:
        state["errors"].append({"agent": "Report Generation", "error": f"Agent failed: {str(e)}"})
        
    return state
