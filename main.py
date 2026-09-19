from database import Mailbox, Message, database_dependency
from classes import RequestAuthenticate, ResponseAuthenticate, ResponseBase
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exception import MailException

app = FastAPI()

@app.exception_handler(MailException)
async def mail_exception_handler(request: Request, err: MailException):
    error_response = ResponseBase(
        success=False, message=err.message, data=None)
    return JSONResponse(status_code=200, content=error_response.model_dump())
