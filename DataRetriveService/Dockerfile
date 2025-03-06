# DataRetriveService/Dockerfile
# Use a slim version of Python as the base image
FROM python:3.12.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire service code
COPY . .

# Command to run the service
CMD ["uvicorn", "main:app"]