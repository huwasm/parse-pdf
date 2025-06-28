FROM python:3.12-slim

# native dep for PyMuPDF
RUN apt-get update \
 && apt-get install -y libmupdf-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask pymupdf pillow requests

COPY app.py /app/
ENV PORT 8080
CMD ["python", "/app/app.py"]
