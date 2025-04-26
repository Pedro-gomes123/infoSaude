from sqlmodel import  create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends
from modelos import Postos

url_bancodedados = "sqlite:///bdinfosaude.db"
connect_args = {"check_same_thread":False}

engine = create_engine(url_bancodedados, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def criar_bd():
    SQLModel.metadata.create_all(engine)