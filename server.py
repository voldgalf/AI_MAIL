from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from classes import ResponseBase
from exception import MailException
import uvicorn
from typing import Any

class ServerManager():
    def __init__(self) -> None:
        self.app = FastAPI()
    def run(self, config: dict[str, Any]):
        
        server_config = config.get("server", {})

        address = server_config.get("address", "127.0.0.1")
        port = server_config.get("port", 6379)
        
        uvicorn.run(server_manager.app, host=address, port=port)    

server_manager = ServerManager()


@server_manager.app.exception_handler(MailException)
async def mail_exception_handler(request: Request, err: MailException):

    error_response = ResponseBase(
        success=False, message=err.code.name, data=None)
    return JSONResponse(status_code=200, content=error_response.model_dump())

#app.include_router(router)

#uvicorn.run(app, host=)
