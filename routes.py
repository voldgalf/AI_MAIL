from fastapi.routing import APIRouter

from classes import RequestAuthenticate, ResponseAuthenticate

from exception import MailException

from database import database_dependency, select, Mailbox

from sessions import session_manager

router = APIRouter()

@router.get("/authenticate", response_model=ResponseAuthenticate)
def authenticate(database: database_dependency, request: RequestAuthenticate):
    if not (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox does not exist")

    session_token = session_manager.create_token(
        existing_mailbox.id, existing_mailbox.address)

    return ResponseAuthenticate(address=existing_mailbox.address, jwt=session_token)