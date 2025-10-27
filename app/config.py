from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Carrega o .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    # Banco de Dados
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    # PGVector
    COLLECTION_NAME: str

    # Ollama
    OLLAMA_BASE_URL: str
    LLM_MODEL_NAME: str

    def get_db_connection_string(self) -> str:
        """Retorna a string de conexão do DB."""
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

@lru_cache()
def get_settings() -> Settings:
    """Retorna a instância das configurações."""
    return Settings()

# Instância única para ser importada por outros módulos
settings = get_settings()