# Use a lightweight Python base
FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Install system dependencies for dlib
RUN apt-get update && apt-get install -y cmake libdlib-dev libgl1 && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PORT=8080
EXPOSE $PORT

CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "verify_face:app"]
