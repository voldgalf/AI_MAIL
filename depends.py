from sqlmodel import Session
from classes import RequestCredientals
from fastapi import Depends
from exception import MailException
from typing import Annotated
from sessions import session_manager

from database import engine_manager, Mailbox


def create_database_session():
    with Session(engine_manager.sql_engine) as session:
        yield session


def validate_mailbox(request: RequestCredientals):

    if not (existing_mailbox := engine_manager.get_mailbox_by_property("address", request.address)):
        raise MailException("Mailbox does not exist")

    if not (session_manager.validate_token(existing_mailbox.id, jwt=request.jwt)):
        raise MailException("Invalid session token")

    return existing_mailbox


authenticate_dependency = Annotated[Mailbox, Depends(validate_mailbox)]
