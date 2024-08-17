FROM python:3.11.9-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./bbot /bbot
WORKDIR /bbot
EXPOSE 8000

RUN apk add py3-scikit-learn && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        tradebot

ENV PATH="/py/bin:$PATH"

USER tradebot