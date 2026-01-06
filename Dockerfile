# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Avoid running as root: create a user
RUN useradd -m appuser

# Set the working directory in the container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt /app/

# Upgrade pip safely
RUN python -m pip install --upgrade pip

# Install dependencies as root (needed inside container, safe)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Run uvicorn as non-root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
