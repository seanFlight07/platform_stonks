import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.dialects.postgresql import insert

from utils.logger import setup_logger

logger = setup_logger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL env is not set")

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
def get_company(code):
    query = text("""
        SELECT code, name, exchange
        FROM company
        WHERE code = :code
    """)
    with engine.connect() as connection:
        result = connection.execute(query,{"code": code})
        row = result.first()

        if row is None:
            return None

        return {
            "code": row.code,
            "name": row.name,
            "exchange": row.exchange
        }

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
            ORDER BY date DESC
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

################################################################
# Exchange Market functions
################################################################
def get_exchange(exchange):
    query = text("""
                 SELECT timezone,
                 blackout_start,
                 blackout_end
                 FROM exchange
                 WHERE exchange = :exchange
                 """)
    with engine.connect() as connection:
        result = connection.execute(query, {"exchange":exchange})
        exchange_info = result.first()

        if exchange_info is None:
            logger.warning("No exchange information was found for %s",exchange)
            return None
    return {
        "timezone": exchange_info.timezone,
        "blackout_start": exchange_info.blackout_start,
        "blackout_end": exchange_info.blackout_end
    }

################################################################
# User functions
################################################################
def get_user_by_email(email):
    query = text("""
        SELECT id, email, password_hash, role, active
        FROM users
        WHERE email = :email
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query,{"email": email})
            user = result.mappings().fetchone()
            if user:
                logger.info("User was found with email %s",email)
                return user
            logger.info("No user was found with email %s",email)
            return None
    except Exception:
        logger.warning("Failed to get user by email: %s",email)
        raise

def get_user_by_id(id):
    query = text("""
        SELECT id, email, password_hash, role, active
        FROM users
        WHERE id = :id
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query,{"id": id})
            user = result.mappings().fetchone()
            if user:
                logger.info("User was found with id %s exists",id)
                return user
            logger.info("User was not found with id %s",id)
            return None
    except Exception:
        logger.warning("Failed to get user by id: %s",id)
        raise

def create_user(email, password_hash):
    try:
        query = text("""
            INSERT INTO users (email, password_hash)
            VALUES (:email, :password_hash)
        """)

        user = get_user_by_email(email)

        if user:
            return False

        with engine.begin() as connection:
            connection.execute(
                query,
                {
                    "email": email,
                    "password_hash": password_hash
                }
            )

        logger.info("User added with email %s", email)
        return True

    except Exception:
        logger.exception("Could not insert user with email %s", email)
        raise

