FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y libmupdf-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask pymupdf pillow requests

WORKDIR /app
COPY app.py .

ENV PORT 8080
CMD ["python", "app.py"]
