from fastapi.routing import APIRouter

from classes import RequestAuthenticate, ResponseAuthenticate, RequestCreateMailbox, ResponseCreateMailbox, ResponseSendMail, RequestSendMail, RequestReadInbox, ResponseReadInbox

from exception import MailException

from database import database_dependency, select, Mailbox, Message

from sessions import session_manager
import re

import bcrypt

router = APIRouter()


def contains_special_characters(string: str):
    if re.search(r'[^a-zA-Z0-9]', string):
        raise MailException(
            "Mailbox address cannot contain special characters")
    return None


@router.get("/authenticate", response_model=ResponseAuthenticate)
def authenticate(database: database_dependency, request: RequestAuthenticate):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    if not (bcrypt.checkpw(request.password.encode('utf-8'), existing_mailbox.password_hash)):
        raise MailException("Invalid password for mailbox")

    session_token = session_manager.create_token(
        existing_mailbox.id, existing_mailbox.address)

    return ResponseAuthenticate(data={"jwt": session_token, "address": existing_mailbox.address})


@router.get("/create-mailbox", response_model=ResponseCreateMailbox)
def create_mailbox(database: database_dependency, request: RequestCreateMailbox):
    if (_ := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox already exists")

    contains_special_characters(request.address)

    hashed_password: bytes = bcrypt.hashpw(
        request.password.encode('utf-8'), bcrypt.gensalt())

    new_mailbox = Mailbox(address=request.address,
                          password_hash=hashed_password)

    database.add(new_mailbox)
    database.commit()
    database.refresh(new_mailbox)

    response = ResponseCreateMailbox(data=new_mailbox)

    return response


@router.get("/send", response_model=ResponseSendMail)
def send_mail(database: database_dependency, request: RequestSendMail):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    if not (session_manager.validate_token(existing_mailbox.id, jwt=request.jwt)):
        raise MailException("Invalid session token")

    contains_special_characters(request.address)

    new_mail = Message(recipient_address=request.recipient, sender_address=existing_mailbox.address,
                       subject=request.subject, content=request.content)

    database.add(new_mail)
    database.commit()
    database.refresh(new_mail)

    response = ResponseSendMail(data=new_mail)

    return response


@router.get("/read-inbox", response_model=ResponseReadInbox)
def read_inbox(database: database_dependency, request: RequestReadInbox):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    if not (session_manager.validate_token(existing_mailbox.id, jwt=request.jwt)):
        raise MailException("Invalid session token")

    mail = database.exec(select(Message).where(
        Message.recipient_address == request.address)).all()

    response = ResponseReadInbox(data=list(mail))

    return response
