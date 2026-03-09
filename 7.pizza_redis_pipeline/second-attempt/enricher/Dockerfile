FROM python:3.12-slim
WORKDIR /app
COPY enricher/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY enricher/ ./enricher/
COPY data/ ./data/
CMD ["python", "-m", "enricher.enricher_consumer"]
