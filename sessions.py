import redis
import uuid
import jwt
import time
from typing import Any

from exception import MailException


class SessionManager():
    def __init__(self):
        self.redis_instance: redis.Redis | None = None

    def start(self, config: dict[str, Any]):

        redis_config = config.get("redis", {})

        address = redis_config.get("address", "127.0.0.1")
        port = redis_config.get("port", 6379)
        self.redis_instance = redis.Redis(address, port, decode_responses=True)

    def validate_token(self, uuid: uuid.UUID, jwt: str):

        if not self.redis_instance:
            raise MailException("Redis not initalized!")

        found_token = self.redis_instance.get(str(uuid))

        return (found_token == jwt)

    def check_token(self, uuid: uuid.UUID) -> bool:

        if not self.redis_instance:
            raise MailException("Redis not initalized!")

        found_token = self.redis_instance.get(str(uuid))

        return (found_token != None)

    def create_token(self, uuid: uuid.UUID, address: str) -> str:

        if not self.redis_instance:
            raise MailException("Redis not initalized!")

        if (self.check_token(uuid)):
            raise MailException("Already existing session token!")

        new_token: str = jwt.encode({"address": address, "uuid": str(  # type: ignore
            uuid), "created_at": time.time()}, "secret", algorithm="HS256")

        self.redis_instance.set(str(uuid), new_token)

        return new_token


session_manager = SessionManager()
