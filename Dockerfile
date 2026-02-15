FROM python:3.13-slim

WORKDIR /app

# Copy dependency file first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose port 8080
EXPOSE 8080

# Run uvicorn - bind to 0.0.0.0 so it's accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
