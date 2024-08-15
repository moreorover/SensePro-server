# Use an ARM-compatible base image for Raspberry Pi (adjust if necessary)
FROM arm32v7/python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the utils folder into the container
COPY ./utils /app/utils

# Copy your Python scripts
COPY auth_service.py /app/

# Copy Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Command to run Supervisor
CMD ["/usr/bin/supervisord"]
