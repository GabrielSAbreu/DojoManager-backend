from fastapi import FastAPI, HTTPException, status
from typing import List
from model import Session
from model.modalidade import Modalidade
from schema import ModalidadeCreate, ModalidadeResponse, UsuarioCreate, UsuarioResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Esse é o Dojo Manager API! EM CONSTRUÇÃO! OSS!"}


# Enpoints para Modalidade


# Criar nova modalidade
@app.post("/modalidades")
def criar_modalidade(modalidade_dados: ModalidadeCreate):
    session = Session()

    modalidade_existente = (
        session.query(Modalidade)
        .filter(Modalidade.nome_modalidade == modalidade_dados.nome_modalidade)
        .first()
    )
    # Se já existir a modalidade, encerra session e retorna erro 400
    if modalidade_existente:
        session.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A modalidade '{modalidade_dados.nome_modalidade}' já está cadastrada.",
        )

    nova_modalidade = Modalidade(nome_modalidade=modalidade_dados.nome_modalidade)

    session.add(nova_modalidade)
    session.commit()
    session.refresh(nova_modalidade)

    session.close()

    return nova_modalidade


# Listar todas as modalidades
@app.get("/modalidades", response_model=List[ModalidadeResponse])
def listar_modalidades():
    session = Session()
    modalidades = session.query(Modalidade).all()
    session.close()
    return modalidades


# Listar modalidade por ID
@app.get("/modalidades/{id_modalidade}")
def obter_modalidade(id_modalidade: int):
    session = Session()
    modalidade = (
        session.query(Modalidade)
        .filter(Modalidade.id_modalidade == id_modalidade)
        .first()
    )
    session.close()

    if not modalidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Modalidade não encontrada"
        )

    return modalidade


# Editar modalidade (PUT)
@app.put("/modalidades/{id_modalidade}")
def editar_modalidade(id_modalidade: int, modalidade_dados: ModalidadeCreate):
    session = Session()

    modalidade = (
        session.query(Modalidade)
        .filter(Modalidade.id_modalidade == id_modalidade)
        .first()
    )

    # Se não existir, encerra session e retorna erro 404
    if not modalidade:
        session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Modalidade não encontrada para atualização",
        )

    modalidade.nome_modalidade = modalidade_dados.nome_modalidade

    session.commit()
    session.refresh(modalidade)
    session.close()

    return modalidade


# Deletar modalidade (DELETE)
# @app.delete("/modalidades/{id_modalidade}", status_code=status.HTTP_204_NO_CONTENT)
@app.delete("/modalidades/{id_modalidade}", status_code=status.HTTP_200_OK)
def deletar_modalidade(id_modalidade: int):
    session = Session()

    modalidade = (
        session.query(Modalidade)
        .filter(Modalidade.id_modalidade == id_modalidade)
        .first()
    )

    if not modalidade:
        session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Modalidade não encontrada para exclusão",
        )

    session.delete(modalidade)
    session.commit()
    session.close()

    return {modalidade.nome_modalidade: "Modalidade deletada com sucesso"}
