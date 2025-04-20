FROM python:3.12.9-alpine

# uv
COPY --from=http://ghcr.io/astral-sh/uv:lastest /uv /uvx /bin/

COPY  . /app

WORKDIR /app
RUN sync --frozen --no-cache

CMD []
