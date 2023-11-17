# syntax=docker/dockerfile:1

FROM python:3.11.4-slim-bookworm

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD [ "uvicorn", "poker_dapp_backend.server.main:app", "--host=0.0.0.0", "--port=8000" ,"--reload" ]
