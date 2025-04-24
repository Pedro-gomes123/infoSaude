from fastapi import FastAPI, HTTPException
from modelos import Postos, ListarPosto
from bancodedados import SessionDep, criar_bd
from sqlmodel import select, Session, engine
import json
from haversine import haversine, Unit

app = FastAPI()

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

@app.on_event("startup")
def inicializa():
    criar_bd()
    with Session(engine) as session:
        migrar_postos(session)


@app.get("/postos/", response_model=list[ListarPosto])
def listar_postos(session: SessionDep) -> list[Postos]:
    postos = session.exec(select(Postos)).all()
    return postos

@app.get("/postos/{id_posto}")
def listar_posto(id_posto: int, session: SessionDep) -> Postos:
    posto = session.get(Postos, id_posto)
    if not posto:
        raise HTTPException(status_code=404, detail="Posto não encontrado")
    return posto

@app.get("/postos/proximos", response_model=ListarPosto)
def postos_proximos(latitude:float, longitude:float, session:SessionDep) -> Postos:
    postos = session.exec(select(Postos)).all()
    coordenada_usuario = (latitude, longitude)
    menor_distancia = 1000
    for posto in postos:
        distancia = haversine(coordenada_posto, coordenada_usuario, unit=Unit.KILOMETERS)
        coordenada_posto = (posto["latitude"], posto["longitude"])
        if  distancia < menor_distancia:
            menor_distancia = distancia
            posto_proximo = posto

    return posto_proximo


