#!/bin/sh

# path es2
PROJECT_DIR="${1:-/home/ubuntu/wine-shop/backend}"

# Exit the script immediately if any command exits with a non-zero status
set -e

# Function to handle errors with custom messages
handle_error() {
    echo "Error: $1"
    exit 1
}

# Navigate to the application directory
cd "$PROJECT_DIR" || handle_error "Failed to navigate to the application directory."

echo "Start renew certificate"
docker compose -f docker-compose-update-cert.yml up --rm

echo "Reload nginx"
docker exec nginx nginx -s reload

echo "Certificate has renewed, nginx has reloaded successfully"



# створити періодичне завдання
# crontab -e
# 0 3 * * * /home/ubuntu/wine-shop/backend/commands/cert_renew.sh >> /var/log/certbot-renew.log 2>&1