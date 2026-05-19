# Hugging Face recommended base image
FROM python:3.9

# Hugging Face ke liye user banana zaroori hai
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Requirements pehle copy karo (Docker caching ke liye)
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Baaki sab copy karo
COPY --chown=user . /app

# Port 7860 — Hugging Face ka default port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]