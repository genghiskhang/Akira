FROM python:3.12-slim

USER root

WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir --no-compile --upgrade pip
RUN pip install --no-cache-dir --no-compile -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]