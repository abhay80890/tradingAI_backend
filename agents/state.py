from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    """
    The shared memory state for all AI agents in FinPilot.
    Agents read from this dictionary and write their results back to it.
    """
    job_id: str
    symbol: str            # The stock ticker (e.g., "AAPL")
    user_prompt: str       # Custom instructions from the user (e.g., "Focus on AI")
    
    # Agent Outputs
    market_data: Optional[Dict[str, Any]]
    financial_metrics: Optional[Dict[str, Any]]
    technical_signals: Optional[Dict[str, Any]]
    news_sentiment: Optional[Dict[str, Any]]
    rag_evidence: Optional[List[Any]]
    risk_score: Optional[Dict[str, Any]]
    portfolio_plan: Optional[Dict[str, Any]]
    final_report: Optional[str]
    
    # Tracking & Error Handling
    errors: List[Dict[str, str]]  # List of dicts e.g. [{"agent": "Market", "error": "API down"}]
    current_step: str             # Name of the currently running agent
