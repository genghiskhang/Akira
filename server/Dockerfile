FROM python:3.12-slim

USER root

WORKDIR /app

ADD akira /app/akira

COPY requirements.txt .

RUN pip install --no-cache-dir --no-compile --upgrade pip
RUN pip install --no-cache-dir --no-compile -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "akira:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]