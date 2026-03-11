# Use a lightweight Python base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# 1. Copy everything (All your code + the mountain of .whl files)
COPY . .

# 2. Install EVERYTHING from the local folder ONLY
# This tells Docker: "Don't go to the internet, use the files I provided."
RUN pip install --no-cache-dir --no-index --find-links . -r requirements.txt

# 3. Clean up the installation files to keep the image small
RUN rm *.whl

# 4. Network and Execution
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]