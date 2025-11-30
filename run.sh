#!/usr/bin/env bash
set -e

IMAGE_NAME="color-mood-analyzer:latest"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Running container on port 8080..."
docker run --rm -p 8080:8080 -v $(pwd)/assets:/app/assets $IMAGE_NAME

chmod +x run.sh
echo "Run script is now executable."
