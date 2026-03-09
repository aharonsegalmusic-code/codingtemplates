FROM python:3.12-slim
WORKDIR /app
COPY risk_evaluator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY risk_evaluator/ ./risk_evaluator/
COPY data/ ./data/
CMD ["python", "-m", "risk_evaluator.risk_evaluator"]
