import json
import math
import pandas as pd
import ta
from typing import Dict, Any
from langchain_core.tools import tool

@tool
def calculate_technical_indicators(daily_prices_json: str) -> str:
    """
    Takes raw Alpha Vantage TIME_SERIES_DAILY JSON data and calculates technical 
    analysis indicators: RSI (14-day), SMA (20 & 50-day), and MACD. 
    Always call get_daily_prices first, then pass the result directly to this tool.
    
    Args:
        daily_prices_json: The raw JSON string returned by get_daily_prices tool.
    
    Returns:
        A JSON string with RSI, SMA, MACD values and signal labels.
    """
    try:
        data = json.loads(daily_prices_json)
        
        if "error" in data:
            return json.dumps({"error": data["error"]})
            
        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            return json.dumps({"error": "No time series data found in the provided JSON."})
            
        # Build DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df = df.rename(columns={
            "1. open": "open", "2. high": "high",
            "3. low": "low", "4. close": "close", "5. volume": "volume"
        })
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index(ascending=True)
        
        if df.empty or len(df) < 30:
            return json.dumps({"error": "Not enough data points (need at least 30 days)."})
            
        close = df["close"]
        
        # Calculate indicators
        rsi_series = ta.momentum.rsi(close, window=14)
        sma_20 = ta.trend.sma_indicator(close, window=20).iloc[-1]
        sma_50 = ta.trend.sma_indicator(close, window=50).iloc[-1]
        macd = ta.trend.macd(close).iloc[-1]
        macd_sig = ta.trend.macd_signal(close).iloc[-1]
        rsi_val = rsi_series.iloc[-1]
        latest_close = close.iloc[-1]
        
        def clean(v):
            return 0.0 if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v)
        
        rsi_val = clean(rsi_val)
        rsi_signal = "Neutral"
        if rsi_val > 70:
            rsi_signal = "Overbought"
        elif rsi_val < 30:
            rsi_signal = "Oversold"
            
        result = {
            "rsi_14": rsi_val,
            "rsi_signal": rsi_signal,
            "sma_20": clean(sma_20),
            "sma_50": clean(sma_50),
            "trend_signal": "Bullish" if latest_close > clean(sma_20) else "Bearish",
            "macd": clean(macd),
            "macd_signal_line": clean(macd_sig),
            "macd_crossover": "Bullish" if clean(macd) > clean(macd_sig) else "Bearish"
        }
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({"error": f"Calculation failed: {str(e)}"})
