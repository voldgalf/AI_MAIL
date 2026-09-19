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

class RequestCreateMailbox(RequestBase):
    address: str
    password: str
    
class ResponseCreateMailbox(BaseModel):
    address: str
    jwt: str