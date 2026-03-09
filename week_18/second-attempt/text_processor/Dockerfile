FROM python:3.12-slim
WORKDIR /app
COPY text_processor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY text_processor/ ./text_processor/
COPY data/ ./data/
CMD ["python", "-m", "text_processor.text_worker"]
