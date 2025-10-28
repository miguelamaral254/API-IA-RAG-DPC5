# --- Imports Atualizados ---
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.vectorstore import get_retriever
from app.config import settings

def get_llm():
    """Inicializa e retorna o LLM."""
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME
        )

def get_rag_chain():
    """Cria e retorna a chain de RAG."""
    retriever = get_retriever()
    llm = get_llm()
    
    
    rag_template = """
    Você é um assistente da Polícia Civil de Pernambuco. 
    Responda a pergunta do usuário APENAS com base no contexto fornecido.
    Se a informação não estiver no contexto, diga 'Desculpe, não tenho essa informação.'

    Contexto:
    {context}

    Pergunta:
    {question}
    """
    rag_prompt = ChatPromptTemplate.from_template(rag_template)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def get_classification_chain():
    """Cria e retorna a chain de Classificação de Intenção."""
    llm = get_llm()
    
    classification_template = """
    Sua tarefa é classificar a intenção do usuário.
    Responda APENAS com UMA das seguintes intenções: 
    [registrar_bo, localizar_unidade, dicas_seguranca, consultar_status_bo, saudacao, despedida, fallback]

    Texto do Usuário:
    {query}
    """
    classification_prompt = ChatPromptTemplate.from_template(classification_template)
    
    classification_chain = (
        classification_prompt
        | llm
        | StrOutputParser()
    )
    return classification_chain