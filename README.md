# Projeto Delegacia 5.0: Microserviço de IA (RAG)

Este repositório contém o **Microserviço de IA** para o projeto "Delegacia 5.0 – Chatbot Humanizado".

Este serviço é o "cérebro" do chatbot e é responsável por duas tarefas principais:
1.  **Classificação de Intenção:** Entender o que o usuário deseja fazer (ex: `registrar_bo`, `localizar_unidade`).
2.  **Geração de Resposta (RAG):** Buscar informações em uma base de conhecimento (documentos `.pdf`, `.txt`, `.docx`) para responder perguntas sobre dicas de segurança, localização de delegacias, etc.

Este serviço foi construído para ser consumido por um **Orquestrador de Chat** (ex: um servidor Node.js com WebSocket), desacoplando a lógica de IA dos canais de comunicação.

---

## 1. Instalação e Configuração (Passo a Passo)

Siga os passos abaixo para configurar e executar este serviço localmente.

### Pré-requisitos

* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/products/docker-desktop/) e **Docker Compose**
* [Python 3.11+](https://www.python.org/downloads/)
* Uma conta gratuita no **[Groq](https://groq.com/)** para obter uma API Key.

### Passo 1: Clonar o Repositório

```bash
git clone [https://github.com/miguelamaral254/API-IA-RAG-DPC5.git](https://github.com/miguelamaral254/API-IA-RAG-DPC5.git)
````
````bash
cd API-IA-RAG-DPC5
````

### Passo 2: Configurar o Ambiente (`.env`)

Crie um arquivo chamado `.env` na raiz desta pasta (`API-IA-RAG-DPC5`). Copie e cole o conteúdo abaixo, substituindo os valores `...` pelos seus.

**Arquivo `.env` (use como modelo para seu `.env`)**

```ini
# Configurações do Banco de Dados (para scripts locais)
DATABASE_HOST=localhost
DATABASE_PORT=5433
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_NAME=delegacia_db

# Configuração do PGVector
COLLECTION_NAME=delegacia_docs

# Configuração do Ollama (Embeddings Locais)
# Usado para vetorizar os documentos (Etapa 1 do RAG)
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=phi3:mini

# Configuração do Groq (Chat/Geração Online)
# Usado para "pensar" e gerar as respostas (Etapa 2 do RAG)
GROQ_API_KEY=gsk_SUA_CHAVE_API_DO_GROQ_AQUI
```

**Nota de Segurança:** Adicione `.env` ao seu arquivo `.gitignore` para nunca comitar suas chaves secretas\!

### Passo 3: Iniciar os Serviços de Dependência (Docker)

O banco de dados e o servidor de *embeddings* (Ollama) rodam via Docker.

```bash
# 1. Inicie o banco (db) e o ollama (na pasta raiz do projeto)
docker-compose up -d db ollama

# 2. Baixe o modelo de embedding (phi3:mini) para dentro do container ollama
# (Isso só precisa ser feito uma vez)
docker-compose exec ollama ollama pull phi3:mini
```

### Passo 4: Configurar o Ambiente Python

Este serviço roda localmente em um ambiente virtual (`venv`) para desenvolvimento.

```bash
# 1. Crie a venv (ambiente virtual)
python3 -m venv venv

# 2. Ative a venv
source venv/bin/activate

# 3. Instale todas as dependências do Python
pip install -r requirements.txt
```

-----

## 2\. Como Usar

Com o ambiente configurado, siga estes passos para rodar a API.

### Passo 5: Alimentar o RAG (Ingestão de Dados)

O RAG precisa "aprender" com seus documentos.

1.  **Adicione seus arquivos (`.pdf`, `.docx`, `.txt`) na pasta `/data`.**
2.  Execute o script de ingestão (com a `venv` ativa):

<!-- end list -->

```bash
# O script vai ler a pasta /data, vetorizar os arquivos (usando o Ollama)
# e salvar tudo no banco de dados pgvector.
python scripts/ingest.py
```

**Saída Esperada:** `Ingestão concluída!`

### Passo 6: Executar a API

Com as dependências rodando (Docker) e o banco alimentado (Ingestão), inicie o servidor FastAPI:

```bash
# (Com a venv ativa)
uvicorn app.main:app --reload --port 8001
```

O servidor estará disponível em `http://127.0.0.1:8001`.

-----

## 3\. Arquitetura e Stack Tecnológica

### Diagrama da Arquitetura Completa

O diagrama abaixo ilustra o fluxo de dados desde o usuário (front-end) até os back-ends de processamento e integração:

````mermaid
graph TD
    subgraph "Usuário"
        F["🌐 Frontend (React)"]
    end

    subgraph "Servidor de Chat (Orquestrador)"
        WS["🚀 Orquestrador (Node.js + WebSocket)"]
    end

    subgraph "Microsserviços de Backend"
        NLP["🧠 API de IA - RAG <br/> Python/FastAPI <br/> <b>[Este Repositório]</b>"]
        BO_API["📋 API de Ações - BO <br/> Node.js/Express"]
    end

    subgraph "Bancos de Dados (Docker)"
        DB["🐘 PostgreSQL"]
        PGVEC["Vector<br/>pgvector"]
    end

    subgraph "Serviços Externos"
        GROQ["⚡️ Groq API (LLM Rápido)"]
        OLLAMA["🤖 Ollama (Embeddings)"]
    end

    %% -- Fluxo de Chat (RAG) --
    F <-->|"1. Envia Msg (Socket)"| WS
    WS -->|"2. Classifica Intaenção"| NLP
    NLP -->|"3. Chama LLM (Geração)"| GROQ
    GROQ -->|"4. Retorna Intenção"| NLP
    NLP -->|"5. Retorna Intenção"| WS
    WS -->|"6. Pede Resposta (RAG)"| NLP
    NLP -->|"7. Vetoriza Pergunta"| OLLAMA
    NLP -->|"8. Busca no Vetor"| PGVEC
    PGVEC -->|"9. Retorna Contexto"| NLP
    NLP -->|"10. Gera Resposta (LLM)"| GROQ
    GROQ -->|"11. Retorna Resposta"| NLP
    NLP -->|"12. Retorna Resposta"| WS
    WS -->|"13. Envia Resposta (Socket)"| F

    %% -- Fluxo de Ação (BO) --
    WS -->|"Comando: Abrir Modal"| F
    F -->|"Envia Dados (Form via REST/POST)"| BO_API
    BO_API -->|"Salva no Banco"| DB
````

### Stack Tecnológica (Este Serviço: API-IA-RAG)

  * **Linguagem:** Python 3.11+
  * **Framework:** FastAPI
  * **Orquestração de IA:** LangChain
  * **LLM (Geração/Classificação):** Groq API (ex: `llama-3.1-70b-versatile`) - Rápido, via API.
  * **Embeddings (Vetorização):** Ollama (ex: `phi3:mini`) - Gratuito, rodando localmente via Docker.
  * **Banco de Dados:** PostgreSQL com a extensão `pgvector`.
  * **Infraestrutura:** Docker e Docker Compose.

-----

## 4\. Integração de Canal (Web Chat)

Conforme os requisitos do Projeto Integrador, a integração com o canal de chat (um web chat embutido) **é desacoplada** deste serviço de IA.

A arquitetura foi projetada para que um **Serviço Orquestrador** (o `chat_orchestrator` em Node.js no diagrama) seja o responsável por gerenciar a comunicação com o cliente (seja ele um site, um app, ou o WhatsApp).

### Exemplo de Fluxo (Desacoplado)

1.  **Canal Web (Web Chat Embutido):**

      * Um frontend React se conecta ao Orquestrador via **WebSocket (Socket.io)**.
      * Quando o usuário envia uma mensagem, o Orquestrador a recebe.
      * O Orquestrador então chama esta API (`/classify` ou `/query/rag`) para obter uma resposta.
      * A resposta da API é enviada de volta ao React pelo WebSocket.

2.  **Exemplo de Canal Alternativo (Ex: WhatsApp):**

      * Um usuário envia uma mensagem para o número do WhatsApp.
      * A API do WhatsApp envia um **Webhook** para o Orquestrador.
      * O Orquestrador recebe o Webhook, trata a mensagem e chama esta API (`/classify` ou `/query/rag`).
      * A resposta da API é formatada e enviada de volta para a API do WhatsApp, que a entrega ao usuário.

Em ambos os cenários, esta **API de IA não muda**. Ela é agnóstica ao canal, garantindo modularidade e escalabilidade.

-----

## 5\. Endpoints da API (Testando com Postman)

### Classificar Intenção

  * **URL:** `http://localhost:8001/classify`
  * **Método:** `POST`
  * **Body (JSON):**
    ```json
    {
        "query": "Como eu registro um furto de celular?"
    }
    ```
  * **Resposta (200 OK):**
    ```json
    {
        "intent": "registrar_bo"
    }
    ```

### Responder Pergunta (RAG)

  * **URL:** `http://localhost:8001/query/rag`
  * **Método:** `POST`
  * **Body (JSON):**
    ```json
    {
        "query": "Onde fica a delegacia da mulher no Recife?"
    }
    ```
  * **Resposta (200 OK):**
    ```json
    {
        "answer": "A 1ª Delegacia da Mulher - Recife fica na Rua XYZ, 987, Santo Amaro, Recife-PE. O telefone é (81) 9999-8888 e sua especialidade é o atendimento a vítimas de violência doméstica e familiar."
    }
    ```
