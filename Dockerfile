# Use Python 3.11 slim (compatible with pandas 2.5+)
FROM python:3.11-slim

# Install system dependencies for dlib and OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variable for Railway
ENV PORT=8080
EXPOSE $PORT

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "verify_face:app"]
