from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker

from model.base import Base

# Gerar o banco de dados na pasta database
db = create_engine("sqlite:///database/dojomanager.db")

Session = sessionmaker(bind=db)
session = Session()


# Cria as tabelas no banco de dados
Base.metadata.create_all(db)
