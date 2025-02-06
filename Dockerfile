# Use a lightweight Python image
FROM python:3.12-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . /app


# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Expose the FastAPI port

CMD ["python","app.py"]


