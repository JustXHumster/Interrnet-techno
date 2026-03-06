FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0

EXPOSE 5000

CMD ["python", "app.py"]