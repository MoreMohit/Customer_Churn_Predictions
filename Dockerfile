# Use an official lightweight Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port for Streamlit
EXPOSE 8080

# Run the Streamlit app
CMD ["streamlit", "run", "apk.py", "--server.port=8080", "--server.address=0.0.0.0"]
