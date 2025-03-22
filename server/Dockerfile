FROM python:3.12-slim

USER root

WORKDIR /app

ADD akira /app/akira

COPY requirements.txt .
COPY entrypoint.sh .
COPY init_db.py .

RUN pip install --no-cache-dir --no-compile --upgrade pip
RUN pip install --no-cache-dir --no-compile -r requirements.txt

EXPOSE 8080

CMD ["./entrypoint.sh"]