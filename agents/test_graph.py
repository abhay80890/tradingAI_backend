import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.state import AgentState
from agents.graph import research_graph
from dotenv import load_dotenv

def main():
    # Load env vars to get API keys
    load_dotenv(dotenv_path="../.env")
    
    if len(sys.argv) < 2:
        print("Usage: python test_graph.py <SYMBOL>")
        print("Example: python test_graph.py MSFT")
        sys.exit(1)
        
    symbol = sys.argv[1].upper()
    print(f"🚀 Starting LangGraph AI Workflow for {symbol}...\n")
    
    # 1. Initialize empty state
    initial_state: AgentState = {
        "job_id": "test-graph-001",
        "symbol": symbol,
        "user_prompt": "",
        "market_data": None,
        "financial_metrics": None,
        "technical_signals": None,
        "news_sentiment": None,
        "rag_evidence": None,
        "risk_score": None,
        "portfolio_plan": None,
        "final_report": None,
        "errors": [],
        "current_step": "init"
    }
    
    # 2. Execute the workflow! (This automatically runs all agents in order)
    print("⏳ Running agents...\n")
    final_state = research_graph.invoke(initial_state)
    
    # 3. Print the combined results
    print("--- 🏁 WORKFLOW COMPLETE ---\n")
    
    if final_state.get("errors"):
        print("⚠️ ERRORS ENCOUNTERED:")
        for err in final_state["errors"]:
            print(f"  - [{err['agent']}]: {err['error']}")
        print("")
            
    print("✅ MARKET DATA EXTRACTED (Agent 1):")
    if final_state.get("market_data"):
        print(f"  Company: {final_state['market_data'].get('company_name')}")
        print(f"  Price: ${final_state['market_data'].get('current_price')}")
    else:
        print("  None")
        
    print("\n✅ FINANCIAL METRICS CALCULATED (Agent 2):")
    if final_state.get("financial_metrics"):
        ratios = final_state['financial_metrics'].get('ratios', {})
        print(f"  Gross Margin: {ratios.get('gross_margin', 0) * 100:.2f}%")
        print(f"  ROE: {ratios.get('roe', 0) * 100:.2f}%")
    else:
        print("  None")
        
    print("\n✅ TECHNICAL SIGNALS EXTRACTED (Agent 3):")
    if final_state.get("technical_signals"):
        tech = final_state["technical_signals"]
        print(f"  RSI (14): {tech.get('rsi_14', 0):.2f} ({tech.get('rsi_signal')})")
        print(f"  SMA 20 vs 50: {tech.get('sma_20', 0):.2f} / {tech.get('sma_50', 0):.2f} ({tech.get('trend_signal')})")
        print(f"  MACD Crossover: {tech.get('macd_crossover')}")
    else:
        print("  None")
        
    print("\n✅ NEWS SENTIMENT EXTRACTED (Agent 4):")
    if final_state.get("news_sentiment"):
        news = final_state["news_sentiment"]
        print(f"  Overall Mood: {news.get('sentiment_label')} (Score: {news.get('average_score'):.2f})")
        print(f"  Articles Analyzed: {news.get('article_count')}")
        if news.get('top_articles'):
            print(f"  Top Headline: {news['top_articles'][0]['title']}")
    else:
        print("  None")
        
    print(f"\n✅ RAG DOCUMENT EVIDENCE (Agent 5):")
    if final_state.get("rag_evidence"):
        for evidence in final_state["rag_evidence"]:
            print(f"  - {evidence}")
    else:
        print("  No internal documents found for this query.")
        
    print(f"\n✅ RISK ANALYSIS (Agent 6):")
    if final_state.get("risk_score"):
        risk = final_state["risk_score"]
        print(f"  Score: {risk.get('risk_score')}/10 ({risk.get('risk_level')})")
        print(f"  Reasoning: {risk.get('reasoning')}")
    else:
        print("  None")

    print(f"\n✅ PORTFOLIO PLAN (Agent 7):")
    if final_state.get("portfolio_plan"):
        plan = final_state["portfolio_plan"]
        print(f"  Action: {plan.get('action')} (Confidence: {plan.get('confidence_score')}%)")
        print(f"  Allocation: {plan.get('recommended_allocation')}")
        print(f"  Reasoning: {plan.get('reasoning')}")
    else:
        print("  None")

    print(f"\n✅ FINAL REPORT (Agent 8):")
    if final_state.get("final_report"):
        print("  [Generated successfully! Check backend/latest_report.md or see below:]")
        print(f"\n---\n{final_state['final_report']}\n---")
        with open("latest_report.md", "w", encoding="utf-8") as f:
            f.write(final_state["final_report"])
    else:
        print("  None")

if __name__ == "__main__":
    main()
