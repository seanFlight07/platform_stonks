
def add_code(data,code):
    data["code"] = code
    return data

def calculate_dollar_change(data, last_close):
    data["change_dollar"] = (data["Close"] - last_close).round(2)
    return data

def calculate_percentage_change(data,last_close):
    data["change_pct"] = ((data["change_dollar"] / last_close)*100).round(2)
    return data

#Transformation to bring all other functions together
def transform_api_data(data, code, last_close):
    last_close = float(last_close)

    data.columns = data.columns.get_level_values(0)
    data = data.reset_index()

    data = add_code(data, code)
    data = calculate_dollar_change(data, last_close)
    data = calculate_percentage_change(data,last_close)

    data = data.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })
    return data

def transform_api_historical(data,code):
    data.columns = data.columns.get_level_values(0)
    data = data.reset_index()
    data = add_code(data, code)
    data = data.sort_values("Date")
    
    data["change_dollar"] = data["Close"].diff()
    data["change_pct"] = data["Close"].pct_change() * 100
    data = data.dropna(subset=["change_dollar", "change_pct"])
    
    data = data.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })
    return data

def transform_company(company_info):
    return{
        "code": company_info["code"],
        "name": company_info["long_name"],
        "exchange": company_info["exchange"],
        "active": True

    }

