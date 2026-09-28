import json
from typing import List
from langchain_core.tools import tool
from qdrant_client import QdrantClient
from core.config import settings

@tool
def search_internal_documents(query: str) -> str:
    """
    Searches the internal Qdrant vector database for documents, PDFs, or research 
    notes that have been uploaded by the user and are relevant to the query.
    Use this to find internal company knowledge, uploaded earnings calls, 
    analyst reports, or any custom documents about a stock.
    
    Args:
        query: A natural language search query (e.g., 'AAPL revenue growth risks 2024')
    
    Returns:
        A JSON string containing a list of relevant text excerpts from uploaded documents.
    """
    try:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
            return json.dumps({"excerpts": [], "message": "GEMINI_API_KEY not configured. Cannot perform semantic search."})
            
        # Import here to avoid errors if langchain_google_genai is not installed
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        
        client = QdrantClient(url="http://localhost:6333")
        collections = [c.name for c in client.get_collections().collections]
        
        if "finpilot_docs" not in collections:
            return json.dumps({"excerpts": [], "message": "No documents uploaded yet. The knowledge base is empty."})
            
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GEMINI_API_KEY
        )
        query_vector = embeddings.embed_query(query)
        
        results = client.search(
            collection_name="finpilot_docs",
            query_vector=query_vector,
            limit=3
        )
        
        excerpts = []
        for hit in results:
            if hit.payload and "page_content" in hit.payload:
                excerpts.append(hit.payload["page_content"])
                
        return json.dumps({"excerpts": excerpts, "count": len(excerpts)})
        
    except Exception as e:
        return json.dumps({"excerpts": [], "error": f"RAG search failed: {str(e)}"})
