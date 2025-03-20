# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files **including** model files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Verify that model files exist inside the container
RUN ls -l /app/

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
