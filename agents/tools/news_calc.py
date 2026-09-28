from typing import Dict, Any, List

def process_news_sentiment(news_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses the Alpha Vantage NEWS_SENTIMENT response.
    Averages the sentiment scores to determine overall market mood.
    Returns the top 5 articles and the aggregate score.
    """
    feed = news_data.get("feed", [])
    
    if not feed:
        return {}
        
    total_score = 0.0
    valid_articles = 0
    top_articles = []
    
    # Process up to 5 articles
    for item in feed[:5]:
        score = item.get("overall_sentiment_score")
        if score is not None:
            try:
                score_float = float(score)
                total_score += score_float
                valid_articles += 1
                
                top_articles.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "published_at": item.get("time_published", ""),
                    "score": score_float
                })
            except ValueError:
                continue
                
    if valid_articles == 0:
        return {}
        
    average_score = total_score / valid_articles
    
    # Alpha Vantage defines sentiment logic:
    # <= -0.15 is Bearish/Negative
    # >= 0.15 is Bullish/Positive
    # Between -0.15 and 0.15 is Neutral
    if average_score >= 0.15:
        sentiment_label = "Bullish"
    elif average_score <= -0.15:
        sentiment_label = "Bearish"
    else:
        sentiment_label = "Neutral"
        
    return {
        "average_score": average_score,
        "sentiment_label": sentiment_label,
        "article_count": valid_articles,
        "articles": top_articles
    }
