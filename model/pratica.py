from model.base import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey


class Pratica(Base):
    __tablename__ = "pratica"

    fk_usuario_id_usuario = Column(
        Integer, ForeignKey("usuarios.id_usuario"), nullable=False, primary_key=True
    )
    fk_modalidade_id = Column(
        Integer,
        ForeignKey("modalidades.id_modalidade"),
        nullable=False,
        primary_key=True,
    )
    data_inicio_modalidade = Column(Date, nullable=False)
