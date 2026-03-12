FROM python:3.12-slim

# Install system dependencies needed for SHAP/XGBoost
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Install dependencies from the internet
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the rest of the code
COPY . .

EXPOSE 10000

# Render uses port 10000 by default, let's match it
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]