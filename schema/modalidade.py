from pydantic import BaseModel, Field


class ModalidadeCreate(BaseModel):
    nome_modalidade: str = Field(..., min_length=2, max_length=50, example="Jiu-jitsu")


class ModalidadeResponse(BaseModel):
    id_modalidade: int
    nome_modalidade: str

    class Config:
        from_attributes = True
