import os
from sqlalchemy import create_engine, text, Table, MetaData
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert
from utils.logger import setup_logger

logger = setup_logger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception:
        logger.exception("DB is down. Check with admin")
        return False

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

def company_exists(code):
    query = text("""
        SELECT 1
        FROM company
        WHERE code = :code
    """)
    with engine.connect() as connection:
        result = connection.execute(query,{"code": code})
    return result.first() is not None

def insert_company(company):
    try:
        with engine.begin() as connection:
            if company_exists(company["code"]):
                logger.warning("Company %s already exists. Insert Rejected",company['code'])
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
            logger.info("Company %s has been inserted",company['code'])
            return True
    except Exception:
        logger.exception("Failed to insert company: %s", company['code'])
        raise
################################################################
# Price functions
################################################################
def get_last_prices():
    try:
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
        logger.debug("Retrived lastest prices for %s companies",len(last_prices))
        return last_prices
    except Exception:
        logger.exception("failed to get last price")
        raise

def insert_data(data):
    try: 
        with engine.begin() as connection:
            meta_data = MetaData()
            target_table = Table('price', meta_data,autoload_with=connection)
            records = data.to_dict(orient='records')

            if records:
                insert_statement = insert(target_table).values(records)
                do_nothing = insert_statement.on_conflict_do_nothing(
                    index_elements=["code","date"]).returning(target_table.c.code)
                result = connection.execute(do_nothing)
                inserted_count = len(result.fetchall())
                processed_count = len(records)
                
                if inserted_count == 0:
                    logger.info("Processed %s price records; no new records inserted",processed_count)
                else:
                    logger.info("Processed %s price records; inserted %s new records",processed_count,inserted_count)
    
    except Exception:
        logger.exception("Failed to insert data")
        raise

def get_prices(code):
    try:
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
            logger.debug("get data successful")
        return prices
    except Exception:
        logger.exception("failed to get price")
        raise
