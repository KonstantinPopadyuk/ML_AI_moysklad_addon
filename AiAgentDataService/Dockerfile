# AiAgentDataService/Dockerfile
FROM python:3.12-slim

# RUN apk add --no-cache \
#     gcc \
#     musl-dev \
#     libffi-dev \
#     openssl-dev \
#     zlib-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire service code
COPY . .

# Command to run the service
CMD ["python", "main.py"]