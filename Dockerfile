FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
