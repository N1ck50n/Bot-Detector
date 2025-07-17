# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY analyzeLogs.py .

# If you have a log file or want to copy sample logs, you can add:
# COPY sample-log.log .

# Command to run the script when the container starts
CMD ["python", "analyzeLogs.py"]
