from pydantic import BaseModel, Field
from datetime import date
from schema.usuario import UsuarioResponse
from schema.modalidade import ModalidadeResponse


class PraticaCreate(BaseModel):
    fk_usuario_id_usuario: int = Field(..., example=1)
    fk_modalidade_id: int = Field(..., example=1)


class PraticaResponse(BaseModel):
    fk_usuario_id_usuario: int
    fk_modalidade_id: int
    data_inicio_modalidade: date
    usuario: UsuarioResponse
    modalidade: ModalidadeResponse

    class Config:
        from_attributes = True
