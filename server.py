# Copyright (C) 2026 Michael MacMullen

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint
from fastapi.responses import JSONResponse
from classes import ErrorResponse
from exception import MailException
import uvicorn
from typing import Any
from logger import log_manager


class ServerManager():
    def __init__(self) -> None:
        self.app = FastAPI()
        log_manager.logger.info(f"{self.__class__.__name__} initialized")

    def start(self, config: dict[str, Any]):

        log_manager.logger.info(f"{self.__class__.__name__} started")

        server_config = config.get("server", {})

        address = server_config.get("address", "127.0.0.1")
        port = server_config.get("port", 8000)

        uvicorn.run(server_manager.app, host=address, port=port)


server_manager = ServerManager()


@server_manager.app.middleware("http")
async def mail_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    if (request.client):
        log_manager.logger.info(
            f"{request.client.host}:{request.client.port} - {request.url.path}")
    response: Response = await call_next(request)
    return response

@server_manager.app.exception_handler(MailException)
async def mail_exception_handler(request: Request, err: MailException):

    if (request.client):
        log_manager.logger.info(
            f"{request.client.host}:{request.client.port}\t{err.code.name}")

    error_response = ErrorResponse(message=err.code.detail)
    return JSONResponse(status_code=err.code.status_code, content=error_response.model_dump())
