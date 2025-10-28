# Base image with Python 3.11
FROM python:3.11-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose port (Railway uses $PORT automatically)
EXPOSE 8080

# Start the Flask app with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "verify_face:app", "--workers", "4", "--threads", "2"]
