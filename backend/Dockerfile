# Backend Dockerfile

FROM python:3.11.6-slim

RUN mkdir -p /dotaverse/backend
WORKDIR /dotaverse

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY backend ./backend

EXPOSE 8000
