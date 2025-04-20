FROM python:3.12.9-slim-bookworm as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv pip install --no-cache -r requirements.txt

#################

FROM python:3.12.9-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# Настройки Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PYTHONFAULTHANDLER=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]