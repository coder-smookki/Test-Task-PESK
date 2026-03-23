FROM python:3.12-slim AS base

WORKDIR /app

COPY pyproject.toml .

FROM base AS bot

RUN pip install --no-cache-dir .

COPY . .

CMD ["python", "-m", "app.bot.__main__"]

FROM base AS api

RUN pip install --no-cache-dir ".[api]"

COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.api.__main__"]
