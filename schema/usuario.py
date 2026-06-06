from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional
from model.usuario import TipoUsuario


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50, example="João Silva")
    email: Optional[EmailStr] = None
    telefone: str = Field(..., min_length=8, max_length=20, example="51999998888")
    tipo_usuario: TipoUsuario = Field(..., example="aluno")
    data_nascimento: date = Field(..., example="2010-05-15")

    @field_validator("email", mode="before")
    @classmethod
    def tratar_email_vazio(cls, v):
        # Se o usuário digitou uma string vazia "" ou cheia de espaços, transforma em None
        if isinstance(v, str) and v.strip() == "":
            return None
        return v


class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    email: Optional[str]
    telefone: str
    tipo_usuario: TipoUsuario
    data_nascimento: date

    class Config:
        from_attributes = True
