FROM python:3.9-slim

WORKDIR /app

# Install curl for the healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir requests

COPY main.py .

# Use CMD instead of ENTRYPOINT for better environment variable handling
CMD ["python", "main.py"]
