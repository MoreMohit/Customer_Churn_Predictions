# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy only the requirements file first (optimizing cache usage)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project after dependencies are installed
COPY . .

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port for Streamlit
EXPOSE 8080

# Run the Streamlit app
CMD ["streamlit", "run", "./app.py", "--server.port=8080", "--server.address=0.0.0.0"]
