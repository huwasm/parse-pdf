FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y libmupdf-dev fonts-freefont-ttf \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask pymupdf pillow requests gunicorn

WORKDIR /app
COPY app.py .

ENV PYTHONUNBUFFERED=1
ENV PORT 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--log-level=debug", "app:app"]
