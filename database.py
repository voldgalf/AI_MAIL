from sqlmodel import SQLModel, Field, LargeBinary, Column, create_engine, Session, select
from fastapi import Depends
from typing import Annotated
import uuid


class Mailbox(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    address: str
    password_hash: bytes = Field(sa_column=Column(LargeBinary))


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    recipient_address: str
    sender_address: str
    subject: str
    content: str


engine = create_engine("sqlite:///database.db")


def create_database_session():
    with Session(engine) as session:
        yield session


database_dependency = Annotated[Session, Depends(create_database_session)]
