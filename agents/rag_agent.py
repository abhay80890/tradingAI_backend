"""
Agent 5 — RAG Document Agent (Pydantic + ReAct)
"""
from agents.state import AgentState
from agents.llm import get_llm, run_react_agent
from agents.tools.rag_search import search_internal_documents
from agents.schemas import RAGResultSchema

RAG_TOOLS = [search_internal_documents]

RAG_PROMPT = """You are a Document Research Agent.

Goal: Search internal database for: {symbol}
Context: {user_prompt}

1. Call search_internal_documents(query=...) with a good targeted query.
2. Review any found excerpts.
"""

def rag_document_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    user_prompt = state.get("user_prompt", "General analysis")
    state["current_step"] = "RAG Document Agent"
    try:
        llm = get_llm()
        raw_answer = run_react_agent(llm, RAG_TOOLS, RAG_PROMPT.format(symbol=symbol, user_prompt=user_prompt))
        
        structured_llm = llm.with_structured_output(RAGResultSchema)
        parsed = structured_llm.invoke(f"Extract RAG results for {symbol}. Empty excerpts are fine if none found. Raw output: {raw_answer}")
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "RAG Document", "error": data["error"]})
            state["rag_evidence"] = []
        else:
            # We strictly map excerpts array back to state["rag_evidence"] 
            # to maintain compatibility with the rest of the app.
            state["rag_evidence"] = data.get("excerpts", [])
            
    except Exception as e:
        state["errors"].append({"agent": "RAG Document", "error": f"Agent failed: {str(e)}"})
        state["rag_evidence"] = []
    return state
