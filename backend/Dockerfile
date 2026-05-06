FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app ./app
RUN pip install --no-cache-dir fastapi>=0.115.0 uvicorn[standard]>=0.32.0 sqlalchemy[asyncio]>=2.0.36 asyncpg>=0.30.0 pydantic>=2.9.0 pydantic-settings>=2.6.0 httpx>=0.27.0
EXPOSE 
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", ""]
