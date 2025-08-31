# Estágio 1: Build - Instalação de dependências
FROM python:3.11-slim AS builder

WORKDIR /app

# Define variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala as dependências de build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Estágio 2: Final - Imagem de produção
FROM python:3.11-slim

WORKDIR /app

# Copia as dependências pré-compiladas do estágio de build
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copia o código da aplicação
COPY ./app /app/app

# Expõe a porta que a aplicação vai rodar
EXPOSE 8000

# O comando padrão para iniciar a aplicação.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
