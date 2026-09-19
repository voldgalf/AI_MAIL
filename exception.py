from enum import Enum


class MailExceptionTypes(Enum):
    MAILBOX_PASSWORD_INCORRECT = 1
    MAILBOX_ADDRESS_NONEXISTANT = 2
    MAILBOX_ADDRESS_HAS_SPECIAL_CHARS = 3
    MAILBOX_ALREADY_EXISTS = 4
    MAILBOX_INVALID_SESSION_TOKEN = 5
    REDIS_NOT_INITIALIZED = 6


class MailException(Exception):
    def __init__(self, code: MailExceptionTypes):
        self.code: MailExceptionTypes = code
