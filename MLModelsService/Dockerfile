# MLModelsService/Dockerfile
FROM python:3.12-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# #without it catboost do not install
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire service code
COPY . .

# Command to run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]