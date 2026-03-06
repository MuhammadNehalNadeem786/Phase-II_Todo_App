FROM python:3.10-slim

# Set workdir to backend folder inside container
WORKDIR /app/backend

# Copy only backend requirements first for caching
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


