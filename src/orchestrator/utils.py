"""
Utility functions for the Container Poker platform
Logging, error handling, and helper functions
"""

import logging
import sys
import os
from functools import wraps
from datetime import datetime
import json


def setup_logging(app=None):
    """
    Set up logging with educational formatting
    
    Args:
        app: Flask app instance (optional)
        
    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger('containerpoker')
    logger.setLevel(logging.DEBUG if os.getenv('DEBUG_LOGS', 'true') == 'true' else logging.INFO)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler with educational formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Educational format that's easy to read
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler for persistent logs
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = logging.FileHandler(
        f'logs/containerpoker_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Add Flask app logger if provided
    if app:
        app.logger.handlers = logger.handlers
        app.logger.setLevel(logger.level)
    
    logger.info("="*50)
    logger.info("🎓 Container Poker Logging Initialized")
    logger.info("📝 Logs are educational - read them to learn!")
    logger.info("="*50)
    
    return logger


def error_handler(func):
    """
    Decorator for educational error handling
    Provides clear error messages that help students learn
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger('containerpoker')
            
            # Log the error with educational context
            logger.error(f"❌ Error in {func.__name__}: {str(e)}")
            
            # Provide educational hints based on error type
            if "permission denied" in str(e).lower():
                logger.info("💡 TIP: This might be a Docker socket permission issue")
                logger.info("    Try: sudo usermod -aG docker $USER")
                
            elif "cannot connect to docker" in str(e).lower():
                logger.info("💡 TIP: Is Docker running?")
                logger.info("    Try: sudo systemctl start docker")
                
            elif "image not found" in str(e).lower():
                logger.info("💡 TIP: The Docker image doesn't exist locally")
                logger.info("    Try: docker pull <image-name>")
                
            elif "container not found" in str(e).lower():
                logger.info("💡 TIP: The container might have been removed")
                logger.info("    Try: docker ps -a (to see all containers)")
                
            elif "port is already allocated" in str(e).lower():
                logger.info("💡 TIP: Another process is using this port")
                logger.info("    Try: lsof -i :PORT or netstat -tulpn | grep PORT")
            
            # Re-raise the exception
            raise
    
    return wrapper


def format_container_info(container):
    """
    Format container information in an educational way
    
    Args:
        container: Docker container object
        
    Returns:
        Formatted dictionary with container information
    """
    try:
        info = {
            'id': container.short_id,
            'name': container.name,
            'status': container.status,
            'image': container.image.tags[0] if container.image.tags else 'untagged',
            'created': container.attrs['Created'],
            'platform': container.attrs.get('Platform', 'unknown'),
        }
        
        # Add networking information
        networks = container.attrs['NetworkSettings']['Networks']
        info['networks'] = list(networks.keys())
        
        # Add resource usage if running
        if container.status == 'running':
            try:
                stats = container.stats(stream=False)
                info['resource_usage'] = {
                    'cpu_percent': calculate_cpu_percent(stats),
                    'memory_usage': format_bytes(
                        stats['memory_stats'].get('usage', 0)
                    ),
                    'memory_limit': format_bytes(
                        stats['memory_stats'].get('limit', 0)
                    )
                }
            except:
                info['resource_usage'] = 'Unable to get stats'
        
        return info
        
    except Exception as e:
        logger = logging.getLogger('containerpoker')
        logger.error(f"Error formatting container info: {e}")
        return {'error': str(e)}


def calculate_cpu_percent(stats):
    """
    Calculate CPU percentage from Docker stats
    Educational function showing how Docker calculates CPU usage
    """
    try:
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                   stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                      stats['precpu_stats']['system_cpu_usage']
        
        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * 100.0
            return round(cpu_percent, 2)
        return 0.0
    except:
        return 0.0


def format_bytes(bytes_value):
    """
    Format bytes into human-readable format
    Educational function showing unit conversion
    """
    try:
        bytes_value = int(bytes_value)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    except:
        return "0 B"


def validate_image_name(image_name):
    """
    Validate Docker image name format
    Educational function showing Docker naming conventions
    """
    import re
    
    # Docker image name pattern
    # [registry/]namespace/repository[:tag]
    pattern = r'^(?:(?:[a-zA-Z0-9.-]+(?::[0-9]+)?/)?[a-z0-9-_./]+(?::[a-zA-Z0-9.-_]+)?)?$'
    
    if not image_name:
        return False, "Image name cannot be empty"
    
    if not re.match(pattern, image_name):
        return False, ("Invalid image name format. "
                      "Expected: [registry/]namespace/repository[:tag]")
    
    # Educational checks
    if ':latest' not in image_name and ':' not in image_name:
        logger = logging.getLogger('containerpoker')
        logger.info("💡 TIP: No tag specified, Docker will use ':latest'")
    
    return True, "Valid image name"


def parse_command(command_string):
    """
    Parse command string into list format for Docker
    Educational function showing command parsing
    """
    import shlex
    
    if not command_string:
        return None
    
    try:
        # Use shlex to properly parse shell-like syntax
        parsed = shlex.split(command_string)
        
        logger = logging.getLogger('containerpoker')
        logger.debug(f"📝 Parsed command: {command_string} -> {parsed}")
        
        return parsed
    except ValueError as e:
        raise ValueError(f"Invalid command syntax: {e}")


def create_safe_container_name(base_name=None):
    """
    Create a safe container name with timestamp
    Educational function showing Docker naming rules
    """
    import re
    from datetime import datetime
    
    if not base_name:
        base_name = "containerpoker"
    
    # Docker container naming rules:
    # - Must match [a-zA-Z0-9][a-zA-Z0-9_.-]*
    # - Cannot start with hyphen or period
    safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '', base_name)
    
    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    container_name = f"{safe_name}_{timestamp}"
    
    logger = logging.getLogger('containerpoker')
    logger.debug(f"📝 Generated container name: {container_name}")
    
    return container_name


def get_container_health_status(container):
    """
    Get detailed health status of a container
    Educational function showing health check concepts
    """
    try:
        health = container.attrs.get('State', {}).get('Health')
        
        if not health:
            return {
                'status': 'no_healthcheck',
                'message': 'No health check configured',
                'educational_tip': ('💡 Health checks help monitor container health. '
                                   'Add HEALTHCHECK to your Dockerfile!')
            }
        
        status = health.get('Status', 'unknown')
        failing_streak = health.get('FailingStreak', 0)
        
        # Get last health check log
        logs = health.get('Log', [])
        last_check = logs[-1] if logs else None
        
        return {
            'status': status,
            'failing_streak': failing_streak,
            'last_check': last_check,
            'educational_tip': get_health_tip(status, failing_streak)
        }
        
    except Exception as e:
        logger = logging.getLogger('containerpoker')
        logger.error(f"Error getting health status: {e}")
        return {'status': 'error', 'message': str(e)}


def get_health_tip(status, failing_streak):
    """
    Provide educational tips based on health status
    """
    tips = {
        'healthy': "✅ Container is healthy and passing health checks",
        'unhealthy': f"❌ Container is failing health checks ({failing_streak} times)",
        'starting': "🔄 Container is still starting up, health checks pending"
    }
    
    if status == 'unhealthy':
        tips['unhealthy'] += ("\n💡 TIP: Check logs to see why health checks are failing. "
                             "Common issues: service not ready, wrong health check command")
    
    return tips.get(status, f"Unknown health status: {status}")