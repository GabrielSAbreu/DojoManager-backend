# from fastapi import APIRouter, HTTPException, status
# from typing import List
# from model import Session
# from datetime import date
# from model.pratica import Pratica
# from model.usuario import Usuario
# from model.modalidade import Modalidade
# from schema import PraticaCreate, PraticaResponse

# router = APIRouter(prefix="/praticas", tags=["Pratica"])


# # 1. Vincular Aluno a uma Modalidade (Criar Prática)
# @router.post("", response_model=PraticaResponse, status_code=status.HTTP_201_CREATED)
# def criar_pratica(pratica_dados: PraticaCreate):
#     session = Session()
#     try:
#         # Validação 1: O usuário existe?
#         usuario_existente = (
#             session.query(Usuario)
#             .filter(Usuario.id_usuario == pratica_dados.fk_usuario_id_usuario)
#             .first()
#         )
#         if not usuario_existente:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Usuário com ID {pratica_dados.fk_usuario_id_usuario} não encontrado.",
#             )

#         # Validação 2: A modalidade existe?
#         modalidade_existente = (
#             session.query(Modalidade)
#             .filter(Modalidade.id_modalidade == pratica_dados.fk_modalidade_id)
#             .first()
#         )
#         if not modalidade_existente:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Modalidade com ID {pratica_dados.fk_modalidade_id} não encontrada.",
#             )

#         # Validação 3: O aluno já está matriculado nessa modalidade? (Evitar duplicidade na chave composta)
#         vinculo_existente = (
#             session.query(Pratica)
#             .filter(
#                 Pratica.fk_usuario_id_usuario == pratica_dados.fk_usuario_id_usuario,
#                 Pratica.fk_modalidade_id == pratica_dados.fk_modalidade_id,
#             )
#             .first()
#         )

#         if vinculo_existente:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"O usuário '{usuario_existente.nome}' ya está matriculado na modalidade '{modalidade_existente.nome_modalidade}'.",
#             )

#         # Se passou em todas as checagens, cria o registro gerando a data atual automaticamente
#         nova_pratica = Pratica(
#             fk_usuario_id_usuario=pratica_dados.fk_usuario_id_usuario,
#             fk_modalidade_id=pratica_dados.fk_modalidade_id,
#             data_inicio_modalidade=date.today(),  # Back-end assumindo o controle da data
#         )

#         session.add(nova_pratica)
#         session.commit()
#         session.refresh(nova_pratica)
#         return nova_pratica

#     except HTTPException as http_err:
#         raise http_err
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro interno ao matricular aluno: {str(e)}",
#         )
#     finally:
#         session.close()


# # 2. Listar todos os vínculos (Quem pratica o quê)
# @router.get("", response_model=List[PraticaResponse])
# def listar_praticas():
#     session = Session()
#     try:
#         # Graças ao relationship, o SQLAlchemy já traz os dados do usuário e modalidade aninhados
#         praticas = session.query(Pratica).all()
#         return praticas
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro interno ao listar práticas: {str(e)}",
#         )
#     finally:
#         session.close()


# # 3. Remover Vínculo (Desmatricular Aluno de uma Modalidade)
# @router.delete(
#     "/usuario/{fk_usuario_id_usuario}/modalidade/{fk_modalidade_id}",
#     status_code=status.HTTP_200_OK,
# )
# def deletar_pratica(fk_usuario_id_usuario: int, fk_modalidade_id: int):
#     session = Session()
#     try:
#         # Localiza a linha exata combinando a chave composta
#         pratica = (
#             session.query(Pratica)
#             .filter(
#                 Pratica.fk_usuario_id_usuario == fk_usuario_id_usuario,
#                 Pratica.fk_modalidade_id == fk_modalidade_id,
#             )
#             .first()
#         )

#         if not_pratica:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Matrícula/Vínculo não encontrado para exclusão.",
#             )

#         # Armazena os nomes para um retorno amigável antes de deletar
#         nome_aluno = práticа.usuario.nome
#         nome_mod = práticа.modalidade.nome_modalidade

#         session.delete(pratica)
#         session.commit()

#         return {
#             "message": f"Aluno '{nome_aluno}' desvinculado com sucesso da modalidade '{nome_mod}'."
#         }

#     except HTTPException as http_err:
#         raise http_err
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro interno ao remover matrícula: {str(e)}",
#         )
#     finally:
#         session.close()

from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import date
from model import Session
from model.pratica import Pratica
from model.usuario import Usuario
from model.modalidade import Modalidade
from schema.pratica import PraticaCreate, PraticaResponse

# IMPORTANTE: Importar o joinedload do SQLAlchemy
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/praticas", tags=["Práticas"])


# 1. Vincular Aluno a uma Modalidade (POST)
@router.post("", response_model=PraticaResponse, status_code=status.HTTP_201_CREATED)
def criar_pratica(pratica_dados: PraticaCreate):
    session = Session()
    try:
        # Validação 1: O usuário existe?
        usuario_existente = (
            session.query(Usuario)
            .filter(Usuario.id_usuario == pratica_dados.fk_usuario_id_usuario)
            .first()
        )
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )

        # Validação 2: A modalidade existe?
        modalidade_existente = (
            session.query(Modalidade)
            .filter(Modalidade.id_modalidade == pratica_dados.fk_modalidade_id)
            .first()
        )
        if not modalidade_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modalidade não encontrada.",
            )

        # Validação 3: Evitar duplicidade
        vinculo_existente = (
            session.query(Pratica)
            .filter(
                Pratica.fk_usuario_id_usuario == pratica_dados.fk_usuario_id_usuario,
                Pratica.fk_modalidade_id == pratica_dados.fk_modalidade_id,
            )
            .first()
        )
        if vinculo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já matriculado nesta modalidade.",
            )

        # Criação do registro
        nova_pratica = Pratica(
            fk_usuario_id_usuario=pratica_dados.fk_usuario_id_usuario,
            fk_modalidade_id=pratica_dados.fk_modalidade_id,
            data_inicio_modalidade=date.today(),
        )
        session.add(nova_pratica)
        session.commit()

        # O PULO DO GATO: Em vez de usar apenas session.refresh(), fazemos uma busca explicativa
        # trazendo os dados do usuário e modalidade via JOIN de forma ultra segura antes de fechar a sessão
        resultado = (
            session.query(Pratica)
            .options(joinedload(Pratica.usuario), joinedload(Pratica.modalidade))
            .filter(
                Pratica.fk_usuario_id_usuario == nova_pratica.fk_usuario_id_usuario,
                Pratica.fk_modalidade_id == nova_pratica.fk_modalidade_id,
            )
            .first()
        )

        return resultado

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )
    finally:
        session.close()


# 2. Listar todos os vínculos (GET)
@router.get("", response_model=List[PraticaResponse])
def listar_praticas():
    session = Session()
    try:
        # Adicionado o joinedload aqui também para garantir a resposta rica na listagem
        praticas = (
            session.query(Pratica)
            .options(joinedload(Pratica.usuario), joinedload(Pratica.modalidade))
            .all()
        )
        return praticas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )
    finally:
        session.close()
