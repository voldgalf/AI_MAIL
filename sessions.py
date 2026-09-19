import redis
import uuid
import jwt
import time

from exception import MailException


class SessionManager():
    def __init__(self):
        self.r = redis.Redis()
        
    def validate_token(self, uuid: uuid.UUID, jwt: str):
        found_token = self.r.get(str(uuid))

        return (found_token == jwt)

    def check_token(self, uuid: uuid.UUID) -> bool:
        found_token = self.r.get(str(uuid))

        return (found_token != None)

    def create_token(self, uuid: uuid.UUID, address: str) -> str:

        if (self.check_token(uuid)):
            raise MailException("Already existing session token!")

        new_token = jwt.encode({"address": address, "uuid": str(
            uuid), "created_at": time.time()}, "secret", algorithm="HS256")

        self.r.set(str(uuid), new_token)

        return new_token


session_manager = SessionManager()
