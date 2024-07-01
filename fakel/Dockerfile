FROM python:3.9.19-alpine

LABEL authors="Serezhkin Konstantin"

WORKDIR /app/

ENV PYTHONPATH=/app/fakel/

COPY ./requirements.txt /app/fakel/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/fakel/requirements.txt

COPY . /app/fakel/
