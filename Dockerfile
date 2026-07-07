# =============================================================================
# Ollama Benchmark Dashboard — LLM benchmarking platform
# JorahOne
# =============================================================================
FROM python:3.11-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy application
COPY collector/ ./collector/
COPY *.md ./

# Create runtime directories
RUN mkdir -p results outputs data

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${DASHBOARD_PORT:-8081}/ || exit 1

# Collect system info on startup
CMD ["python3", "collector/system_info.py"]
