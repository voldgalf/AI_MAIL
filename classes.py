# Copyright (C) 2026 Michael MacMullen

from database import Mail, Mailbox
from typing import Any
from pydantic import BaseModel
import uuid


class RequestCredientals(BaseModel):
    address: str
    jwt: str


class ResponseBase(BaseModel):
    success: bool = True
    message: str = ""
    data: Any

# Authentication


class RequestAuthenticate(BaseModel):
    address: str
    password: str


class ResponseAuthenticateDataWrapper(BaseModel):
    jwt: str


class ResponseAuthenticate(ResponseBase):
    data: ResponseAuthenticateDataWrapper | None

# Creation


class RequestCreateMailbox(BaseModel):
    address: str
    password: str


class ResponseCreateMailbox(ResponseBase):
    data: Mailbox | None

# Sending Messages


class RequestSendMail(RequestCredientals):
    subject: str
    recipient: str
    content: str
    pass


class ResponseSendMail(ResponseBase):
    data: Mail | None


# Reading Inbox


class RequestReadInbox(RequestCredientals):
    pass


class ResponseReadInbox(ResponseBase):
    data: list[Mail] | None

class RequestReadMessage(RequestCredientals):
    message_id: str
    pass


class ResponseReadMessage(ResponseBase):
    data: Mail | None
