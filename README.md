# 🎓 Container Poker - Learn Container Orchestration

A hands-on learning platform for students to experiment with container orchestration using Docker, Python, and real-world patterns. Build, break, and understand containers through interactive examples!

## 🚀 Quick Start (2 minutes!)

```bash
# Clone the repository
git clone https://github.com/yourusername/containerpoker.git
cd containerpoker

# One command setup!
make setup

# Visit http://localhost:5000
```

That's it! You're ready to learn container orchestration! 🎉

## 📚 What You'll Learn

- **Container Basics**: Lifecycle, states, and management
- **Automation**: Using `pexpect` for scripted interactions
- **Interactive Sessions**: Real terminal access with `dockerpty`
- **Multi-Container Patterns**: Dependencies and networking
- **Health Monitoring**: Implementing resilient systems
- **Real-World Skills**: Patterns used in production environments

## 🛠️ Prerequisites

- **Docker**: Install from [docker.com](https://docker.com)
- **Python 3.8+**: Usually pre-installed on most systems
- **Git**: For cloning the repository
- **Make**: Usually pre-installed (Windows users: use Git Bash)

## 📖 Detailed Setup

### 1. Install Docker

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Log out and back in for group changes

# macOS
# Install Docker Desktop from docker.com

# Windows
# Install Docker Desktop from docker.com
# Use Git Bash for running commands
```

### 2. Install uv (Fast Python Package Manager)

```bash
# All platforms
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 3. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/containerpoker.git
cd containerpoker

# Complete setup (installs dependencies, builds containers, starts app)
make setup

# Or step by step:
make install  # Install Python dependencies
make build    # Build Docker containers
make start    # Start the application
```

## 🎮 Usage

### Available Commands

```bash
make help      # Show all available commands
make start     # Start the application
make stop      # Stop all containers
make restart   # Restart the application
make logs      # View application logs
make shell     # Open shell in orchestrator container
make clean     # Clean up all containers
make test      # Run tests
make format    # Format code with black
make lint      # Lint code with flake8
```

### Web Interface

Visit [http://localhost:5000](http://localhost:5000) after starting the application.

**Features:**
- **Dashboard**: System status and quick actions
- **Containers**: Manage and monitor containers
- **Examples**: Run educational orchestration examples
- **Logs**: Real-time log viewing with syntax highlighting

## 📚 Educational Examples

### 1. Hello World Container (Beginner)
Learn the basic container lifecycle - create, run, capture output, and cleanup.

### 2. Interactive Shell (Beginner)
Experience real terminal sessions using dockerpty - perfect for debugging!

### 3. Automated Commands (Intermediate)
Master pexpect for scripting complex command sequences with pattern matching.

### 4. Multi-Container Dependencies (Intermediate)
Orchestrate multiple containers with proper startup order and health checks.

### 5. Log Monitoring (Intermediate)
Stream logs in real-time and trigger automated responses to events.

### 6. Health Checks & Recovery (Advanced)
Implement production-ready health monitoring and auto-recovery patterns.

### 7. Container Networking (Advanced)
Create isolated networks and manage inter-container communication.

### 8. Volume Management (Intermediate)
Handle persistent data, backups, and data sharing between containers.

## 🏗️ Project Structure

```
containerpoker/
├── Dockerfile              # Orchestrator container definition
├── docker-compose.yml      # Multi-container setup
├── Makefile               # Student-friendly commands
├── pyproject.toml         # Python project configuration
├── requirements.txt       # Python dependencies (auto-generated)
├── .env.example          # Environment configuration template
├── README.md             # This file!
├── ORCHESTRATION.md      # Deep dive into orchestration concepts
└── src/
    ├── app.py            # Main Flask application
    ├── orchestrator/
    │   ├── __init__.py
    │   ├── core.py       # Container management functions
    │   ├── examples.py   # Educational example implementations
    │   └── utils.py      # Helper functions and logging
    ├── templates/        # HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── containers.html
    │   └── logs.html
    └── static/           # CSS and JavaScript
        ├── css/
        │   └── style.css
        └── js/
            └── app.js
```

## 🔧 Development Workflow

### Hot Reload Development

The application automatically reloads when you modify Python files!

```bash
# Terminal 1: Run the application
make start

# Terminal 2: View logs
make logs

# Edit files in ./src - changes auto-reload!
# Try modifying src/orchestrator/examples.py
```

### Adding New Examples

1. Edit `src/orchestrator/examples.py`
2. Add your function to the `ExampleFlows` class
3. Register it in the `self.examples` dictionary
4. The UI automatically picks it up!

### Debugging Tips

```bash
# Open shell in the orchestrator container
make shell

# Inside the container:
python
>>> import docker
>>> client = docker.from_env()
>>> client.containers.list()

# Check Docker directly
docker ps -a
docker logs containerpoker_orchestrator
```

## 🐛 Troubleshooting

### Common Issues

**"Permission denied" errors**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

**"Cannot connect to Docker daemon"**
```bash
# Start Docker service
sudo systemctl start docker
# Or on Mac/Windows: Start Docker Desktop
```

**"Port 5000 already in use"**
```bash
# Find process using port
lsof -i :5000
# Or change port in docker-compose.yml
```

**"Module not found" errors**
```bash
# Reinstall dependencies
make clean
make install
make build
```

## 📚 Learning Resources

- **ORCHESTRATION.md**: Deep dive into container orchestration concepts
- **Docker Documentation**: [docs.docker.com](https://docs.docker.com)
- **Python Docker SDK**: [docker-py.readthedocs.io](https://docker-py.readthedocs.io)
- **pexpect Documentation**: [pexpect.readthedocs.io](https://pexpect.readthedocs.io)

## 🤝 Contributing

We welcome contributions from students and educators!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- New educational examples
- Improved error messages
- Additional orchestration patterns
- Documentation improvements
- UI enhancements

## 📝 License

This project is licensed under the MIT License - perfect for educational use!

## 🙏 Acknowledgments

- Docker team for amazing container technology
- Flask community for the simple web framework
- Students who inspired this educational approach
- Open source community for tool support

## 💡 Tips for Students

1. **Start Simple**: Begin with Example 1 and work your way up
2. **Read the Logs**: They contain educational tips and insights
3. **Break Things**: Don't be afraid to experiment and fail
4. **Check Browser Console**: Educational messages appear there too
5. **Modify Code**: The best way to learn is by changing things
6. **Ask Questions**: Use the GitHub issues for help

---

**Happy Learning! 🐳** Remember: The best way to learn container orchestration is by doing. Start with `make setup` and explore!