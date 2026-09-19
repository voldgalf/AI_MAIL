from database import Mail, Mailbox
from typing import Any
from pydantic import BaseModel


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


class ResponseAuthenticate(ResponseBase):
    data: dict[str, str] | None

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


class ResponseSendMail(BaseModel):
    data: Mail | None
    

# Reading Inbox


class RequestReadInbox(RequestCredientals):
    pass


class ResponseReadInbox(BaseModel):
    data: list[Mail] | None

