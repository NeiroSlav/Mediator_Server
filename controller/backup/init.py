from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    MetaData,
    Table,
    Date,
    Time,
)
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

dialogs = Table(
    "dialogs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date, nullable=False),
    Column("start_time", Time, nullable=False),
    Column("answer_rate", Time, nullable=False),
    Column("finish_rate", Time, nullable=False),
    Column("user", String, nullable=False),
)

# Создание базы данных и таблицы, если они не существуют
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
