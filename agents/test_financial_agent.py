import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.state import AgentState
from agents.financial_agent import financial_analysis_agent
from dotenv import load_dotenv

def main():
    # Load env vars to get Alpha Vantage Key
    load_dotenv(dotenv_path="../.env")
    
    if len(sys.argv) < 2:
        print("Usage: python test_financial_agent.py <SYMBOL>")
        print("Example: python test_financial_agent.py AAPL")
        sys.exit(1)
        
    symbol = sys.argv[1].upper()
    print(f"🚀 Running Financial Analysis Agent for {symbol}...\n")
    
    # 1. Initialize an empty shared state
    initial_state: AgentState = {
        "job_id": "test-job-002",
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
    
    # 2. Run the agent (pass state in, get updated state out)
    new_state = financial_analysis_agent(initial_state)
    
    # 3. Print the results
    print("--- 📊 AGENT RESULTS ---")
    
    if new_state["errors"]:
        print("\n⚠️ ERRORS ENCOUNTERED:")
        for err in new_state["errors"]:
            print(f"  - [{err['agent']}]: {err['error']}")
            
    if new_state["financial_metrics"]:
        print("\n✅ FINANCIAL METRICS CALCULATED:")
        metrics = new_state["financial_metrics"]
        print(f"  Symbol: {metrics['symbol']}")
        print(f"  Fiscal Year End: {metrics['fiscal_date_ending']}")
        print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")
        print(f"  Net Income: ${metrics['net_income']:,.2f}")
        
        print("\n  --- Ratios ---")
        ratios = metrics["ratios"]
        print(f"  Gross Margin: {ratios['gross_margin'] * 100:.2f}%")
        print(f"  Net Margin: {ratios['net_margin'] * 100:.2f}%")
        print(f"  Return on Equity (ROE): {ratios['roe'] * 100:.2f}%")
        print(f"  Debt to Equity: {ratios['debt_to_equity']:.2f}")
    else:
        print("\n❌ No financial metrics returned.")

if __name__ == "__main__":
    main()
