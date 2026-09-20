import requests
from fastmcp import FastMCP

from classes import RequestAuthenticate, ResponseAuthenticate, ResponseCreateMailbox, RequestCreateMailbox, ResponseReadInbox, RequestReadInbox, RequestSendMail, ResponseSendMail, RequestReadMessage, ResponseReadMessage
class ElmA():
    def __init__(self) -> None:
        self.address: str = "agentA"
        self.password: str = "password"
        self.jwt: str = ""
        self.authenticated: bool = False
        self.app = FastMCP("ElmA")

        self.app.add_tool(self.create_mailbox)
        self.app.add_tool(self.authenticate)
        self.app.add_tool(self.read_inbox)
        self.app.add_tool(self.send_message)
        self.app.add_tool(self.read_message)

    def create_mailbox(self):
        response = requests.get("http://127.0.0.1:8000/create-mailbox", json=RequestCreateMailbox(
            address=self.address, password=self.password).model_dump())

        response_formatted: ResponseCreateMailbox = ResponseCreateMailbox.model_validate(
            response.json())

        return response_formatted.model_dump()

    def authenticate(self):

        response = requests.get("http://127.0.0.1:8000/authenticate", json=RequestAuthenticate(
            address=self.address, password=self.password).model_dump())

        response_formatted: ResponseAuthenticate = ResponseAuthenticate.model_validate(
            response.json())

        print(response_formatted)

        if (response_formatted.success and response_formatted.data):
                self.jwt = response_formatted.data.jwt
                self.authenticated = True

        return response_formatted.model_dump()

    def read_inbox(self):

        response = requests.get("http://127.0.0.1:8000/read-inbox",
                                json=RequestReadInbox(address=self.address, jwt=self.jwt).model_dump())

        response_formatted = ResponseReadInbox.model_validate(response.json())

        return response_formatted.model_dump()

    def send_message(self, recipient_address: str, subject: str, message: str):

        response = requests.get("http://127.0.0.1:8000/send-message", json=RequestSendMail(
            address=self.address, jwt=self.jwt, subject=subject, recipient=recipient_address, content=message).model_dump())

        response_formatted = ResponseSendMail.model_validate(response.json())

        return response_formatted.model_dump()

    def read_message(self, message_id: str):

        response = requests.get("http://127.0.0.1:8000/read-message", json=RequestReadMessage(
            address=self.address, jwt=self.jwt, message_id=message_id).model_dump())

        response_formatted = ResponseReadMessage.model_validate(response.json())

        return response_formatted.model_dump()


elma = ElmA()


if __name__ == "__main__":
    elma.app.run(transport="stdio")
