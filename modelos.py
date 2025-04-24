from sqlmodel import SQLModel, Field

class Postos(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    nome_oficial: str
    endereco: str
    bairro: str
    fone: str
    servico: str
    especialidade: str
    como_usar: str
    horario: str
    latitude: float
    longitude: float