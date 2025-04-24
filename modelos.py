from sqlmodel import SQLModel, Field

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