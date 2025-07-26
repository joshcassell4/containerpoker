.PHONY: help setup setup-dev docker-setup install clean start stop restart logs shell test format lint git-init

# Default target
help:
	@echo "Container Poker - Container Orchestration Learning Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  setup        - Quick setup for container development (no local Python needed)"
	@echo "  setup-dev    - Full setup with local Python development (requires uv)"
	@echo "  docker-setup - Alias for setup (container-only development)"
	@echo "  build        - Build Docker containers"
	@echo "  start        - Start the application"
	@echo "  stop         - Stop all containers"
	@echo "  restart      - Restart the application"
	@echo "  logs         - Show application logs"
	@echo "  shell        - Open shell in the orchestrator container"
	@echo "  clean        - Clean up containers and images"
	@echo "  test         - Run tests in container"
	@echo "  format       - Format code in container"
	@echo "  lint         - Lint code in container"
	@echo "  install-dev-tools - Install pytest, black, flake8 in container"
	@echo "  git-init     - Initialize git repo and push to GitHub"

# Quick setup for container development (Windows/Mac/Linux friendly)
setup: build start
	@echo "Setup complete! Visit http://localhost:5000"
	@echo "All development happens inside the container - no local Python needed!"
	@echo "TIP: Use 'make shell' to access the container"

# Alias for container-only setup
docker-setup: setup

# Full setup for local development (requires uv)
setup-dev: check-uv install build start
	@echo "Full development setup complete! Visit http://localhost:5000"
	@echo "You can develop locally or in the container"

# Check if uv is installed (only for local development)
check-uv:
	@which uv > /dev/null || (echo "ERROR: uv not found. For local development, install with: curl -LsSf https://astral.sh/uv/install.sh | sh" && echo "TIP: Use 'make setup' for container-only development (no uv needed)" && exit 1)
	@echo "uv found"

# Install Python dependencies locally (only for local development)
install:
	@echo "Installing dependencies locally..."
	uv sync
	uv export --no-hashes > requirements.txt

# Build Docker containers
build:
	@echo "Building containers..."
	docker compose build

# Start the application
start:
	@echo "Starting Container Poker..."
	docker compose up -d
	@echo "Application available at http://localhost:5000"

# Stop containers
stop:
	@echo "Stopping containers..."
	docker compose down

# Restart the application
restart: stop start

# Show logs
logs:
	docker compose logs -f

# Open shell in orchestrator container
shell:
	docker compose exec orchestrator bash

# Clean up everything
clean:
	@echo "Cleaning up..."
	docker compose down -v --remove-orphans
	docker system prune -f

# Run tests (in container)
test:
	@echo "Running tests in container..."
	docker compose exec orchestrator python -m pytest || echo "Install pytest in container first: make shell, then pip install pytest"

# Format code (in container)
format:
	@echo "Formatting code in container..."
	docker compose exec orchestrator python -m black src/ || echo "Install black in container first: make shell, then pip install black"

# Lint code (in container)
lint:
	@echo "Linting code in container..."
	docker compose exec orchestrator python -m flake8 src/ || echo "Install flake8 in container first: make shell, then pip install flake8"

# Install dev tools in container
install-dev-tools:
	@echo "Installing development tools in container..."
	docker compose exec orchestrator pip install pytest black flake8

# Initialize git repository and push to GitHub
git-init:
	@echo "Initializing git repository..."
	git init
	cp .env.example .env
	git add .
	git commit -m "Initial commit: Container Poker learning platform"
	@echo "Creating GitHub repository 'containerpoker'..."
	gh repo create containerpoker --public --description "Container orchestration learning platform for students"
	git branch -M main
	git remote add origin https://github.com/$$(gh api user --jq .login)/containerpoker.git
	git push -u origin main
	@echo "Repository created and pushed to GitHub!"
	@echo "Visit: https://github.com/$$(gh api user --jq .login)/containerpoker"