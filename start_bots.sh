#!/bin/bash

# TrustCoin Bots Startup Script
# This script helps you manage the TrustCoin bots deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed."
}

# Function to check environment file
check_env_file() {
    if [ ! -f ".env" ]; then
        print_error ".env file not found. Please create it with your bot tokens."
        exit 1
    fi
    
    # Check if required tokens are present
    if ! grep -q "BOT_TOKEN_ENG=" .env || ! grep -q "BOT_TOKEN_ARA=" .env || ! grep -q "BOT_TOKEN_FR=" .env; then
        print_error "Missing bot tokens in .env file. Please check BOT_TOKEN_ENG, BOT_TOKEN_ARA, and BOT_TOKEN_FR."
        exit 1
    fi
    
    print_success "Environment file is configured correctly."
}

# Function to start the bots
start_bots() {
    print_status "Starting TrustCoin bots..."
    
    # Build and start containers
    docker-compose up --build -d
    
    if [ $? -eq 0 ]; then
        print_success "All bots started successfully!"
        print_status "Running containers:"
        docker-compose ps
    else
        print_error "Failed to start bots. Check the logs for more information."
        exit 1
    fi
}

# Function to stop the bots
stop_bots() {
    print_status "Stopping TrustCoin bots..."
    docker-compose down
    print_success "All bots stopped successfully!"
}

# Function to restart the bots
restart_bots() {
    print_status "Restarting TrustCoin bots..."
    docker-compose restart
    print_success "All bots restarted successfully!"
}

# Function to show logs
show_logs() {
    if [ -z "$1" ]; then
        print_status "Showing logs for all bots..."
        docker-compose logs -f
    else
        print_status "Showing logs for $1 bot..."
        docker-compose logs -f "trustcoin-bot-$1"
    fi
}

# Function to show status
show_status() {
    print_status "TrustCoin Bots Status:"
    docker-compose ps
    echo ""
    print_status "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

# Main script logic
case "$1" in
    start)
        check_docker
        check_env_file
        start_bots
        ;;
    stop)
        stop_bots
        ;;
    restart)
        restart_bots
        ;;
    logs)
        show_logs "$2"
        ;;
    status)
        show_status
        ;;
    *)
        echo "TrustCoin Bots Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|logs|status}"
        echo ""
        echo "Commands:"
        echo "  start    - Start all TrustCoin bots"
        echo "  stop     - Stop all TrustCoin bots"
        echo "  restart  - Restart all TrustCoin bots"
        echo "  logs     - Show logs (optional: specify 'english', 'arabic', or 'french')"
        echo "  status   - Show bots status and resource usage"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 logs english"
        echo "  $0 status"
        exit 1
        ;;
esac