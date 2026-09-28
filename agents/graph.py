from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.market_agent import market_research_agent
from agents.financial_agent import financial_analysis_agent
from agents.technical_agent import technical_analysis_agent
from agents.news_agent import news_sentiment_agent
from agents.rag_agent import rag_document_agent
from agents.risk_agent import risk_analysis_agent
from agents.portfolio_agent import portfolio_planning_agent
from agents.report_agent import report_generation_agent

def build_research_graph():
    """
    Builds the LangGraph orchestrator that wires all the agents together.
    """
    # 1. Initialize the graph with our shared memory (AgentState)
    workflow = StateGraph(AgentState)
    
    # 2. Add our agents as nodes
    workflow.add_node("market_research", market_research_agent)
    workflow.add_node("financial_analysis", financial_analysis_agent)
    workflow.add_node("technical_analysis", technical_analysis_agent)
    workflow.add_node("news_sentiment", news_sentiment_agent)
    workflow.add_node("rag_document", rag_document_agent)
    workflow.add_node("risk_analysis", risk_analysis_agent)
    workflow.add_node("portfolio_planning", portfolio_planning_agent)
    workflow.add_node("report_generation", report_generation_agent)
    
    # 3. Define the execution sequence (Edges)
    workflow.set_entry_point("market_research")
    workflow.add_edge("market_research", "financial_analysis")
    workflow.add_edge("financial_analysis", "technical_analysis")
    workflow.add_edge("technical_analysis", "news_sentiment")
    workflow.add_edge("news_sentiment", "rag_document")
    workflow.add_edge("rag_document", "risk_analysis")
    workflow.add_edge("risk_analysis", "portfolio_planning")
    workflow.add_edge("portfolio_planning", "report_generation")
    workflow.add_edge("report_generation", END)
    
    # 4. Compile the graph into an executable workflow
    return workflow.compile()

# Expose a compiled instance to be used by the FastAPI backend
research_graph = build_research_graph()
