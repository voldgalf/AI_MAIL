from sqlmodel import SQLModel, Field, LargeBinary, Column, create_engine, select
import uuid


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


engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)