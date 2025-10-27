# 1. Base Image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements e install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy o código da aplicação (a pasta 'app' local -> pasta 'app' no container)
COPY ./app ./app

# 5. Expõe a porta que o FastAPI vai rodar
EXPOSE 8001

# 6. Comando para rodar a aplicação (agora aponta para app.main)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]