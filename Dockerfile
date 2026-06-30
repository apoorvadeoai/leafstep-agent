FROM python:3.11-slim

WORKDIR /app

COPY requirements-cloudrun.txt .
RUN pip install --no-cache-dir -r requirements-cloudrun.txt

COPY . .

ENV PORT=8080
ENV APP_MODULE=main:app

CMD exec uvicorn ${APP_MODULE} --host 0.0.0.0 --port ${PORT}
