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

# Fetch the latest changes from the remote repository
echo "Fetching the latest changes from the remote repository..."
git fetch origin main || handle_error "Failed to fetch updates from the 'origin' remote."

# Reset the local repository to match the remote 'main' branch
echo "Resetting the local repository to match 'origin/main'..."
git reset --hard origin/main || handle_error "Failed to reset the local repository to 'origin/main'."

# (Optional) Pull any new tags from the remote repository
echo "Fetching tags from the remote repository..."
git fetch origin --tags || handle_error "Failed to fetch tags from the 'origin' remote."

echo "rename .env.sample to .env ..."
cp .env.sample .env

echo "add permissions to run for cert_init.sh"
chmod +x ./commands/cert_renew.sh


echo "📦 remove irrelevant containers and services"
docker compose -f docker-compose-prod.yml down --remove-orphans || echo "⚠️ Warning: Down with Orphans not completed "

# Build and run Docker containers with Docker Compose v2
docker compose -f docker-compose-prod.yml up -d --build || handle_error "Failed to build and run Docker containers using docker-compose-prod.yml."


# Print a success message upon successful deployment
echo "Deployment completed successfully."
