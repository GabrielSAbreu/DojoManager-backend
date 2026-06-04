from fastapi import FastAPI
from model import Session

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Esse é o Dojo Manager API! EM CONSTRUÇÃO! OSS!"}
