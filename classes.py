from database import Message, Mailbox
from typing import Any
from pydantic import BaseModel


class RequestBase(BaseModel):
    address: str
    jwt: str


class ResponseBase(BaseModel):
    success: bool = True
    message: str = ""
    data: Any = None

# Authentication


class RequestAuthenticate(BaseModel):
    address: str
    password: str


class ResponseAuthenticate(ResponseBase):
    address: str
    jwt: str

# Creation


class RequestCreateMailbox(BaseModel):
    address: str
    password: str


class ResponseCreateMailbox(BaseModel):
    mailbox: Mailbox

# Sending Messages


class RequestSendMail(RequestBase):
    subject: str
    recipient: str
    content: str
    pass


class ResponseSendMail(BaseModel):
    mail: Message
