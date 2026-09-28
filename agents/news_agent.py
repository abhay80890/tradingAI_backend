"""
Agent 4 — News & Sentiment Agent (Pydantic + ReAct)
"""
from agents.state import AgentState
from agents.llm import get_llm, run_react_agent
from agents.tools.alpha_vantage import get_news_sentiment
from agents.schemas import NewsSentimentSchema

NEWS_TOOLS = [get_news_sentiment]

NEWS_PROMPT = """You are a News & Sentiment Analysis Agent.

Goal: Analyze market sentiment for: {symbol}

1. Call get_news_sentiment(symbol='{symbol}')
2. Average the sentiment scores across all returned articles.
3. Label as Bullish (>= 0.15), Bearish (<= -0.15), or Neutral.
"""

def news_sentiment_agent(state: AgentState) -> AgentState:
    symbol = state["symbol"]
    state["current_step"] = "News & Sentiment Agent"
    try:
        llm = get_llm()
        raw_answer = run_react_agent(llm, NEWS_TOOLS, NEWS_PROMPT.format(symbol=symbol))
        
        structured_llm = llm.with_structured_output(NewsSentimentSchema)
        parsed = structured_llm.invoke(f"Extract sentiment analysis for {symbol}. If there is an error, populate 'error'. Raw output: {raw_answer}")
        
        data = parsed.model_dump()
        
        if data.get("error"):
            state["errors"].append({"agent": "News & Sentiment", "error": data["error"]})
        else:
            state["news_sentiment"] = data
            
    except Exception as e:
        state["errors"].append({"agent": "News & Sentiment", "error": f"Agent failed: {str(e)}"})
    return state
