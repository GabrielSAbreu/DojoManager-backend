from fastapi import FastAPI, HTTPException, status
from typing import List
from model import Session
from fastapi.middleware.cors import CORSMiddleware
from routes import modalidade_router, usuario_router, pratica_router

app = FastAPI()

origins = ["*"]  # Permitir todas as origens afim de facilitar o teste local

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(modalidade_router)
app.include_router(usuario_router)
app.include_router(pratica_router)
