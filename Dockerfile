# Use Python 3.12 base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Download wait-for-it.sh and make it executable
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x wait-for-it.sh

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Django’s port
EXPOSE 8000

# Run migrations and start server after waiting for DB and Redis
CMD ["sh", "-c", "./wait-for-it.sh db:5432 -- ./wait-for-it.sh redis:6379 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
