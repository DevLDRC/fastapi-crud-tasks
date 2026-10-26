# syntax=docker/dockerfile:1
FROM python:3.14-slim

# Copia os binários oficiais do uv a partir da imagem do Astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Diretório da aplicação no container
WORKDIR /app

# Variáveis de ambiente para otimização do uv e Python
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# 1. Instala primeiro apenas as dependências do projeto aproveitando cache de camadas
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# 2. Copia o código-fonte da aplicação
COPY . /app

# 3. Sincroniza e instala a aplicação no ambiente virtual
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Adiciona o ambiente virtual do uv ao PATH para execução direta
ENV PATH="/app/.venv/bin:$PATH"

# Expõe a porta padrão da API
EXPOSE 8000

# Executa a aplicação via Uvicorn ouvindo em todas as interfaces de rede (0.0.0.0)
CMD ["uvicorn", "src.fastapi_crud_tasks.main:app", "--host", "0.0.0.0", "--port", "8000"]
