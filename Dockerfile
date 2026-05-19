FROM python:3.11

# Hugging Face ka default user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# requirements copy karo
COPY --chown=user requirements.txt requirements.txt

# install karo
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# baaki sab copy karo
COPY --chown=user . /app

# Hugging Face port
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]