# =============================================================================
# Ollama Benchmark Dashboard — LLM benchmarking platform
# JorahOne
#
# Auto-discover models → Run multi-dimensional tests → Rank & score → Visualize
# Uses only Python stdlib — no pip dependencies required.
# =============================================================================
FROM python:3.11-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy application
COPY collector/ ./collector/
COPY static/ ./static/
COPY *.py ./
COPY *.json ./
COPY *.md ./

# Create runtime directories
RUN mkdir -p results outputs

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${DASHBOARD_PORT:-8081}/api/summary || exit 1

# Default: start the dashboard server
CMD ["python3", "dashboard_server.py"]
