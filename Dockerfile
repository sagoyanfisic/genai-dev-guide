FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home appuser

USER appuser

ADD --chown=appuser:appuser https://astral.sh/uv/0.8.13/install.sh /home/appuser/uv-installer.sh
RUN sh /home/appuser/uv-installer.sh && rm /home/appuser/uv-installer.sh

ENV PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app

COPY --chown=appuser:appuser pyproject.toml .python-version uv.lock ./

RUN uv sync --locked --no-cache

COPY --chown=appuser:appuser . .

EXPOSE 8080

CMD ["./entrypoint.sh"]
