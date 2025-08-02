
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yfinance as yf

app = FastAPI(
    title="YFinance Extended Stock Connector API",
    description="Fetches stock and valuation data (EV/EBITDA, shares) using yfinance.",
    version="1.1.0"
)

def safe_get(data, key, default=None):
    return data[key] if key in data and data[key] is not None else default

@app.get("/stock-extended-summary", summary="Get Extended Stock Data", description="Returns key valuation metrics and shares outstanding.")
def get_extended_stock_data(ticker: str = Query(..., description="Stock ticker symbol (e.g., AAPL, MSFT, M7, ^GSPC)")):
    stock = yf.Ticker(ticker)

    try:
        info = stock.info
        shares_outstanding = safe_get(info, "sharesOutstanding")
        ev_to_ebitda = safe_get(info, "enterpriseToEbitda")  # most recent EV/EBITDA

        result = {
            "ticker": ticker.upper(),
            "shares_outstanding": shares_outstanding,
            "ev_to_ebitda": ev_to_ebitda,
        }

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
