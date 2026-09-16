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


if __name__ == "__main__":
    companies = get_active_companies()

    for company in companies:
        print(company)
