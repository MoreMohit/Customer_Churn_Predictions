# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy only requirements first (for caching dependencies)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Ensure model file is available
RUN ls -l /app/

# Copy the correct new model file
COPY Best_Model_Forest_New.pkl /app/Best_Model_Forest_New.pkl

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
