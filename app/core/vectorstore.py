from langchain_postgres.vectorstores import PGVector
from langchain_ollama.embeddings import OllamaEmbeddings
from app.config import settings

def get_embeddings():
    """Inicializa e retorna o modelo de embeddings."""
    return OllamaEmbeddings(
        model=settings.LLM_MODEL_NAME,
        base_url=settings.OLLAMA_BASE_URL
    )

# DEPOIS (CORRETO)
def get_vector_store() -> PGVector:
    """Inicializa e retorna o VectorStore PGVector."""
    return PGVector(
        collection_name=settings.COLLECTION_NAME,
        connection=settings.get_db_connection_string(),
        embeddings=get_embeddings(), # <== CORRIGIDO
    )
def get_retriever():
    """Retorna o retriever do VectorStore."""
    return get_vector_store().as_retriever()