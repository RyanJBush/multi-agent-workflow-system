FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies first for layer-cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ app/

# Ensure the SQLite data directory exists (mounted as a volume in Compose)
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
