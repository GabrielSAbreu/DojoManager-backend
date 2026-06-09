from fastapi import FastAPI, HTTPException, status
from typing import List
from model import Session

# from model.modalidade import Modalidade
# from schema import ModalidadeCreate, ModalidadeResponse, UsuarioCreate, UsuarioResponse
from routes import modalidade_router, usuario_router, pratica_router

app = FastAPI()

app.include_router(modalidade_router)
app.include_router(usuario_router)
app.include_router(pratica_router)
