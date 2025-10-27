from fastapi import APIRouter, HTTPException
from app.schemas.models import QueryRequest, ClassifyResponse
from app.core.chains import get_classification_chain

router = APIRouter()

@router.post("/classify", response_model=ClassifyResponse)
async def classify_intent_endpoint(request: QueryRequest):
    """
    Recebe uma pergunta e classifica a intenção.
    """
    try:
        classification_chain = get_classification_chain()
        # O .strip() remove espaços em branco que o LLM pode retornar
        intent = classification_chain.invoke(request.query).strip()
        return {"intent": intent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))