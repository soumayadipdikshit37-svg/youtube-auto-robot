#!/bin/bash
# Setup script for GitHub Actions

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    wget \
    imagemagick

echo "Creating silent audio..."
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 60 silent.mp4 -y || echo "Audio creation failed, continuing..."

echo "Setup complete!"
