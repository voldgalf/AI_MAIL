engine = create_engine("sqlite:///database.db")

def create_database_session():
    with Session(engine) as session:
        yield session

database_dependency = Annotated[Session, Depends(create_database_session)]
