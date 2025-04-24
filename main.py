from fastapi import FastAPI
from modelos import Postos
from bancodedados import SessionDep, criar_bd
from sqlmodel import select, Session, engine
import json

app = FastAPI()

@app.on_event("startup")
def inicializa():
    criar_bd()
    with Session(engine) as session:
        migrar_postos(session)



def migrar_postos(session: SessionDep):
    with open("postos_saude.json","r",encoding="utf-8") as arquivo:
        postos = json.load(arquivo)
    verificar_bd = session.exec(select(Postos)).first()
    if verificar_bd:
        return
    for posto in postos:
        novo_posto = Postos(nome_oficial=posto["nome_oficial"], endereco=posto["endereco"], bairro=posto["bairro"], fone=posto["fone"], servico=posto["servico"], especialidade=posto["especialidade"], como_usar=posto["como_usar"], horario=posto["horario"], latitude=posto["latitude"], longitude=posto["longitude"])
        session.add(novo_posto)
    session.commit()