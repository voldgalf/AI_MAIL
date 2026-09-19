from fastapi.routing import APIRouter

from classes import RequestAuthenticate, ResponseAuthenticate, RequestCreateMailbox, ResponseCreateMailbox, ResponseSendMail, RequestSendMail

from exception import MailException

from database import database_dependency, select, Mailbox, Message

from sessions import session_manager

import bcrypt

router = APIRouter()


@router.get("/authenticate", response_model=ResponseAuthenticate)
def authenticate(database: database_dependency, request: RequestAuthenticate):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    session_token = session_manager.create_token(
        existing_mailbox.id, existing_mailbox.address)

    return ResponseAuthenticate(address=existing_mailbox.address, jwt=session_token)


@router.get("/create-mailbox", response_model=ResponseCreateMailbox)
def create_mailbox(database: database_dependency, request: RequestCreateMailbox):
    if (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox already exists")

    hashed_password: bytes = bcrypt.hashpw(
        request.password.encode('utf-8'), bcrypt.gensalt())

    new_mailbox = Mailbox(address=request.address,
                          password_hash=hashed_password)

    database.add(new_mailbox)
    database.commit()
    database.refresh(new_mailbox)

    response = ResponseCreateMailbox(mailbox=new_mailbox)

    return response


@router.get("/send", response_model=ResponseSendMail)
def send_mail(database: database_dependency, request: RequestSendMail):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    if not (session_manager.validate_token(existing_mailbox.id, jwt=request.jwt)):
        raise MailException("Invalid session token")

    new_mail = Message(recipient_address=request.recipient, sender_address=existing_mailbox.address,
                       subject=request.subject, content=request.content)

    database.add(new_mail)
    database.commit()
    database.refresh(new_mail)

    response = ResponseSendMail(mail=new_mail)

    return response
