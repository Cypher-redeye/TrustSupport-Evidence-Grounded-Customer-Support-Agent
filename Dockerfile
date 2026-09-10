FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY data/ /app/data/
COPY models/ /app/models/
COPY results/ /app/results/
COPY src/ /app/src/

# Expose FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Command is handled by docker-compose
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
