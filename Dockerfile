# Base image with Python
FROM python:3.11-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Railway uses $PORT automatically)
ENV PORT=8080
EXPOSE $PORT

# Start the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "verify_face:app"]
