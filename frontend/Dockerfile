# Use official Python 3.13.2 base image
FROM python:3.13.2

# Set working directory
WORKDIR /app

# Copy requirements and install them first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire frontend source code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Streamlit run command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
