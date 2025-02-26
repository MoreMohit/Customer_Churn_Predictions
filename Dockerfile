# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

# Expose the required port for Streamlit
EXPOSE 8080

# Run the Streamlit app
CMD ["streamlit", "run", "apk.py", "--server.port=8080", "--server.address=0.0.0.0"]
