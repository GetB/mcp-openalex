FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY mcp_openalex/ ./mcp_openalex/
RUN pip install --no-cache-dir .
EXPOSE 8080
CMD ["sh", "-c", "uvicorn mcp_openalex.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
