# TelegramBotService/Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire service code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the service
CMD ["python", "main.py"]