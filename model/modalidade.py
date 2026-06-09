from model.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Modalidade(Base):
    __tablename__ = "modalidades"

    id_modalidade = Column(Integer, primary_key=True, autoincrement=True)
    nome_modalidade = Column(String(50), nullable=False)

    usuarios = relationship("Usuario", secondary="pratica", back_populates="modalidade")
    praticas = relationship(
        "Pratica", back_populates="modalidade", cascade="all,delete-orphan"
    )

    def __init__(self, nome_modalidade):
        self.nome_modalidade = nome_modalidade
