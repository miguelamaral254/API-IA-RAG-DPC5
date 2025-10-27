from fastapi import FastAPI
from app.routers import rag, classification

app = FastAPI(title="Delegacia 5.0 - IA API")

# Inclui os roteadores modulares
app.include_router(rag.router, tags=["RAG"])
app.include_router(classification.router, tags=["Classification"])

@app.get("/")
def read_root():
    return {"status": "IA API está online"}