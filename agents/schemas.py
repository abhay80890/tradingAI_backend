from pydantic import BaseModel, Field
from typing import List, Optional

class MarketDataSchema(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    company_name: str = Field(description="Full name of the company")
    industry: str = Field(description="Industry the company operates in")
    description: str = Field(description="Brief company description")
    current_price: float = Field(description="Current trading price")
    change_percent: str = Field(description="Percentage change today, e.g., '+1.5%'")
    day_high: float = Field(description="Highest price today")
    day_low: float = Field(description="Lowest price today")
    volume: int = Field(description="Trading volume today")
    market_cap: int = Field(description="Total market capitalization")
    pe_ratio: float = Field(description="Price to Earnings ratio")
    fifty_two_week_high: float = Field(description="52 week high price")
    fifty_two_week_low: float = Field(description="52 week low price")
    error: Optional[str] = Field(default=None, description="Any error message encountered")

class RatiosSchema(BaseModel):
    gross_margin: float
    net_margin: float
    roe: float
    debt_to_equity: float

class FinancialMetricsSchema(BaseModel):
    symbol: str
    fiscal_date_ending: str
    total_revenue: float
    gross_profit: float
    net_income: float
    total_assets: float
    total_liabilities: float
    total_debt: float
    shareholder_equity: float
    ratios: RatiosSchema
    error: Optional[str] = Field(default=None)

class TechnicalSignalsSchema(BaseModel):
    symbol: str
    rsi_14: float
    rsi_signal: str = Field(description="Neutral, Overbought, or Oversold")
    sma_20: float
    sma_50: float
    trend_signal: str = Field(description="Bullish or Bearish")
    macd: float
    macd_signal: float
    macd_crossover: str = Field(description="Bullish or Bearish")
    error: Optional[str] = Field(default=None)

class ArticleSchema(BaseModel):
    title: str
    url: str
    score: float

class NewsSentimentSchema(BaseModel):
    symbol: str
    average_score: float
    sentiment_label: str = Field(description="Bullish, Bearish, or Neutral")
    article_count: int
    top_articles: List[ArticleSchema]
    error: Optional[str] = Field(default=None)

class RAGResultSchema(BaseModel):
    symbol: str
    query_used: str
    document_count: int
    excerpts: List[str]
    summary: str
    error: Optional[str] = Field(default=None)

class RiskScoreSchema(BaseModel):
    symbol: str
    risk_score: int = Field(description='Risk score from 1 (Safest) to 10 (Highest Risk)')
    risk_level: str = Field(description='Low, Medium, or High')
    reasoning: str = Field(description='2-3 sentence explanation for the score based on the provided data')
    error: Optional[str] = Field(default=None)

class PortfolioPlanSchema(BaseModel):
    symbol: str
    action: str = Field(description='Buy, Hold, or Sell')
    confidence_score: int = Field(description='Confidence from 1 to 100')
    recommended_allocation: str = Field(description='Percentage allocation, e.g., 5-10%')
    reasoning: str = Field(description='Explanation of the portfolio strategy')
    error: Optional[str] = Field(default=None)

class FinalReportSchema(BaseModel):
    symbol: str
    markdown_report: str = Field(description='The complete, beautifully formatted Markdown report')
    error: Optional[str] = Field(default=None)
