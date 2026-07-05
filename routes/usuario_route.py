from fastapi import APIRouter, HTTPException, status
from typing import List
from model import Session
from model.usuario import Usuario
from schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


# 1. Criar novo usuário
@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_dados: UsuarioCreate):
    """
    Cria um novo usuário no sistema.
    """
    session = Session()
    try:
        if usuario_dados.email:
            email_existente = (
                session.query(Usuario)
                .filter(Usuario.email == usuario_dados.email)
                .first()
            )
            if email_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"O e-mail '{usuario_dados.email}' já está cadastrado.",
                )

        novo_usuario = Usuario(
            nome=usuario_dados.nome,
            email=usuario_dados.email,
            telefone=usuario_dados.telefone,
            tipo_usuario=usuario_dados.tipo_usuario,
            data_nascimento=usuario_dados.data_nascimento,
        )

        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        return novo_usuario
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao salvar usuário: {str(e)}",
        )
    finally:
        session.close()


# 2. Listar todos os usuários
@router.get("", response_model=List[UsuarioResponse])
def listar_usuarios():
    """
    Lista todos os usuários cadastrados.
    """
    session = Session()
    try:
        usuarios = session.query(Usuario).all()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao listar usuários: {str(e)}",
        )
    finally:
        session.close()


# 3. Obter usuário por ID
@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obter_usuario(id_usuario: int):
    """
    Exibe os dados de um usuário pelo ID informado.
    """
    session = Session()
    try:
        usuario = (
            session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )

        return usuario
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar usuário: {str(e)}",
        )
    finally:
        session.close()


# 4. Editar usuário (PUT)
@router.put("/{id_usuario}", response_model=UsuarioResponse)
def editar_usuario(id_usuario: int, usuario_dados: UsuarioCreate):
    """
    Atualiza os dados de um usuário existente com base no ID informado.
    """
    session = Session()
    try:
        usuario = (
            session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado para atualização.",
            )

        usuario.nome = usuario_dados.nome
        usuario.email = usuario_dados.email
        usuario.telefone = usuario_dados.telefone
        usuario.tipo_usuario = usuario_dados.tipo_usuario
        usuario.data_nascimento = usuario_dados.data_nascimento

        session.commit()
        session.refresh(usuario)
        return usuario
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao atualizar usuário: {str(e)}",
        )
    finally:
        session.close()


# 5. Deletar usuário (DELETE)
@router.delete("/{id_usuario}", status_code=status.HTTP_200_OK)
def deletar_usuario(id_usuario: int):
    """
    Remove um usuário cadastrado com base no ID informado.
    """
    session = Session()
    try:
        usuario = (
            session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado para exclusão.",
            )

        nome_deletado = usuario.nome
        session.delete(usuario)
        session.commit()
        return {nome_deletado: "Usuário deletado com sucesso"}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao excluir usuário: {str(e)}",
        )
    finally:
        session.close()
