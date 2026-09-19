from sqlmodel import Session, select
from classes import RequestCredientals
from fastapi import Depends
from exception import MailException
from typing import Annotated
from sessions import session_manager

from database import engine, Mailbox

def create_database_session():
    with Session(engine) as session:
        yield session


database_dependency = Annotated[Session, Depends(create_database_session)]

def validate_mailbox(request: RequestCredientals, database: database_dependency):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    if not (session_manager.validate_token(existing_mailbox.id, jwt=request.jwt)):
        raise MailException("Invalid session token")
    
    return existing_mailbox

authenticate_dependency = Annotated[Mailbox, Depends(validate_mailbox)]