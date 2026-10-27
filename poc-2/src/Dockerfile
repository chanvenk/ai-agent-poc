# Use a lightweight official Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the default port expected by Foundry/azd local routing (8088)
EXPOSE 8088

# Command to run the application specified in azure.yaml
CMD ["python", "main.py"]