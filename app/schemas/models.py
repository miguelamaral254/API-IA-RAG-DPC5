from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class RagResponse(BaseModel):
    answer: str

class ClassifyResponse(BaseModel):
    intent: str