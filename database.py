from sqlmodel import SQLModel, Field, LargeBinary, Column, create_engine, Session, select
from sqlalchemy import Engine
import uuid
from typing import Any
import bcrypt


class Mailbox(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    address: str
    password_hash: bytes = Field(sa_column=Column(LargeBinary), exclude=True)


class Mail(SQLModel, table=True):
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
            
    def get_mailbox_by_property(self, property: str, value: str) -> Mailbox | None:

        col = getattr(Mailbox, property, None)

        if col not in Mailbox.model_fields:
            return None
        
        with Session(engine_manager.sql_engine) as session:
            found_mailbox = session.exec(select(Mailbox).where(
                col == value)).first()

            return found_mailbox

    def get_mail_by_property(self, property: str, value: str) -> list[Mail]:
        col = getattr(Mail, property, None)

        if col not in Mail.model_fields:
            return []

        with Session(engine_manager.sql_engine) as session:
            found_mail = session.exec(select(Mail).where(col == value)).all()
            return list(found_mail)

    def add_mailbox(self, mailbox: Mailbox):
        with Session(engine_manager.sql_engine) as session:
            session.add(mailbox)
            session.commit()
            session.refresh(mailbox)
            
        return True
    
    def add_mail(self, mail: Mail):
        with Session(engine_manager.sql_engine) as session:
            session.add(mail)
            session.commit()
            session.refresh(mail)
            
        return True

engine_manager = EngineManager()
