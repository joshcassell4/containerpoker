"""
Core Container Management Module
Handles basic container operations with educational error messages
"""

import docker
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class ContainerManager:
    """
    Educational container manager that wraps Docker operations
    with clear error messages and learning opportunities
    """
    
    def __init__(self, docker_client: docker.DockerClient):
        """
        Initialize the container manager
        
        Args:
            docker_client: Initialized Docker client instance
        """
        self.client = docker_client
        self.containers_created = []  # Track containers for cleanup
        logger.info("🎓 ContainerManager initialized - ready to orchestrate!")
    
    def list_containers(self, all: bool = True) -> List[Dict[str, Any]]:
        """
        List all containers with educational information
        
        Args:
            all: If True, show all containers (not just running)
            
        Returns:
            List of container information dictionaries
        """
        try:
            containers = self.client.containers.list(all=all)
            
            container_list = []
            for container in containers:
                # Get detailed container info
                container_info = {
                    'id': container.short_id,
                    'name': container.name,
                    'image': container.image.tags[0] if container.image.tags else 'unknown',
                    'status': container.status,
                    'created': container.attrs['Created'],
                    'command': container.attrs['Config']['Cmd'],
                    'ports': container.attrs['NetworkSettings']['Ports'],
                    'labels': container.labels,
                    'educational_info': {
                        'state_explanation': self._explain_container_state(container.status),
                        'next_actions': self._suggest_next_actions(container.status)
                    }
                }
                container_list.append(container_info)
            
            logger.info(f"📋 Listed {len(container_list)} containers")
            return container_list
            
        except Exception as e:
            logger.error(f"❌ Error listing containers: {e}")
            raise Exception(f"Failed to list containers: {str(e)}")
    
    def spawn_container(self, image: str, name: Optional[str] = None, 
                       command: Optional[str] = None, **kwargs) -> docker.models.containers.Container:
        """
        Spawn a new container with educational feedback
        
        Args:
            image: Docker image to use
            name: Optional container name
            command: Optional command to run
            **kwargs: Additional Docker run parameters
            
        Returns:
            Created container instance
        """
        try:
            # Educational logging
            logger.info(f"🚀 Spawning container from image: {image}")
            
            # Set default parameters for educational purposes
            run_params = {
                'image': image,
                'detach': True,  # Run in background
                'tty': True,     # Allocate pseudo-TTY
                'stdin_open': True,  # Keep stdin open
                'labels': {
                    'created_by': 'containerpoker',
                    'educational': 'true',
                    'created_at': datetime.now().isoformat()
                }
            }
            
            # Add optional parameters
            if name:
                run_params['name'] = name
            if command:
                run_params['command'] = command
                
            # Merge with any additional kwargs
            run_params.update(kwargs)
            
            # Create the container
            container = self.client.containers.run(**run_params)
            
            # Track for cleanup
            self.containers_created.append(container.id)
            
            logger.info(f"✅ Container '{container.name}' created successfully!")
            logger.info(f"💡 TIP: Use 'docker logs {container.short_id}' to see output")
            
            return container
            
        except docker.errors.ImageNotFound:
            error_msg = (f"Image '{image}' not found locally. "
                        f"Try 'docker pull {image}' first!")
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        except docker.errors.APIError as e:
            error_msg = f"Docker API error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        except Exception as e:
            logger.error(f"❌ Unexpected error spawning container: {e}")
            raise
    
    def container_action(self, container_id: str, action: str) -> Dict[str, Any]:
        """
        Perform an action on a container (start, stop, restart, remove)
        
        Args:
            container_id: Container ID or name
            action: Action to perform
            
        Returns:
            Result dictionary with educational information
        """
        try:
            container = self.client.containers.get(container_id)
            
            # Perform the requested action
            if action == 'start':
                container.start()
                message = f"Container '{container.name}' started"
                tip = "Use 'docker logs -f' to follow the output"
                
            elif action == 'stop':
                container.stop()
                message = f"Container '{container.name}' stopped"
                tip = "Container still exists - use 'remove' to delete it"
                
            elif action == 'restart':
                container.restart()
                message = f"Container '{container.name}' restarted"
                tip = "This is equivalent to 'stop' then 'start'"
                
            elif action == 'remove':
                # Stop first if running
                if container.status == 'running':
                    container.stop()
                container.remove()
                message = f"Container '{container.name}' removed"
                tip = "Container and its data are now gone"
                
                # Remove from tracking
                if container.id in self.containers_created:
                    self.containers_created.remove(container.id)
            
            else:
                raise ValueError(f"Unknown action: {action}")
            
            logger.info(f"✅ {message}")
            
            return {
                'message': message,
                'educational_tip': tip,
                'container_state': container.status if action != 'remove' else 'removed'
            }
            
        except docker.errors.NotFound:
            error_msg = (f"Container '{container_id}' not found. "
                        "Use 'docker ps -a' to see all containers")
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        except Exception as e:
            logger.error(f"❌ Error performing {action} on container: {e}")
            raise
    
    def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        """
        Get container logs with educational context
        
        Args:
            container_id: Container ID or name
            tail: Number of lines to return from the end
            
        Returns:
            Container logs as string
        """
        try:
            container = self.client.containers.get(container_id)
            
            # Get logs
            logs = container.logs(tail=tail, timestamps=True).decode('utf-8')
            
            if not logs:
                logs = ("📭 No logs yet. The container might be:\n"
                       "1. Still starting up\n"
                       "2. Not producing any output\n"
                       "3. Writing to stderr instead of stdout")
            
            return logs
            
        except docker.errors.NotFound:
            error_msg = f"Container '{container_id}' not found"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        except Exception as e:
            logger.error(f"❌ Error getting logs: {e}")
            raise
    
    def execute_command(self, container_id: str, command: str, 
                       workdir: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a command in a running container
        
        Args:
            container_id: Container ID or name
            command: Command to execute
            workdir: Optional working directory
            
        Returns:
            Command output and exit code
        """
        try:
            container = self.client.containers.get(container_id)
            
            # Check if container is running
            if container.status != 'running':
                raise Exception(f"Container is {container.status}, not running")
            
            # Execute the command
            exec_params = {'cmd': command}
            if workdir:
                exec_params['workdir'] = workdir
                
            result = container.exec_run(**exec_params)
            
            return {
                'exit_code': result.exit_code,
                'output': result.output.decode('utf-8'),
                'success': result.exit_code == 0,
                'educational_tip': self._explain_exit_code(result.exit_code)
            }
            
        except Exception as e:
            logger.error(f"❌ Error executing command: {e}")
            raise
    
    def cleanup_all(self):
        """
        Clean up all containers created by this manager
        Educational method to teach resource cleanup
        """
        logger.info("🧹 Starting cleanup of educational containers...")
        
        cleaned = 0
        errors = []
        
        for container_id in self.containers_created[:]:  # Copy list to avoid modification issues
            try:
                container = self.client.containers.get(container_id)
                if container.status == 'running':
                    container.stop()
                container.remove()
                self.containers_created.remove(container_id)
                cleaned += 1
                logger.info(f"✅ Removed container {container.short_id}")
            except Exception as e:
                errors.append(f"Failed to remove {container_id}: {e}")
        
        if errors:
            logger.warning(f"⚠️ Some containers couldn't be removed: {errors}")
        
        logger.info(f"🎯 Cleanup complete! Removed {cleaned} containers")
        
        return {
            'cleaned': cleaned,
            'errors': errors,
            'educational_tip': "Always clean up resources to avoid 'container sprawl'!"
        }
    
    # Educational helper methods
    def _explain_container_state(self, status: str) -> str:
        """Explain what a container state means"""
        explanations = {
            'running': "Container is actively executing",
            'exited': "Container finished execution (check exit code)",
            'paused': "Container is paused (frozen in time)",
            'restarting': "Container is restarting (check restart policy)",
            'dead': "Container is dead (unrecoverable error)",
            'created': "Container created but not started yet"
        }
        return explanations.get(status, f"Unknown state: {status}")
    
    def _suggest_next_actions(self, status: str) -> List[str]:
        """Suggest what a student might do next"""
        suggestions = {
            'running': ["View logs", "Execute commands", "Stop container"],
            'exited': ["Check logs for errors", "Restart container", "Remove container"],
            'created': ["Start container", "Remove container"],
            'paused': ["Unpause container", "Stop container"],
            'dead': ["Check logs", "Remove and recreate"]
        }
        return suggestions.get(status, ["Check container status"])
    
    def _explain_exit_code(self, exit_code: int) -> str:
        """Explain what an exit code means"""
        if exit_code == 0:
            return "✅ Command succeeded (exit code 0)"
        elif exit_code == 1:
            return "❌ General error (exit code 1)"
        elif exit_code == 126:
            return "❌ Command not executable (exit code 126)"
        elif exit_code == 127:
            return "❌ Command not found (exit code 127)"
        elif exit_code == 130:
            return "⚠️ Terminated by Ctrl+C (exit code 130)"
        else:
            return f"Exit code {exit_code} - check command documentation"