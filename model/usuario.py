from model.base import Base
from sqlalchemy import Column, Integer, String, Date, Enum
import enum
from sqlalchemy.orm import relationship


class TipoUsuario(enum.Enum):
    aluno = "aluno"
    professor = "professor"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True, unique=True)
    telefone = Column(String(20), nullable=False)
    tipo_usuario = Column(Enum(TipoUsuario), nullable=False)
    data_nascimento = Column(Date, nullable=False)

    modalidades = relationship(
        "Modalidade", secondary="pratica", back_populates="usuarios"
    )

    def __init__(self, nome, email, telefone, tipo_usuario, data_nascimento):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.tipo_usuario = tipo_usuario
        self.data_nascimento = data_nascimento
