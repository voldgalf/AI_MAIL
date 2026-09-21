# Copyright (C) 2026 Michael MacMullen

from pydantic import BaseModel
from typing import Generic, TypeVar


class RequestCredientals(BaseModel):
    address: str
    jwt: str


T = TypeVar("T")

class ResponseBase(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: T | None = None

class ErrorResponse(ResponseBase[None]):
    success: bool = False
    message: str = ""
    data : None = None

# Authentication


class RequestAuthenticate(BaseModel):
    address: str
    password: str


class ResponseAuthenticateDataWrapper(BaseModel):
    jwt: str


# Creation


class RequestCreateMailbox(BaseModel):
    address: str
    password: str

# Sending Messages


class RequestSendMail(RequestCredientals):
    subject: str
    recipient: str
    content: str
    pass

# Reading Inbox


class RequestReadInbox(RequestCredientals):
    pass


class RequestReadMessage(RequestCredientals):
    message_id: str
    pass


class ResponseHealthDataWrapper(BaseModel):
    status: str
