import pandas as pd
from sqlalchemy import MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

from utils.db import engine as default_engine
from utils.logger import setup_logger

logger = setup_logger(__name__)

class PriceRepository:
    def __init__(self, db_engine: Engine = default_engine):
        self.engine = db_engine

    def get_last_prices(self):
        try:
            query = text("""
                SELECT DISTINCT ON (code)
                    code,
                    close
                FROM price
                ORDER BY code, date DESC
            """)
            with self.engine.connect() as connection:
                result = connection.execute(query)
                last_prices = {}
        
                for row in result:
                    last_prices[row.code] = row.close
            logger.debug("Retrived lastest prices for %s companies",len(last_prices))
            return last_prices
        except Exception:
            logger.exception("failed to get last price")
            raise

    def insert_data(self,data: pd.DataFrame):
        try: 
            with self.engine.begin() as connection:
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

    def get_prices(self,code:str):
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
            with self.engine.connect() as connection:
                result = connection.execute(query,{"code":code} )

                prices = [dict(row) for row in result.mappings()] 
                logger.debug("get data successful")
            return prices
        except Exception:
            logger.exception("failed to get price")
            raise


