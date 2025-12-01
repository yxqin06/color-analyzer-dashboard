# Base image
FROM python:3.12-slim
ENV FLASK_ENV=development


# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8080

# Run API
CMD ["flask", "--app", "src.api", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
