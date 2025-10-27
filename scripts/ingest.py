import sys
import os

# Adiciona o diretório raiz ao path para encontrar o módulo 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector
from app.config import settings
from app.core.vectorstore import get_embeddings
from scripts.loaders import load_documents_from_directory

DATA_PATH = "./data"

def ingest_data():
    """Processa e insere os dados no PGVector."""
    
    # 1. Carregar documentos de PDF, DOCX, TXT
    print(f"Carregando documentos do diretório: {DATA_PATH}...")
    documents = load_documents_from_directory(DATA_PATH)
    
    if not documents:
        print("Nenhum documento encontrado para ingerir.")
        return

    print(f"{len(documents)} documentos carregados.")

    # 2. Dividir Documentos em "Chunks"
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    if not chunks:
        print("Nenhum 'chunk' foi criado após a divisão.")
        return

    print(f"{len(chunks)} chunks criados. Iniciando ingestão no PGVector...")

    # 3. Inserir no PGVector
    embeddings = get_embeddings()
    
    # DEPOIS (CORRETO)
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        collection_name=settings.COLLECTION_NAME,
        connection=settings.get_db_connection_string(), # <== CORRIGIDO
        pre_delete_collection=True 
    )
    print("Ingestão concluída!")

if __name__ == "__main__":
    # Verifica se a pasta 'data' existe
    if not os.path.exists(DATA_PATH):
        print(f"Erro: Diretório '{DATA_PATH}' não encontrado.")
        print("Por favor, crie o diretório e adicione seus arquivos .pdf, .docx ou .txt.")
        sys.exit(1)
        
    try:
        # Testa a conexão com Ollama antes de começar
        get_embeddings().embed_query("teste de conexão")
    except Exception as e:
        print("Erro ao conectar ao Ollama. Verifique se ele está rodando.")
        print(f"Erro: {e}")
        sys.exit(1)
        
    ingest_data()