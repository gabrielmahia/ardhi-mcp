# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for ardhi-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/ardhi-mcp"
LABEL org.opencontainers.image.description="ardhi-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir ardhi-mcp

CMD ["ardhi-mcp"]
