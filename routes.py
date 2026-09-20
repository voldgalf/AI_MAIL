# Copyright (C) 2026 Michael MacMullen

from fastapi import Request
from fastapi.routing import APIRouter

from classes import RequestAuthenticate, ResponseAuthenticate, RequestCreateMailbox, ResponseCreateMailbox, ResponseSendMail, RequestSendMail, RequestReadInbox, ResponseReadInbox, ResponseAuthenticateDataWrapper, RequestReadMessage, ResponseReadMessage, ResponseHealth, ResponseHealthDataWrapper

from exception import MailException, MailExceptionTypes

from database import Mailbox, Mail

from depends import authenticate_dependency

from database import engine_manager

from sessions import session_manager
import re

import bcrypt

router = APIRouter()


def contains_special_characters(string: str):   
    if re.search(r'[^a-zA-Z0-9]', string):
        raise MailException(
            MailExceptionTypes.MAILBOX_ADDRESS_HAS_SPECIAL_CHARS)
    return None


@router.get("/health", response_model=ResponseHealth)
def health(request: Request):
    return ResponseHealth(data=ResponseHealthDataWrapper(status="ok"))


@router.post("/authenticate", response_model=ResponseAuthenticate)
def authenticate(request: RequestAuthenticate):
    if not (existing_mailbox := engine_manager.get_mailbox_by_property("address", request.address)):
        raise MailException(MailExceptionTypes.MAILBOX_ADDRESS_NONEXISTANT)

    if not engine_manager.check_mailbox_password(existing_mailbox, request.password):
        raise MailException(MailExceptionTypes.MAILBOX_PASSWORD_INCORRECT)

    session_token = session_manager.create_token(
        existing_mailbox.id, existing_mailbox.address)

    return ResponseAuthenticate(data=ResponseAuthenticateDataWrapper(jwt=session_token))


@router.post("/create-mailbox", response_model=ResponseCreateMailbox)
def create_mailbox(request: RequestCreateMailbox):
    if (_ := engine_manager.get_mailbox_by_property("address", request.address)):
        raise MailException(MailExceptionTypes.MAILBOX_ALREADY_EXISTS)

    contains_special_characters(request.address)

    hashed_password: bytes = bcrypt.hashpw(
        request.password.encode('utf-8'), bcrypt.gensalt())

    new_mailbox = Mailbox(address=request.address,
                          password_hash=hashed_password)

    engine_manager.add_mailbox(new_mailbox)

    response = ResponseCreateMailbox(data=new_mailbox)

    return response


@router.post("/send-message", response_model=ResponseSendMail)
def send_mail(existing_mailbox: authenticate_dependency, request: RequestSendMail):
    contains_special_characters(request.address)

    new_mail = Mail(recipient_address=request.recipient, sender_address=existing_mailbox.address,
                    subject=request.subject, content=request.content)

    engine_manager.add_mail(new_mail)

    response = ResponseSendMail(data=new_mail)

    return response


@router.post("/read-message", response_model=ResponseReadMessage)
def read_message(existing_mailbox: authenticate_dependency, request: RequestReadMessage):

    found_mail = engine_manager.get_mail_by_id(
        recipient_address=existing_mailbox.address, id=request.message_id)
    response = ResponseReadMessage(data=found_mail)

    return response


@router.post("/read-inbox", response_model=ResponseReadInbox)
def read_inbox(existing_mailbox: authenticate_dependency, request: RequestReadInbox):

    found_mail = engine_manager.get_mail_by_property(
        "recipient_address", existing_mailbox.address)

    response = ResponseReadInbox(data=found_mail)

    return response
