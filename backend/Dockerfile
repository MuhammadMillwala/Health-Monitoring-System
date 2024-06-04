# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install netcat (using netcat-openbsd)
RUN apt-get update && apt-get install -y netcat-openbsd

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make the wait-for-it.sh script executable
RUN chmod +x /app/wait-for-it.sh

# Specify the default command to run when starting the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
