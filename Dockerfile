  FROM python:3.12-slim

  RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      && rm -rf /var/lib/apt/lists/*

  RUN groupadd --gid 1000 appuser && \
      useradd --uid 1000 --gid 1000 --create-home appuser && \
      mkdir /app && \
      chown appuser:appuser /app

  RUN curl -LsSf https://astral.sh/uv/0.8.13/install.sh | sh

  ENV PATH="/home/appuser/.local/bin:$PATH"

  WORKDIR /app

  COPY --chown=appuser:appuser pyproject.toml .python-version uv.lock ./

  RUN uv sync --locked --no-cache

  COPY --chown=appuser:appuser . .
  
  USER appuser

  EXPOSE 8000

  CMD ["./entrypoint.sh"]
