import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.state import AgentState
from agents.market_agent import market_research_agent
from dotenv import load_dotenv

def main():
    # Load env vars to get Alpha Vantage Key
    load_dotenv(dotenv_path="../.env")
    
    if len(sys.argv) < 2:
        print("Usage: python test_market_agent.py <SYMBOL>")
        print("Example: python test_market_agent.py AAPL")
        sys.exit(1)
        
    symbol = sys.argv[1].upper()
    print(f"🚀 Running Market Research Agent for {symbol}...\n")
    
    # 1. Initialize an empty shared state
    initial_state: AgentState = {
        "job_id": "test-job-001",
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
    new_state = market_research_agent(initial_state)
    
    # 3. Print the results
    print("--- 📊 AGENT RESULTS ---")
    
    if new_state["errors"]:
        print("\n⚠️ ERRORS ENCOUNTERED:")
        for err in new_state["errors"]:
            print(f"  - [{err['agent']}]: {err['error']}")
            
    if new_state["market_data"]:
        print("\n✅ MARKET DATA FOUND:")
        for key, value in new_state["market_data"].items():
            print(f"  {key}: {value}")
    else:
        print("\n❌ No market data returned.")

if __name__ == "__main__":
    main()
