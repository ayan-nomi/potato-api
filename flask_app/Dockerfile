# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for numpy and pandas
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel to avoid compatibility issues
RUN pip install --upgrade pip setuptools wheel

# Install numpy first to avoid compatibility issues with pandas
RUN pip install numpy==1.21.2

# Copy the requirements file to install remaining dependencies
COPY requirements.txt requirements.txt

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port for Flask
EXPOSE 5000

# Run the app by default
CMD ["flask", "run", "--host=0.0.0.0"]

