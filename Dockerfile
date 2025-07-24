# Base image
FROM python:3.9-slim

# Environment variables

ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLAST_ENV=production \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# ExPOSE the app port
EXPOSE $PORT

# Init db script
COPY init_db.py .

#Start the app using gunicorn
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:application"]
CMD ["sh", "-c", "python init_db.py && gunicorn -w 4 -b 0.0.0.0:8000 wsgi:application"]