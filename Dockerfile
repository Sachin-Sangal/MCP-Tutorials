# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN pip install uv

# Copy requirements file
COPY requirements.txt .

# Install dependencies using uv
RUN uv venv
RUN uv pip install -r requirements.txt


# Copy application code
COPY weather.py .

# Expose port
EXPOSE 8050

# Command to run the server
CMD ["uv", "run", "weather.py"] 