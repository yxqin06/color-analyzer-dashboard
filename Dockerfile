# 1. Base image
FROM python:3.12-slim
ENV FLASK_ENV=development


# 2. Set working directory
WORKDIR /app

# 3. Install system deps for Pillow
RUN apt-get update && apt-get install -y \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy project files
COPY . /app

# 5. Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# 6. Expose Flask port
EXPOSE 8080

# 7. Run API
CMD ["flask", "--app", "src.api", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
