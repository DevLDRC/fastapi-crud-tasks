# FastAPI CRUD Tasks

API REST para gerenciamento de tarefas e autenticação de usuários, desenvolvida com **FastAPI**, **SQLAlchemy** (SQLite) e autenticação via **JWT**, utilizando o **uv** como gerenciador de pacotes e ambiente virtual.

---

## 📋 Pré-requisitos

Para executar a aplicação diretamente na máquina:
- [Python](https://www.python.org/) (versão `>= 3.14`)
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependências e ambientes Python)
  - *Instalação rápida do `uv`:*
    - **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
    - **Linux / macOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Git](https://git-scm.com/)

Para executar em container isolado (dispensa a instalação de Python ou uv locais):
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Guia de Execução Local (com uv)

Siga o passo a passo abaixo para clonar, configurar e rodar o projeto localmente:

### 1. Clonar o repositório

```bash
git clone https://github.com/DevLDRC/fastapi-crud-tasks.git
cd fastapi-crud-tasks
```

### 2. Configurar variáveis de ambiente

Crie o arquivo `.env` a partir do modelo `.env.example`:

- **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux / macOS (Bash):**
  ```bash
  cp .env.example .env
  ```

Edite o arquivo `.env` gerado e defina uma chave para a assinatura dos tokens JWT:

```env
SECRET_SIGNATURE="sua_chave_secreta_aqui"
```

### 3. Instalar as dependências

Instale todas as dependências do projeto (incluindo desenvolvimento e testes) utilizando o `uv`:

```bash
uv sync
```

> **Nota:** O `uv` criará automaticamente o ambiente virtual (`.venv`) e instalará as versões travadas no `uv.lock`.

### 4. Executar a aplicação

Inicie o servidor de desenvolvimento com recarregamento automático (*live reload*):

```bash
uv run uvicorn src.fastapi_crud_tasks.main:app --reload --host 127.0.0.1 --port 8000
```

A aplicação estará acessível em: `http://127.0.0.1:8000`

---

## 🐳 Executando com Docker (Ambiente Isolado)

Se preferir rodar a aplicação em um ambiente conteinerizado sem precisar configurar Python ou dependências na máquina:

### Opção 1: Via Docker Compose (Recomendado)

O projeto inclui um [`docker-compose.yml`](docker-compose.yml) configurado:

```bash
docker compose up -d --build
```

Para visualizar os logs e parar os serviços:
```bash
docker compose logs -f
docker compose down
```

### Opção 2: Via Docker CLI

1. **Construir a imagem Docker:**
   ```bash
   docker build -t fastapi-crud-tasks .
   ```

2. **Executar o container:**
   ```bash
   # Utilizando o arquivo .env:
   docker run -d -p 8000:8000 --env-file .env --name fastapi-tasks-app fastapi-crud-tasks

   # Ou informando a variável diretamente:
   docker run -d -p 8000:8000 -e SECRET_SIGNATURE="sua_chave_secreta" --name fastapi-tasks-app fastapi-crud-tasks
   ```

3. **Gerenciar o container:**
   ```bash
   # Ver logs:
   docker logs -f fastapi-tasks-app

   # Parar o container:
   docker stop fastapi-tasks-app
   ```

A API estará disponível na porta `8000`: `http://localhost:8000`

---

## 📚 Documentação Interativa da API

Com a aplicação em execução (seja local ou via Docker), acesse a documentação interativa gerada automaticamente pelo FastAPI:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Executando os Testes

Os testes são gerenciados pelo **pytest**. Para executar a suíte de testes completa:

```bash
uv run pytest
```

Para uma saída detalhada e com log de execução:

```bash
uv run pytest -v
```

---

## 📬 Testando Requisições com `rest.http`

O projeto inclui o arquivo [`rest.http`](rest.http), que permite disparar requisições diretamente no **VS Code** usando a extensão [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client):

- Rotas de Autenticação (`/auth/register`, `/auth/login`, `/auth/me`)
- Rotas CRUD de Itens (`/items/`, `/items/{id}`)