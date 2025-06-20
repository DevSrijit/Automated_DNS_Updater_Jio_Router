#!/bin/bash

# JIO Router DNS Updater - Docker Deployment Script
# Optimized for Raspberry Pi Zero 2W

set -e

echo "🚀 JIO Router DNS Updater - Docker Setup"
echo "========================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from example..."
    cp .env.example .env
    echo "✅ Please edit .env file with your router credentials and DNS settings"
    echo "   Then run this script again."
    exit 1
fi

# Create logs directory
mkdir -p logs

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   For Raspberry Pi: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Function to use docker-compose or docker compose
run_compose() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

echo "🔧 Building Docker image (optimized for ARM/Raspberry Pi)..."
run_compose build

echo "🚀 Starting DNS Updater service..."
run_compose up -d

echo ""
echo "✅ DNS Updater is now running!"
echo ""
echo "📊 Useful commands:"
echo "   View logs:     $(if command -v docker-compose &> /dev/null; then echo 'docker-compose logs -f'; else echo 'docker compose logs -f'; fi)"
echo "   Stop service:  $(if command -v docker-compose &> /dev/null; then echo 'docker-compose down'; else echo 'docker compose down'; fi)"
echo "   Restart:       $(if command -v docker-compose &> /dev/null; then echo 'docker-compose restart'; else echo 'docker compose restart'; fi)"
echo "   Status:        $(if command -v docker-compose &> /dev/null; then echo 'docker-compose ps'; else echo 'docker compose ps'; fi)"
echo ""
echo "📋 Container Status:"
run_compose ps

echo ""
echo "📱 The service will automatically update your router's DNS settings"
echo "   according to the schedule defined in your .env file."
echo ""
echo "🔍 To view real-time logs:"
echo "   $(if command -v docker-compose &> /dev/null; then echo 'docker-compose logs -f dns-updater'; else echo 'docker compose logs -f dns-updater'; fi)"
