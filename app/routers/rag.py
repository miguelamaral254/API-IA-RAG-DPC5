from fastapi import APIRouter, HTTPException
from app.schemas.models import QueryRequest, RagResponse
from app.core.chains import get_rag_chain

router = APIRouter()

@router.post("/query/rag", response_model=RagResponse)
async def query_rag_endpoint(request: QueryRequest):
    """
    Recebe uma pergunta e responde usando RAG (para Dicas, Localização, etc.).
    """
    try:
        rag_chain = get_rag_chain()
        answer = rag_chain.invoke(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))