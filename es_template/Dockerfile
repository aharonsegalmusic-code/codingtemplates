# ── Build stage ───────────────────────────────────────────────
# We use the official slim Python image to keep the image small.
FROM python:3.12-slim

# Set working directory inside the container.
# All subsequent commands run relative to this path.
WORKDIR /app

# Copy requirements first (Docker layer caching trick):
# If requirements.txt hasn't changed, Docker reuses the cached
# pip install layer — making rebuilds much faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY app/  ./app/
COPY data/ ./data/

# Expose the port FastAPI listens on
EXPOSE 8000

# Start the server.
# We don't use `--reload` in production — that's for local dev only.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
