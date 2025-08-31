# Atividade Integradora - API de Inventário de Produtos

Este projeto é uma API RESTful para gerenciamento de um inventário de produtos simples, desenvolvida como parte da Atividade Integradora para a Faculdade QI - Polo Rio Grande/RS.

A aplicação foi construída utilizando Python com o framework FastAPI. O projeto adota princípios de **Clean Code**, utilizando uma arquitetura em camadas e uma convenção de nomenclatura de arquivos que revela a intenção de cada módulo, facilitando a manutenção e evitando ambiguidades durante o desenvolvimento.

**Aluno:** Rafael da Silva Santos
**Polo:** Faculdade QI - Rio Grande/RS
**LinkedIn:** https://www.linkedin.com/in/skan90/

---

## 1. Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de Dados:** SQLite
- **Validação de Dados:** Pydantic
- **Servidor:** Uvicorn
- **Containerização:** Docker & Docker Compose

## 2. Estrutura do Projeto

O projeto segue uma arquitetura modular e escalável (inspirada no padrão Controller-Service-Repository) para garantir uma clara separação de responsabilidades.

Para aderir às práticas de Clean Code, os arquivos dentro dos diretórios `models`, `schemas`, `routers` e `services` possuem sufixos que identificam claramente seu propósito (ex: `_model.py`, `_schema.py`). Isso elimina a confusão de ter múltiplos arquivos com o mesmo nome (`product.py`) e melhora a navegabilidade do projeto.

```
sw-atividade-integradora/
├── app/
│   ├── __init__.py
│   ├── database.py         # Configuração da sessão do banco de dados SQLAlchemy
│   ├── main.py             # Ponto de entrada da aplicação FastAPI
│   ├── models/
│   │   └── product_model.py  # Modelo da tabela de produtos (SQLAlchemy)
│   ├── schemas/
│   │   └── product_schema.py # Esquemas de dados para validação (Pydantic)
│   ├── routers/
│   │   └── product_router.py # Camada de Roteamento/Controller (Endpoints da API)
│   └── services/
│       └── product_service.py# Camada de Serviço (Lógica de negócio)
├── .gitignore
├── docker-compose.yml      # Orquestrador dos containers
├── Dockerfile              # Definição do container da aplicação
├── README.md               # Este arquivo
└── requirements.txt        # Dependências Python
```

## 3. Como Executar o Projeto

Existem duas maneiras de executar o projeto: utilizando Docker (recomendado) ou em um ambiente Python local.

### 3.1. Execução com Docker (Recomendado)

Este método é mais simples, pois o Docker gerencia todo o ambiente e as dependências para você.

**Pré-requisitos:**
* Docker instalado.
* Docker Compose instalado.

**Passos:**

1.  **Extraia os arquivos do projeto** e navegue até o diretório raiz (`sw-atividade-integradora`).

2.  **Inicie os containers** com Docker Compose:
    ```bash
    sudo docker-compose up --build
    ```
    Este comando irá:
    * Construir a imagem Docker da aplicação.
    * Iniciar um container para a API.
    * Criar um volume no diretório `data/` para persistir o banco de dados.
    * Iniciar o servidor Uvicorn. Durante a inicialização, as tabelas do banco de dados serão criadas automaticamente.

3.  **Acesse a API:**
    * A API estará disponível em: `http://localhost:8000`
    * A documentação interativa (Swagger UI) estará em: `http://localhost:8000/docs`
    * A documentação alternativa (ReDoc) estará em: `http://localhost:8000/redoc`

### 3.2. Execução em Ambiente Local

**Pré-requisitos:**
* Python 3.11+

**Passos:**

1.  **Extraia os arquivos do projeto** e navegue até o diretório raiz (`sw-atividade-integradora`).

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    ```
    * No Windows: `venv\Scripts\activate`
    * No macOS/Linux: `source venv/bin/activate`

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicie a aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Ao iniciar, a aplicação criará o arquivo de banco de dados `database.db` dentro de um novo diretório `data/`.

5.  **Acesse a API:**
    * A documentação interativa (Swagger UI) estará disponível em: `http://localhost:8000/docs`

## 4. Documentação da API (Endpoints)

A API fornece operações CRUD completas para o recurso de produtos.

### `POST /api/v1/products/`

* **Descrição:** Cria um novo produto no inventário.
* **Corpo da Requisição (JSON):**
    ```json
    {
      "name": "Smartphone Pro Max",
      "description": "Último lançamento com câmera tripla.",
      "price": 7499.99,
      "quantity": 50
    }
    ```
* **Resposta de Sucesso (201 Created):**
    ```json
    {
      "id": 1,
      "name": "Smartphone Pro Max",
      "description": "Último lançamento com câmera tripla.",
      "price": 7499.99,
      "quantity": 50
    }
    ```

### `GET /api/v1/products/`

* **Descrição:** Lista todos os produtos cadastrados.
* **Resposta de Sucesso (200 OK):**
    ```json
    [
      {
        "id": 1,
        "name": "Smartphone Pro Max",
        "description": "Último lançamento com câmera tripla.",
        "price": 7499.99,
        "quantity": 50
      }
    ]
    ```

### `GET /api/v1/products/{product_id}`

* **Descrição:** Busca um produto específico pelo seu ID.
* **Resposta de Sucesso (200 OK):**
    ```json
    {
      "id": 1,
      "name": "Smartphone Pro Max",
      "description": "Último lançamento com câmera tripla.",
      "price": 7499.99,
      "quantity": 50
    }
    ```
* **Resposta de Erro (404 Not Found):**
    ```json
    {
      "detail": "Product not found"
    }
    ```

### `PUT /api/v1/products/{product_id}`

* **Descrição:** Atualiza os dados de um produto existente.
* **Corpo da Requisição (JSON):**
    ```json
    {
      "name": "Smartphone Pro Max Plus",
      "description": "Versão atualizada com mais bateria.",
      "price": 7599.99,
      "quantity": 45
    }
    ```
* **Resposta de Sucesso (200 OK):**
    ```json
    {
      "id": 1,
      "name": "Smartphone Pro Max Plus",
      "description": "Versão atualizada com mais bateria.",
      "price": 7599.99,
      "quantity": 45
    }
    ```
* **Resposta de Erro (404 Not Found):**
    ```json
    {
      "detail": "Product not found"
    }
    ```

### `DELETE /api/v1/products/{product_id}`

* **Descrição:** Remove um produto do inventário.
* **Resposta de Sucesso (204 No Content):** A resposta não possui corpo.
* **Resposta de Erro (404 Not Found):**
    ```json
    {
      "detail": "Product not found"
    }
    ```