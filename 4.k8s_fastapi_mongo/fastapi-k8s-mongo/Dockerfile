# --------------------------
# BASE IMAGE
# --------------------------
FROM python:3.11-slim

# --------------------------
# WORKDIR
# --------------------------
WORKDIR /app

# --------------------------
# COPY AND INSTALL DEPENDENCIES
# --------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------
# COPY APP CODE
# --------------------------
COPY app ./app

# --------------------------
# PRODUCTION CMD (no reload)
# --------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
