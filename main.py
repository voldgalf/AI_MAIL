from classes import ResponseBase
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exception import MailException
from sessions import session_manager
from database import engine_manager
from routes import router
import tomllib
from pathlib import Path

config = tomllib.loads(Path("./config.toml").read_text())

session_manager.start(config)
engine_manager.start(config)
app = FastAPI()

@app.exception_handler(MailException)
async def mail_exception_handler(request: Request, err: MailException):
    error_response = ResponseBase(
        success=False, message=err.message, data=None)
    return JSONResponse(status_code=200, content=error_response.model_dump())

app.include_router(router)