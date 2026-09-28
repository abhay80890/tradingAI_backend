import httpx
import json
from typing import Dict, Any
from langchain_core.tools import tool
from core.config import settings

BASE_URL = "https://www.alphavantage.co/query"

def _check_rate_limit(data: Dict) -> bool:
    """Returns True if Alpha Vantage returned a rate limit message."""
    return "Information" in data or "Note" in data

@tool
def get_global_quote(symbol: str) -> str:
    """
    Fetches the latest real-time stock price, volume, daily high/low, and percentage
    change for a given stock symbol. Use this to get the current market price.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA')
    
    Returns:
        A JSON string containing the live quote data.
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if _check_rate_limit(data):
            return json.dumps({"error": "API rate limit reached. Max 25 calls/day on free tier."})
        return json.dumps(data.get("Global Quote", {}))

@tool
def get_company_overview(symbol: str) -> str:
    """
    Fetches company fundamental information including company name, industry, 
    description, market cap, P/E ratio, 52-week high and low.
    Use this to understand what the company does and its valuation metrics.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA')
    
    Returns:
        A JSON string containing company overview data.
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if _check_rate_limit(data):
            return json.dumps({"error": "API rate limit reached. Max 25 calls/day on free tier."})
        return json.dumps(data)

@tool
def get_income_statement(symbol: str) -> str:
    """
    Fetches annual income statements for the company including total revenue, 
    gross profit, net income, operating expenses, and EBITDA.
    Use this to analyze profitability and revenue trends.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA')
    
    Returns:
        A JSON string containing annual income statement data.
    """
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if _check_rate_limit(data):
            return json.dumps({"error": "API rate limit reached. Max 25 calls/day on free tier."})
        # Return only the most recent 2 annual reports to save LLM context
        reports = data.get("annualReports", [])[:2]
        return json.dumps({"annualReports": reports})

@tool
def get_balance_sheet(symbol: str) -> str:
    """
    Fetches the company balance sheet including total assets, total liabilities, 
    shareholder equity, short-term and long-term debt. 
    Use this to evaluate financial health and solvency.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA')
    
    Returns:
        A JSON string containing annual balance sheet data.
    """
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if _check_rate_limit(data):
            return json.dumps({"error": "API rate limit reached. Max 25 calls/day on free tier."})
        reports = data.get("annualReports", [])[:2]
        return json.dumps({"annualReports": reports})

@tool
def get_daily_prices(symbol: str) -> str:
    """
    Fetches the last 100 days of daily OHLCV (Open, High, Low, Close, Volume) price 
    data for technical analysis. Use this to get historical price data for 
    calculating moving averages, RSI, and MACD.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA')
    
    Returns:
        A JSON string containing daily time series price data.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if _check_rate_limit(data):
            return json.dumps({"error": "API rate limit reached. Max 25 calls/day on free tier."})
        return json.dumps(data)

@tool
def get_news_sentiment(symbol: str) -> str:
    """
    Fetches recent news articles about the company along with pre-computed AI 
    sentiment scores for each article. Scores range from -0.35 (very negative/bearish) 
    to +0.35 (very positive/bullish).
    Use this to understand current market sentiment and news coverage.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA')
    
    Returns:
        A JSON string containing news articles and their sentiment scores.
    """
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "limit": 5,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if _check_rate_limit(data):
            return json.dumps({"error": "API rate limit reached. Max 25 calls/day on free tier."})
        return json.dumps(data)
