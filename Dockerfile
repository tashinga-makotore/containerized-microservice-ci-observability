# -----------------------------
# Stage 1: Build dependencies
# -----------------------------
FROM python:3.13-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# -----------------------------
# Stage 2: Runtime container
# -----------------------------
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd \
    --create-home \
    --shell /usr/sbin/nologin \
    appuser

COPY --from=builder /install /usr/local

COPY app ./app
COPY scripts ./scripts

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD ["python", "scripts/health_check.py"]

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]