# FastAPI CRUD Tasks

API REST para gerenciamento de tarefas e autenticação de usuários, desenvolvida com **FastAPI**, **SQLAlchemy** (SQLite) e autenticação via **JWT**, utilizando o **uv** como gerenciador de pacotes e ambiente virtual.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

- [Python](https://www.python.org/) (versão `>= 3.14`)
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependências e ambientes Python)
  - *Instalação rápida do `uv`:*
    - **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
    - **Linux / macOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Git](https://git-scm.com/)

---

## 🚀 Guia de Execução Local

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

Edite o arquivo `.env` gerado e defina uma chave segura para a assinatura dos tokens JWT:

```env
SECRET_SIGNATURE="sua_chave_secreta_aqui"
```

### 3. Instalar as dependências

Instale todas as dependências do projeto (incluindo as de desenvolvimento e testes) utilizando o `uv`:

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

## 📚 Documentação Interativa da API

Com a aplicação em execução, acesse a documentação interativa gerada automaticamente pelo FastAPI:

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