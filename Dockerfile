FROM python:3.11

WORKDIR /app

# requirements root mein hai
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# backend folder ka sara code copy karo
COPY backend/ .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]