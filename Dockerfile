FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync \
    --frozen \
    --no-dev \
    --no-install-project

COPY app/ .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8000"]
