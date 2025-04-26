from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from modelos import Postos, ListarPosto
from bancodedados import SessionDep, criar_bd, engine
from sqlmodel import select, Session
import json
from haversine import haversine, Unit
from fastapi.responses import HTMLResponse
import folium

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def float_none(valor):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None

def migrar_postos(session: SessionDep):
    with open("postos_saude.json","r",encoding="utf-8") as arquivo:
        postos = json.load(arquivo)
    verificar_bd = session.exec(select(Postos)).first()
    if verificar_bd:
        return
    for posto in postos:
        novo_posto = Postos(nome_oficial=posto["nome_oficial"], endereco=posto["endereco"], bairro=posto["bairro"], fone=posto["fone"], servico=posto["servico"], especialidade=posto["especialidade"], como_usar=posto["como_usar"], horario=posto["horario"], latitude=float_none(posto["latitude"]), longitude=float_none(posto["longitude"]))
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

@app.get("/postos/proximos/", response_model=ListarPosto)
def postos_proximos(latitude:float, longitude:float, session:SessionDep) -> Postos:
    postos = session.exec(select(Postos)).all()
    coordenada_usuario = (latitude, longitude)
    menor_distancia = float("inf")
    posto_proximo = None
    for posto in postos:
        if posto.latitude is None or posto.longitude is None:
            continue
        coordenada_posto = (posto.latitude, posto.longitude)
        distancia = haversine(coordenada_posto, coordenada_usuario, unit=Unit.KILOMETERS)
        if  distancia < menor_distancia:
            menor_distancia = distancia
            posto_proximo = posto
    if posto_proximo is None:
        raise HTTPException(status_code=404, detail="Nenhum posto encontrado")
    return posto_proximo

@app.get("/postos/filtrar", response_model=list[ListarPosto])
def filtrar_postos(session: SessionDep, bairro: str = None, servico: str = None, especialidade: str = None) -> list[Postos]:
    postos = session.exec(select(Postos)).all()
    postos_filtrados = postos
    if bairro is not None:
        postos_filtrados = [posto for posto in postos if posto.bairro == bairro]
    if servico is not None:
        postos_filtrados = [posto for posto in postos if posto.servico == servico]
    if especialidade is not None:
        postos_filtrados = [posto for posto in postos if especialidade in posto.especialidade]

    return postos_filtrados


@app.get("/mapa_postos/", response_class=HTMLResponse)
def mapear_postos(session: SessionDep):
    postos = session.exec(select(Postos)).all()
    mapa = folium.Map([-8.0539, -34.8808], tiles="OpenStreetMap", zoom_start=14)
    for posto in postos:
        if posto.latitude is not None and posto.longitude is not None:      
            latitude = float(posto.latitude)
            longitude = float(posto.longitude)
            coordenada_posto = [latitude, longitude]
            popup_html = f""" 
                <h3>{posto.nome_oficial}</h3>
                <p>Endereço: {posto.endereco}</p>
                <p>Telefone: {posto.fone}</p>
                <p>Especialidade: {posto.especialidade}</p>
                <p>Horario: {posto.horario}</p>
                """
            folium.Marker(
                location=coordenada_posto,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip= posto.nome_oficial,
                icon=folium.Icon(color="red", icon="plus-sign")
            ).add_to(mapa)

    return mapa._repr_html_()



