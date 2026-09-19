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


@router.get("/create-mailbox", response_model=ResponseCreateMailbox)
def create_mailbox(database: database_dependency, request: RequestCreateMailbox):
    if (existing_mailbox := database.exec(select(Mailbox).where(Mailbox.address == request.address)).first()):
        raise MailException("Mailbox already exists")
    
    hashed_password: bytes = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    
    new_mailbox = Mailbox(address=request.address, password_hash=hashed_password)
        
    database.add(new_mailbox)
    database.commit()
    database.refresh(new_mailbox)
    
    response = ResponseCreateMailbox(mailbox=new_mailbox)
    
    return response
