from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional
from model.usuario import TipoUsuario


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50, example="João Silva")
    email: Optional[EmailStr] = Field(None, example="joao@email.com")
    telefone: str = Field(..., min_length=8, max_length=20, example="51999998888")
    tipo_usuario: TipoUsuario = Field(..., example="aluno")
    data_nascimento: date = Field(..., example="2010-05-15")


class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    email: Optional[str]
    telefone: str
    tipo_usuario: TipoUsuario
    data_nascimento: date

    class Config:
        from_attributes = True
