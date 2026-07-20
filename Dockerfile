# =============================================================================
# BenchDash — local system profile dashboard (stdlib-only Python)
# JorahOne LLC
# =============================================================================
FROM python:3.12-alpine

# procps/pciutils give the collector real data inside the container;
# curl is used by the HEALTHCHECK.
RUN apk add --no-cache curl procps pciutils util-linux

WORKDIR /app

# Application code
COPY collector/ ./collector/
COPY app.py benchdash.py ./
COPY static/ ./static/

RUN mkdir -p results outputs \
    && addgroup -S bench && adduser -S bench -G bench \
    && chown -R bench:bench /app
USER bench

ENV DASHBOARD_HOST=0.0.0.0 \
    DASHBOARD_PORT=8081

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f "http://localhost:${DASHBOARD_PORT}/api/health" || exit 1

CMD ["python3", "app.py"]
