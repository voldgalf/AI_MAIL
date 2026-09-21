from classes import RequestCredientals
from fastapi import Depends
from exception import MailException, MailExceptionTypes
from typing import Annotated
from sessions import session_manager

from database import engine_manager, Mailbox


def validate_mailbox(request: RequestCredientals):

    if len(request.address) == 0 or len(request.jwt) == 0:
        raise MailException(MailExceptionTypes.MISSING_CREDENTIALS)

    if not (existing_mailbox := engine_manager.get_mailbox_by_property("address", request.address)):
        raise MailException(MailExceptionTypes.MAILBOX_ADDRESS_NONEXISTENT)

    if not (session_manager.validate_token(existing_mailbox.id, jwt=request.jwt)):
        raise MailException(MailExceptionTypes.MAILBOX_INVALID_SESSION_TOKEN)

    return existing_mailbox


authenticate_dependency = Annotated[Mailbox, Depends(validate_mailbox)]
