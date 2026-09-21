# Copyright (C) 2026 Michael MacMullen

from fastapi import Request
from fastapi.routing import APIRouter

from classes import RequestAuthenticate, RequestCreateMailbox, RequestSendMail, RequestReadInbox, ResponseAuthenticateDataWrapper, RequestReadMessage, ResponseHealthDataWrapper, ResponseBase, ErrorResponse

from exception import MailException, MailExceptionTypes

from database import Mailbox, Mail

from depends import authenticate_dependency

from database import engine_manager

from sessions import session_manager
import re

import bcrypt

router = APIRouter(responses={401: {"model": ErrorResponse}, 500: {
                   "model": ErrorResponse}, 400: {"model": ErrorResponse}})


def contains_special_characters(string: str):
    if re.search(r'[^a-zA-Z0-9]', string):
        raise MailException(
            MailExceptionTypes.MAILBOX_ADDRESS_HAS_SPECIAL_CHARS)
    return None


@router.get("/health", response_model=ResponseBase[ResponseHealthDataWrapper])
def health(request: Request) -> ResponseBase[ResponseHealthDataWrapper]:
    return ResponseBase[ResponseHealthDataWrapper](data=ResponseHealthDataWrapper(status="ok"))


@router.post("/authenticate", response_model=ResponseBase[ResponseAuthenticateDataWrapper])
def authenticate(request: RequestAuthenticate) -> ResponseBase[ResponseAuthenticateDataWrapper]:
    if not (existing_mailbox := engine_manager.get_mailbox_by_property("address", request.address)):
        raise MailException(MailExceptionTypes.MAILBOX_ADDRESS_NONEXISTANT)

    if not engine_manager.check_mailbox_password(existing_mailbox, request.password):
        raise MailException(MailExceptionTypes.MAILBOX_PASSWORD_INCORRECT)

    session_token = session_manager.create_token(
        existing_mailbox.id, existing_mailbox.address)

    return ResponseBase[ResponseAuthenticateDataWrapper](data=ResponseAuthenticateDataWrapper(jwt=session_token))


@router.post("/create-mailbox", response_model=ResponseBase[Mailbox])
def create_mailbox(request: RequestCreateMailbox) -> ResponseBase[Mailbox]:
    if (_ := engine_manager.get_mailbox_by_property("address", request.address)):
        raise MailException(MailExceptionTypes.MAILBOX_ALREADY_EXISTS)

    contains_special_characters(request.address)

    hashed_password: bytes = bcrypt.hashpw(
        request.password.encode('utf-8'), bcrypt.gensalt())

    new_mailbox = Mailbox(address=request.address,
                          password_hash=hashed_password)

    engine_manager.add_mailbox(new_mailbox)

    response = ResponseBase[Mailbox](data=new_mailbox)

    return response


@router.post("/send-message", response_model=ResponseBase[Mail])
def send_mail(existing_mailbox: authenticate_dependency, request: RequestSendMail) -> ResponseBase[Mail]:
    contains_special_characters(request.address)

    new_mail = Mail(recipient_address=request.recipient, sender_address=existing_mailbox.address,
                    subject=request.subject, content=request.content)

    engine_manager.add_mail(new_mail)

    response = ResponseBase[Mail](data=new_mail)

    return response


@router.post("/read-message", response_model=ResponseBase[Mail])
def read_message(existing_mailbox: authenticate_dependency, request: RequestReadMessage) -> ResponseBase[Mail]:

    found_mail = engine_manager.get_mail_by_id(
        recipient_address=existing_mailbox.address, id=request.message_id)
    response = ResponseBase[Mail](data=found_mail)

    return response


@router.post("/read-inbox", response_model=ResponseBase[list[Mail]])
def read_inbox(existing_mailbox: authenticate_dependency, request: RequestReadInbox) -> ResponseBase[list[Mail]]:

    found_mail = engine_manager.get_mail_by_property(
        "recipient_address", existing_mailbox.address)

    response = ResponseBase[list[Mail]](data=found_mail)

    return response
