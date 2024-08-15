# Use an ARM-compatible base image for Raspberry Pi (adjust if necessary)
FROM arm32v7/python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH="/app"

# Copy the requirements file and install dependencies
COPY ./auth_service/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the utils folder into the container
COPY ./utils /app/utils

# Copy the Python script into the container
COPY ./auth_service/index.py /app/

# Command to run the script
CMD ["python", "index.py"]
