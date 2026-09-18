import os
from sqlalchemy import create_engine, text, Table, MetaData
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


################################################################
# Company functions
################################################################
def get_all_companies():
    query = text("""
        SELECT code, name, exchange
        FROM company
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

def company_exists(connection, code):
    query = text("""
        SELECT 1
        FROM company
        WHERE code = :code
    """)
    with engine.connect() as connection:
        result = connection.execute(query,{"code": code})
    return result.first() is not None

def insert_company(company):
    with engine.begin() as connection:
        if company_exists(connection, company["code"]):
            print(
                f"Company {company['code']} already exists. Failed to upload"
            )
        return False
        query = text("""
            INSERT INTO company(code, name, exchange, active)
            VALUES (:code, :name, :exchange, :active)
        """)
        connection.execute(query, {
            "code": company["code"],
            "name": company["name"],
            "exchange": company["exchange"],
            "active": company["active"]
        })
        return True

################################################################
# Price functions
################################################################
def get_last_prices():
    query = text("""
        SELECT DISTINCT ON (code)
            code,
            close
        FROM price
        ORDER BY code, date DESC
    """)
    with engine.connect() as connection:
        result = connection.execute(query)
        with engine.connect() as connection:
            result = connection.execute(query)
            last_prices = {}
        
            for row in result:
                last_prices[row.code] = row.close
        return last_prices

def upload_data(data):
     with engine.begin() as connection:
        meta_data = MetaData()
        target_table = Table('price', meta_data,autoload_with=connection)
        records = data.to_dict(orient='records')

        if records:
            insert_statment = insert(target_table).values(records)
            do_nothing = insert_statment.on_conflict_do_nothing(
                index_elements=["code","date"]
            )
            connection.execute(do_nothing)

def get_prices(code):
    query = text("""
        SELECT date,
            open,
            high,
            low,
            close,
            change_dollar,
            change_pct,
            volume
        FROM price
        WHERE code = :code
    """)
    with engine.connect() as connection:
        result = connection.execute(query,{"code":code} )

        prices = []        
        for row in result:
            prices.append({
                "date": row.date,
                "open": row.open,
                "high": row.high,
                "low": row.low,
                "close": row.close,
                "change_dollar": row.change_dollar,
                "change_pct": row.change_pct,
                "volume": row.volume
            })
    return prices
