FROM python:3.13.2

WORKDIR /app

COPY requirements.txt .
COPY .env .env  # <-- ADD THIS LINE

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
