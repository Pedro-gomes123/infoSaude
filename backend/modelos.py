from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Postos(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    nome_oficial: str|None
    endereco: str|None
    bairro: str|None
    fone: str|None
    servico: str|None
    especialidade: str|None
    como_usar: str|None
    horario: str|None
    latitude: float|None
    longitude: float|None

class ListarPosto(BaseModel):
    id: int
    nome_oficial: str
    endereco: str
    bairro: str
    especialidade: str