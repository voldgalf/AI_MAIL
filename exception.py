# Copyright (C) 2026 Michael MacMullen

from enum import Enum


class MailExceptionTypes(Enum):
    MAILBOX_PASSWORD_INCORRECT        = ("mailbox_password_incorrect",   401, "Incorrect password")
    MAILBOX_ADDRESS_NONEXISTENT       = ("mailbox_address_nonexistent",  401, "Mailbox does not exist")
    MAILBOX_ADDRESS_HAS_SPECIAL_CHARS = ("mailbox_address_special_chars", 422, "Address contains invalid characters")
    MAILBOX_ALREADY_EXISTS            = ("mailbox_already_exists",       409, "Mailbox already exists")
    MAILBOX_INVALID_SESSION_TOKEN     = ("mailbox_invalid_session_token", 401, "Invalid session token")
    MISSING_CREDENTIALS               = ("missing_credentials",          401, "Missing credentials")
    REDIS_NOT_INITIALIZED             = ("redis_not_initialized",        500, "Internal server error")

    def __init__(self, code: str, status_code: int, detail: str):
        self.code = code
        self.status_code = status_code
        self.detail = detail

class MailException(Exception):
    def __init__(self, code: MailExceptionTypes):
        self.code: MailExceptionTypes = code