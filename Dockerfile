FROM python:3.12.3-alpine3.18

WORKDIR /app

COPY . .

RUN apk add --no-cache python3 py3-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python3", "bot.py"]
