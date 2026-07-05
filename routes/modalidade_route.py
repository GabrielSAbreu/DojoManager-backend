from fastapi import APIRouter, HTTPException, status
from typing import List
from model import Session
from model.modalidade import Modalidade
from schema import ModalidadeCreate, ModalidadeResponse

router = APIRouter(prefix="/modalidades", tags=["Modalidades"])


# 1. Criar nova modalidade
@router.post("", response_model=ModalidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_modalidade(modalidade_dados: ModalidadeCreate):
    """
    Cria nova modalidade

    Necessário cadastrar a modalidade através de uma string
    """
    session = Session()
    try:
        modalidade_existente = (
            session.query(Modalidade)
            .filter(Modalidade.nome_modalidade == modalidade_dados.nome_modalidade)
            .first()
        )

        if modalidade_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A modalidade '{modalidade_dados.nome_modalidade}' já está cadastrada.",
            )

        nova_modalidade = Modalidade(nome_modalidade=modalidade_dados.nome_modalidade)
        session.add(nova_modalidade)
        session.commit()
        session.refresh(nova_modalidade)
        return nova_modalidade

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao salvar a modalidade: {str(e)}",
        )
    finally:
        session.close()


# 2. Listar todas as modalidades
@router.get("", response_model=List[ModalidadeResponse])
def listar_modalidades():
    """
    Lista todas as modalidades cadastradas
    """
    session = Session()
    try:
        modalidades = session.query(Modalidade).all()
        return modalidades
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao listar modalidades: {str(e)}",
        )
    finally:
        session.close()


# 3. Listar modalidade por ID
@router.get("/{id_modalidade}", response_model=ModalidadeResponse)
def obter_modalidade(id_modalidade: int):
    """
    Exibe modalidade pelo ID
    """
    session = Session()
    try:
        modalidade = (
            session.query(Modalidade)
            .filter(Modalidade.id_modalidade == id_modalidade)
            .first()
        )

        if not modalidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modalidade não encontrada.",
            )

        return modalidade
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar modalidade: {str(e)}",
        )
    finally:
        session.close()


# 4. Editar modalidade (PUT)
@router.put("/{id_modalidade}", response_model=ModalidadeResponse)
def editar_modalidade(id_modalidade: int, modalidade_dados: ModalidadeCreate):
    """
    Atualiza os dados de uma modalidade existente com base no ID informado.
    """
    session = Session()
    try:
        modalidade = (
            session.query(Modalidade)
            .filter(Modalidade.id_modalidade == id_modalidade)
            .first()
        )

        if not modalidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modalidade não encontrada para atualização.",
            )

        modalidade.nome_modalidade = modalidade_dados.nome_modalidade
        session.commit()
        session.refresh(modalidade)
        return modalidade
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao atualizar modalidade: {str(e)}",
        )
    finally:
        session.close()


# 5. Deletar modalidade (DELETE)
@router.delete("/{id_modalidade}", status_code=status.HTTP_200_OK)
def deletar_modalidade(id_modalidade: int):
    """
    Remove uma modalidade cadastrada com base no ID informado.
    """
    session = Session()
    try:
        modalidade = (
            session.query(Modalidade)
            .filter(Modalidade.id_modalidade == id_modalidade)
            .first()
        )

        if not modalidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modalidade não encontrada para exclusão.",
            )

        nome_deletado = modalidade.nome_modalidade
        session.delete(modalidade)
        session.commit()
        return {nome_deletado: "Modalidade deletada com sucesso"}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao excluir modalidade: {str(e)}",
        )
    finally:
        session.close()
