import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def get_active_companies():
    query = text("""
        SELECT code, name, exchange
        FROM company
        WHERE active = TRUE
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        companies = []

        for row in result:
            companies.append({
                "code": row.code,
                "name": row.name,
                "exchange": row.exchange
            })

    return companies

def get_last_price():
    query = text("""
        SELECT DISTINCT ON (code)
            code,
            close
        FROM price
        ORDER BY code, date DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        last_prices = {}
        
        for row in result:
            last_prices[row.code] = row.close
    return last_prices


if __name__ == "__main__":
    companies = get_active_companies()
    last_price = get_last_price()
    for company in companies:
        code = company["code"]
        print(company)
        print(last_price)
        previous_close = last_price.get(code)

        print(code, previous_close)
