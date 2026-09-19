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
    data: dict[str, str] = {}

# Creation


class RequestCreateMailbox(BaseModel):
    address: str
    password: str


class ResponseCreateMailbox(BaseModel):
    data: Mailbox

# Sending Messages


class RequestSendMail(RequestBase):
    subject: str
    recipient: str
    content: str
    pass


class ResponseSendMail(BaseModel):
    data: Message
    

# Reading Inbox


class RequestReadInbox(RequestBase):
    pass


class ResponseReadInbox(BaseModel):
    data: list[Message]

