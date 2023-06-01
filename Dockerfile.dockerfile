# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and HTML template into the container
COPY app.py .
COPY template.html .

# Expose the port your Flask app will be running on (e.g., 5000)
EXPOSE 5000

# Set the command to run when the container starts
CMD ["python", "app.py"]
