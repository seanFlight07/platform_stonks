import yfinance as yf

def api_fetch_stock(ticker, exchange):
    unique_code = str(ticker+"."+exchange)
    data = yf.download(unique_code,period='1d')
    return data    
