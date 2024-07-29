from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from databases import Database


DATABASE_URL = "sqlite:///./database.db"

database = Database(DATABASE_URL)
metadata = MetaData()

abonents = Table(
    "abonents",
    metadata,
    Column("topic_id", Integer, primary_key=True),
    Column("topic_name", String, nullable=False),
    Column("state", String, nullable=False),
    Column("abon_id", Integer, nullable=False),
    Column("social", String, nullable=False),
)

# Создание базы данных и таблицы, если они не существуют
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
