from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.vectorstore import get_retriever
from app.config import settings

def get_llm():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL
        )

def get_rag_chain():
    retriever = get_retriever()
    llm = get_llm()
    personality = settings.AGENT_PERSONALITY
    rag_template = f"""
{personality}

Contexto:
{{context}}

Pergunta:
{{question}}
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
    # ... (sem mudanças aqui)
    llm = get_llm()
    
    classification_template = """
    Sua tarefa é classificar a intenção do usuário.
    Responda APENAS com UMA das seguintes intenções: 
    [registrar_bo, consultar_status_bo, localizar_unidade, dicas_seguranca, denuncia_online, agendamento, saudacao, despedida, fallback]

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