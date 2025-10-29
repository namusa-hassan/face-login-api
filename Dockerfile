# Use a slim base image
FROM python:3.11-slim

# Install system dependencies required for dlib and OpenCV
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

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Set environment variable for Railway
ENV PORT=8080
EXPOSE $PORT

# Start app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "verify_face:app"]
