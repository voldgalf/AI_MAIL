from sqlmodel import SQLModel, Field, LargeBinary, Column, create_engine, Session
from sqlalchemy import Engine
import uuid
from typing import Any


class Mailbox(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    address: str
    password_hash: bytes = Field(sa_column=Column(LargeBinary), exclude=True)


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    recipient_address: str
    sender_address: str
    subject: str
    content: str


class EngineManager():
    def __init__(self):
        self.sql_engine: Engine | None = None

    def start(self, config: dict[str, Any]):

        sql_config = config.get("sql", {})

        uri_string = sql_config.get("uri_string", "sqlite:///database.db")
        self.sql_engine = create_engine(uri_string)

        SQLModel.metadata.create_all(self.sql_engine)


engine_manager = EngineManager()
