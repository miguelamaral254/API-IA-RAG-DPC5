import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredFileLoader
)

def load_documents_from_directory(directory_path: str) -> list:
    """
    Carrega todos os documentos suportados (txt, pdf, docx) de um diretório.
    """
    documents = []
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if not os.path.isfile(file_path):
            continue

        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
            else:
                print(f"Arquivo não suportado: {filename}")
        
        except Exception as e:
            print(f"Erro ao carregar o arquivo {filename}: {e}")

    return documents