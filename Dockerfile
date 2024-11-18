FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# In default mode 5000 will be used, you can change this by setting the UVICORN_PORT env to your own preferences
EXPOSE 5000

CMD ["python", "main.py"]