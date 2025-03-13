import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    WHITE = 4  # Data is missing

def latest_financial_index(data: dict):
    """Find the latest standalone financial index."""
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index: int):
    """Get total revenue from financial data."""
    try:
        return data["financials"][financial_index]["pnl"]["lineItems"]["netRevenue"]
    except (KeyError, IndexError, TypeError):
        return None

def total_borrowing(data: dict, financial_index: int):
    """Calculate total borrowings."""
    try:
        bs = data["financials"][financial_index]["bs"]["lineItems"]
        return bs["longTermBorrowings"] + bs["shortTermBorrowings"]
    except (KeyError, IndexError, TypeError):
        return None

def borrowing_to_revenue_flag(data: dict, financial_index: int):
    """Determine the flag for borrowing-to-revenue ratio."""
    revenue = total_revenue(data, financial_index)
    borrowing = total_borrowing(data, financial_index)
    if revenue is None or borrowing is None or revenue == 0:
        return FLAGS.WHITE
    return FLAGS.GREEN if (borrowing / revenue) <= 0.25 else FLAGS.AMBER
