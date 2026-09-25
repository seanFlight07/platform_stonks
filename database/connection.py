import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
database_user = os.environ["POSTGRES_USER"]
database_password = os.environ["POSTGRES_PASSWORD"]
database_name = os.environ["POSTGRES_DB"]

database_url = (
    f"postgresql+psycopg://"
    f"{database_user}:{database_password}"
    f"@localhost:5432/{database_name}"
)

engine = create_engine(
    database_url
)
