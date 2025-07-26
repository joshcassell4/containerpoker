.PHONY: help setup install clean start stop restart logs shell test format lint git-init

# Default target
help:
	@echo "Container Poker - Container Orchestration Learning Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  setup     - Complete project setup (install uv, deps, build, start)"
	@echo "  install   - Install dependencies with uv"
	@echo "  build     - Build Docker containers"
	@echo "  start     - Start the application"
	@echo "  stop      - Stop all containers"
	@echo "  restart   - Restart the application"
	@echo "  logs      - Show application logs"
	@echo "  shell     - Open shell in the orchestrator container"
	@echo "  clean     - Clean up containers and images"
	@echo "  test      - Run tests"
	@echo "  format    - Format code with black"
	@echo "  lint      - Lint code with flake8"
	@echo "  git-init  - Initialize git repo and push to GitHub"

# Complete setup for new students
setup: check-uv install build start
	@echo "🎉 Setup complete! Visit http://localhost:5000"
	@echo "📚 Check README.md for usage instructions"

# Check if uv is installed
check-uv:
	@which uv > /dev/null || (echo "❌ uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)
	@echo "✅ uv found"

# Install Python dependencies
install:
	@echo "📦 Installing dependencies..."
	uv sync
	uv export --no-hashes > requirements.txt

# Build Docker containers
build:
	@echo "🔨 Building containers..."
	docker-compose build

# Start the application
start:
	@echo "🚀 Starting Container Poker..."
	docker-compose up -d
	@echo "🌐 Application available at http://localhost:5000"

# Stop containers
stop:
	@echo "🛑 Stopping containers..."
	docker-compose down

# Restart the application
restart: stop start

# Show logs
logs:
	docker-compose logs -f

# Open shell in orchestrator container
shell:
	docker-compose exec orchestrator bash

# Clean up everything
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	uv run pytest

# Format code
format:
	uv run black src/

# Lint code  
lint:
	uv run flake8 src/

# Initialize git repository and push to GitHub
git-init:
	@echo "🔧 Initializing git repository..."
	git init
	cp .env.example .env
	git add .
	git commit -m "Initial commit: Container Poker learning platform"
	@echo "📡 Creating GitHub repository 'containerpoker'..."
	gh repo create containerpoker --public --description "Container orchestration learning platform for students"
	git branch -M main
	git remote add origin https://github.com/$$(gh api user --jq .login)/containerpoker.git
	git push -u origin main
	@echo "🎉 Repository created and pushed to GitHub!"
	@echo "🔗 Visit: https://github.com/$$(gh api user --jq .login)/containerpoker"