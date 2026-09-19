from database import Message, Mailbox
from typing import Any
from pydantic import BaseModel

class RequestBase(BaseModel):
    address: str
    jwt: str
    
class ResponseBase(BaseModel):
    success: bool
    message: str
    data: Any
    pass


# Authentication

class RequestAuthenticate(BaseModel):
    address: str
    password: str
    
class ResponseAuthenticate(BaseModel):
    address: str
    jwt: str