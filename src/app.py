"""
Container Poker - Container Orchestration Learning Platform
Main Flask application for experimenting with container orchestration
"""

import os
import logging
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import docker
from datetime import datetime

# Import our orchestrator modules
from orchestrator.core import ContainerManager
from orchestrator.examples import ExampleFlows
from orchestrator.utils import setup_logging, error_handler

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Set up logging for educational purposes
logger = setup_logging(app)

# Initialize Docker client and managers
try:
    docker_client = docker.from_env()
    container_manager = ContainerManager(docker_client)
    example_flows = ExampleFlows(container_manager)
    logger.info("🐋 Docker client initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Docker client: {e}")
    docker_client = None

# Routes
@app.route('/')
def index():
    """Main dashboard showing container status and available examples"""
    return render_template('index.html')

@app.route('/containers')
def containers():
    """Container management page"""
    return render_template('containers.html')

@app.route('/logs')
def logs():
    """Log viewing interface"""
    return render_template('logs.html')

# API Routes
@app.route('/api/status')
def api_status():
    """System status and health check"""
    if not docker_client:
        return jsonify({
            'status': 'error',
            'message': 'Docker client not initialized',
            'timestamp': datetime.now().isoformat()
        }), 503
    
    try:
        # Get Docker info
        info = docker_client.info()
        containers = docker_client.containers.list(all=True)
        
        return jsonify({
            'status': 'healthy',
            'docker': {
                'version': info.get('ServerVersion', 'unknown'),
                'containers': {
                    'total': len(containers),
                    'running': len([c for c in containers if c.status == 'running']),
                    'stopped': len([c for c in containers if c.status != 'running'])
                }
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/containers')
def api_containers():
    """List all containers with educational information"""
    if not container_manager:
        return jsonify({'error': 'Container manager not initialized'}), 503
    
    try:
        containers = container_manager.list_containers()
        return jsonify({
            'containers': containers,
            'count': len(containers)
        })
    except Exception as e:
        logger.error(f"Error listing containers: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/containers/spawn', methods=['POST'])
def api_spawn_container():
    """Spawn a new container with educational feedback"""
    if not container_manager:
        return jsonify({'error': 'Container manager not initialized'}), 503
    
    data = request.json
    image = data.get('image', os.getenv('DEFAULT_CONTAINER_IMAGE', 'ubuntu:latest'))
    name = data.get('name')
    command = data.get('command')
    
    try:
        container = container_manager.spawn_container(
            image=image,
            name=name,
            command=command
        )
        
        return jsonify({
            'success': True,
            'container': {
                'id': container.short_id,
                'name': container.name,
                'status': container.status,
                'image': image
            },
            'educational_tip': f"✨ Container '{container.name}' created! Use 'docker ps' to see it."
        })
    except Exception as e:
        logger.error(f"Error spawning container: {e}")
        return jsonify({
            'error': str(e),
            'educational_tip': "💡 Check if the image exists and Docker daemon is running"
        }), 500

@app.route('/api/containers/<container_id>/action', methods=['POST'])
def api_container_action(container_id):
    """Perform actions on containers (start, stop, restart, remove)"""
    if not container_manager:
        return jsonify({'error': 'Container manager not initialized'}), 503
    
    action = request.json.get('action')
    valid_actions = ['start', 'stop', 'restart', 'remove']
    
    if action not in valid_actions:
        return jsonify({
            'error': f'Invalid action. Valid actions: {", ".join(valid_actions)}'
        }), 400
    
    try:
        result = container_manager.container_action(container_id, action)
        return jsonify({
            'success': True,
            'action': action,
            'container_id': container_id,
            'result': result,
            'educational_tip': f"✅ Container {action} successful!"
        })
    except Exception as e:
        logger.error(f"Error performing {action} on container {container_id}: {e}")
        return jsonify({
            'error': str(e),
            'educational_tip': f"💡 Make sure the container exists and can be {action}ed"
        }), 500

@app.route('/api/containers/<container_id>/logs')
def api_container_logs(container_id):
    """Stream container logs for educational purposes"""
    if not container_manager:
        return jsonify({'error': 'Container manager not initialized'}), 503
    
    try:
        logs = container_manager.get_container_logs(container_id)
        return jsonify({
            'container_id': container_id,
            'logs': logs,
            'educational_tip': "📋 These are the container's stdout and stderr outputs"
        })
    except Exception as e:
        logger.error(f"Error getting logs for container {container_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples')
def api_list_examples():
    """List available example flows for students"""
    if not example_flows:
        return jsonify({'error': 'Example flows not initialized'}), 503
    
    examples = example_flows.list_examples()
    return jsonify({
        'examples': examples,
        'count': len(examples)
    })

@app.route('/api/examples/<flow_name>', methods=['POST'])
def api_execute_example(flow_name):
    """Execute an example flow with educational output"""
    if not example_flows:
        return jsonify({'error': 'Example flows not initialized'}), 503
    
    params = request.json or {}
    
    try:
        result = example_flows.execute_flow(flow_name, **params)
        return jsonify({
            'success': True,
            'flow': flow_name,
            'result': result,
            'educational_tip': "🎓 Check the logs to understand what happened!"
        })
    except Exception as e:
        logger.error(f"Error executing example flow {flow_name}: {e}")
        return jsonify({
            'error': str(e),
            'educational_tip': "💡 Read the error message carefully - it's trying to teach you something!"
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Educational 404 error handler"""
    return jsonify({
        'error': 'Not found',
        'educational_tip': '🔍 This endpoint does not exist. Check the API documentation!'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Educational 500 error handler"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'educational_tip': '🔧 Something went wrong. Check the logs for details!'
    }), 500

# Development server with auto-reload
if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    
    # Welcome message for students
    print("\n" + "="*50)
    print("🎓 Container Poker - Learning Platform")
    print("="*50)
    print(f"📚 Starting server at http://{host}:{port}")
    print("💡 Edit files in ./src - they'll auto-reload!")
    print("🔍 Check logs for educational tips")
    print("="*50 + "\n")
    
    # Run the Flask development server
    app.run(host=host, port=port, debug=debug)