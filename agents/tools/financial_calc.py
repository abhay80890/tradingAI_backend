def safe_float(val: any, default: float = 0.0) -> float:
    """Safely convert a string/value to a float, returning default if missing or invalid."""
    try:
        if val is None or val == "None" or val == "":
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning a default if denominator is 0."""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def calculate_gross_margin(revenue: float, gross_profit: float) -> float:
    """Calculates Gross Margin = Gross Profit / Revenue"""
    return safe_divide(gross_profit, revenue)

def calculate_net_margin(revenue: float, net_income: float) -> float:
    """Calculates Net Margin = Net Income / Revenue"""
    return safe_divide(net_income, revenue)

def calculate_roe(net_income: float, shareholder_equity: float) -> float:
    """Calculates Return on Equity (ROE) = Net Income / Shareholder Equity"""
    return safe_divide(net_income, shareholder_equity)

def calculate_debt_to_equity(total_debt: float, shareholder_equity: float) -> float:
    """Calculates Debt to Equity Ratio = Total Debt / Shareholder Equity"""
    return safe_divide(total_debt, shareholder_equity)
