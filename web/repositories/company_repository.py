from sqlalchemy import MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert

from utils.db import engine
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CompanyRepository:
    def get_company(self, code: str):
        query = text("""
            SELECT code, name, exchange
            FROM company
            WHERE code = :code
        """)

        with engine.connect() as connection:
            result = connection.execute(query, {"code": code})
            row = result.mappings().first()

        return dict(row) if row else None

    def get_all_companies(self):
        query = text("""
            SELECT code, name, exchange
            FROM company
        """)

        with engine.connect() as connection:
            result = connection.execute(query)
            return [dict(row) for row in result.mappings()]

    def get_active_companies(self):
        query = text("""
            SELECT code, name, exchange
            FROM company
            WHERE active = TRUE
        """)

        with engine.connect() as connection:
            result = connection.execute(query)
            return [dict(row) for row in result.mappings()]

    def company_exists(self, code: str) -> bool:
        query = text("""
            SELECT 1
            FROM company
            WHERE code = :code
        """)

        with engine.connect() as connection:
            result = connection.execute(query, {"code": code})
            return result.first() is not None

    def insert_company(self, company: dict) -> bool:
        metadata = MetaData()

        try:
            with engine.begin() as connection:
                company_table = Table(
                    "company",
                    metadata,
                    autoload_with=connection
                )

                statement = (
                    insert(company_table)
                    .values(**company)
                    .on_conflict_do_nothing(
                        index_elements=["code"]
                    )
                )

                result = connection.execute(statement)
                inserted = result.rowcount > 0

            if inserted:
                logger.info(
                    "Company %s inserted",
                    company["code"]
                )
            else:
                logger.warning(
                    "Company %s already exists",
                    company["code"]
                )

            return inserted

        except Exception:
            logger.exception(
                "Failed to insert company %s",
                company["code"]
            )
            raise
