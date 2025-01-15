# Etapa 1: Builder
FROM python:3.13 AS builder

# Instalar o Poetry
RUN pip install poetry==1.8

# Configurar variáveis de ambiente do Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copiar os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Instalar dependências sem as de desenvolvimento
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Etapa 2: Runtime
FROM python:3.13-slim AS runtime

# Configurar o ambiente virtual
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Definir o nível de log padrão
ENV PICTURAS_LOG_LEVEL=WARN

# Copiar o ambiente virtual da etapa builder
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copiar o código do microserviço
COPY picturas_people_counter_tool_ms ./picturas_people_counter_tool_ms

# Definir o ponto de entrada
ENTRYPOINT ["python", "-m", "picturas_people_counter_tool_ms.main"]
