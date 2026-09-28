"""
Shared ReAct Agent runner for all FinPilot agents.
Implements the Reason + Act loop using LangChain's bind_tools() — 
compatible with LangGraph v1.2+ and langchain-nvidia-ai-endpoints.
"""
from typing import List, Any
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.tools import BaseTool
from core.config import settings

def get_llm(temperature: float = 0.0) -> ChatNVIDIA:
    """
    Returns a configured NVIDIA LLM instance (Llama 3.1 70B Instruct).
    temperature=0.0 ensures deterministic, factual responses for financial analysis.
    """
    if not settings.NVIDIA_API_KEY:
        raise ValueError(
            "NVIDIA_API_KEY is not configured. "
            "Please set it in your .env file."
        )
    return ChatNVIDIA(
        model="meta/llama-3.3-70b-instruct",
        nvidia_api_key=settings.NVIDIA_API_KEY,
        temperature=temperature,
    )

def run_react_agent(llm: ChatNVIDIA, tools: List[BaseTool], prompt: str, max_steps: int = 8) -> str:
    """
    Runs a full ReAct (Reason + Act) loop for a given prompt and tool set.
    
    The loop:
    1. Sends the prompt to the LLM (with tools bound).
    2. If the LLM wants to call a tool, executes it and feeds the result back.
    3. Repeats until the LLM produces a final text answer (no more tool calls).
    
    Returns the final text content from the LLM.
    """
    # Bind tools to the LLM so it knows what capabilities it has
    llm_with_tools = llm.bind_tools(tools)
    
    # Build a tool name -> callable map for fast lookup
    tool_map = {t.name: t for t in tools}
    
    # Start the conversation with the human prompt
    messages: List[BaseMessage] = [HumanMessage(content=prompt)]
    
    for step in range(max_steps):
        response: AIMessage = llm_with_tools.invoke(messages)
        messages.append(response)
        
        # If no tool calls were made, the LLM is done reasoning
        if not response.tool_calls:
            content = response.content
            if isinstance(content, list):
                content = " ".join([c.get("text", "") for c in content if isinstance(c, dict) and "text" in c])
            return str(content)
        
        # Execute each tool the LLM requested
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id   = tool_call["id"]
            
            if tool_name not in tool_map:
                tool_result = f"Error: Unknown tool '{tool_name}'"
            else:
                try:
                    tool_result = tool_map[tool_name].invoke(tool_args)
                except Exception as e:
                    tool_result = f"Error running {tool_name}: {str(e)}"
            
            # Feed the tool output back into the conversation
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))
    
    # Safety: if we hit max_steps, return whatever the last AI message said
    last_ai = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
    if not last_ai:
        return "Max steps reached without a final answer."
        
    content = last_ai.content
    if isinstance(content, list):
        content = " ".join([c.get("text", "") for c in content if isinstance(c, dict) and "text" in c])
        
    return str(content)
