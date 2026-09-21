# Copyright (C) 2026 Michael MacMullen

from enum import Enum


class MailExceptionTypes(Enum):
    MAILBOX_PASSWORD_INCORRECT = 401
    MAILBOX_ADDRESS_NONEXISTANT = 401
    MAILBOX_ADDRESS_HAS_SPECIAL_CHARS = 401
    MAILBOX_ALREADY_EXISTS = 401
    MAILBOX_INVALID_SESSION_TOKEN = 401
    REDIS_NOT_INITIALIZED = 500
    MISSING_CREDENTIALS = 401

class MailException(Exception):
    def __init__(self, code: MailExceptionTypes):
        self.code: MailExceptionTypes = code