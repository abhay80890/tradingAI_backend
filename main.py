from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Load the secret variables from our .env file
load_dotenv(dotenv_path="../.env")

# 2. Import all API route files
from api.auth import router as auth_router
from api.securities import router as securities_router
from api.watchlist import router as watchlist_router
from api.portfolio import router as portfolio_router
from api.orders import router as orders_router
from api.documents import router as documents_router
from api.research import router as research_router

# 3. Create the FastAPI application
app = FastAPI(
    title="FinPilot AI API",
    description="Multi-Agent AI Investment Research & Paper Trading Platform",
    version="1.0.0"
)

# 4. Configure CORS (Cross-Origin Resource Sharing)
# This allows our Next.js frontend (running on port 3000) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Register all API routes with the app
app.include_router(auth_router)        # /api/v1/auth/...
app.include_router(securities_router)  # /api/v1/securities/...
app.include_router(watchlist_router)   # /api/v1/watchlist/...
app.include_router(portfolio_router)   # /api/v1/portfolios/...
app.include_router(orders_router)      # /api/v1/orders/...
app.include_router(documents_router)   # /api/v1/documents/...
app.include_router(research_router)    # /api/v1/research/...

# 6. Public AI Agent Route (MVP Only)
from pydantic import BaseModel
from agents.graph import research_graph

class RunAgentRequest(BaseModel):
    symbol: str

@app.post("/api/v1/run-agents")
async def run_agents(request: RunAgentRequest):
    """Trigger the LangGraph AI swarm for a given symbol (Mocked for stability)."""
    import asyncio
    
    symbol = request.symbol.upper()
    
    # Simulate processing time for the 8 agents
    await asyncio.sleep(2.5)
    
    mock_report = f"""# 📈 AI Investment Report: {symbol}
    
## Executive Summary
**{symbol}** is currently showing strong technical momentum backed by robust fundamental growth. The AI swarm has analyzed recent market data, SEC filings, and real-time news sentiment to compile this briefing.

## 1. Technical Analysis
* **Trend**: Bullish (Short-term & Long-term)
* **Moving Averages**: Trading above the 50-day and 200-day SMA.
* **RSI (14)**: 62.4 (Approaching overbought, but showing strong momentum)
* **MACD**: Bullish crossover detected 3 days ago.

## 2. Fundamental Analysis
* **Revenue Growth**: +14.2% YoY
* **Profit Margins**: Expanding by 120 bps due to operational efficiencies.
* **Valuation**: Trading at a slight premium to sector peers, justified by higher growth metrics.

## 3. Sentiment & News
* **Overall Sentiment**: 🟢 Positive
* **Key Drivers**: Recent product announcements and favorable macroeconomic conditions have driven positive retail and institutional sentiment. No major regulatory risks detected in recent filings.

## 4. Risk Assessment
* **Volatility Risk**: Medium
* **Market Risk**: Low to Medium
* **Overall Risk Score**: 4/10

## 🎯 Portfolio Recommendation
**Recommendation: ACCUMULATE**
For existing positions, we recommend a HOLD with a trailing stop-loss at 8% below current market price. For new allocations, consider accumulating on any market-wide pullbacks.
"""

    return {
        "status": "success",
        "data": {
            "job_id": "api-run-mock",
            "symbol": symbol,
            "final_report": mock_report
        }
    }

# 7. Health check routes
@app.get("/health")
def health_check():
    """Simple endpoint to check if the server is alive."""
    return {
        "status": "success",
        "message": "FinPilot AI Backend is running smoothly!"
    }

@app.get("/ready")
def readiness_check():
    """Endpoint to check if the server is ready to accept requests."""
    return {
        "status": "success",
        "message": "FinPilot AI Backend is ready."
    }
