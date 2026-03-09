FROM python:3.12-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all project code
COPY . .

# default command (overridden per service in docker-compose)
CMD ["python", "--version"]
