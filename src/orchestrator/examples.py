"""
Educational Example Flows for Container Orchestration
Demonstrates different patterns using pexpect for automation and dockerpty for interaction
"""

import logging
import time
import pexpect
import dockerpty
import docker
from typing import Dict, Any, List, Optional
import json
import os

logger = logging.getLogger(__name__)


class ExampleFlows:
    """
    Collection of educational example flows demonstrating container orchestration patterns
    Uses pexpect for automated workflows and dockerpty for interactive sessions
    """
    
    def __init__(self, container_manager):
        """
        Initialize example flows with a container manager
        
        Args:
            container_manager: ContainerManager instance
        """
        self.manager = container_manager
        self.client = container_manager.client
        
        # Register available examples
        self.examples = {
            'hello_world': {
                'name': 'Hello World Container',
                'description': 'Basic container lifecycle - create, run, and cleanup',
                'difficulty': 'beginner',
                'tool': 'docker-sdk',
                'function': self.hello_world_container
            },
            'interactive_shell': {
                'name': 'Interactive Shell Session',
                'description': 'Real terminal session using dockerpty',
                'difficulty': 'beginner',
                'tool': 'dockerpty',
                'function': self.interactive_shell_example
            },
            'automated_commands': {
                'name': 'Automated Command Sequence',
                'description': 'Execute commands with pexpect pattern matching',
                'difficulty': 'intermediate',
                'tool': 'pexpect',
                'function': self.automated_commands_example
            },
            'multi_container': {
                'name': 'Multi-Container Dependencies',
                'description': 'Coordinate multiple containers with dependencies',
                'difficulty': 'intermediate',
                'tool': 'pexpect',
                'function': self.dependency_orchestration
            },
            'log_monitoring': {
                'name': 'Log Monitoring & Events',
                'description': 'Monitor logs and respond to events',
                'difficulty': 'intermediate',
                'tool': 'pexpect',
                'function': self.log_monitoring_example
            },
            'health_recovery': {
                'name': 'Health Checks & Recovery',
                'description': 'Implement health monitoring and auto-recovery',
                'difficulty': 'advanced',
                'tool': 'pexpect',
                'function': self.health_check_recovery
            },
            'networking': {
                'name': 'Container Networking',
                'description': 'Create networks and connect containers',
                'difficulty': 'advanced',
                'tool': 'docker-sdk',
                'function': self.networking_examples
            },
            'volume_management': {
                'name': 'Volume & Data Management',
                'description': 'Persistent storage and data sharing',
                'difficulty': 'intermediate',
                'tool': 'docker-sdk',
                'function': self.volume_management_example
            }
        }
    
    def list_examples(self) -> List[Dict[str, Any]]:
        """List all available examples with metadata"""
        return [
            {
                'id': key,
                'name': value['name'],
                'description': value['description'],
                'difficulty': value['difficulty'],
                'tool': value['tool']
            }
            for key, value in self.examples.items()
        ]
    
    def execute_flow(self, flow_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a specific example flow
        
        Args:
            flow_name: Name of the flow to execute
            **kwargs: Additional parameters for the flow
            
        Returns:
            Result dictionary with educational information
        """
        if flow_name not in self.examples:
            raise ValueError(f"Unknown example flow: {flow_name}")
        
        example = self.examples[flow_name]
        logger.info(f"🎓 Executing example: {example['name']}")
        logger.info(f"📚 Tool used: {example['tool']}")
        
        try:
            # Execute the example function
            result = example['function'](**kwargs)
            
            return {
                'success': True,
                'flow': flow_name,
                'result': result,
                'educational_notes': self._get_educational_notes(flow_name)
            }
            
        except Exception as e:
            logger.error(f"❌ Example failed: {e}")
            return {
                'success': False,
                'flow': flow_name,
                'error': str(e),
                'debugging_tips': self._get_debugging_tips(flow_name, str(e))
            }
    
    # Example 1: Hello World Container (Basic Docker SDK)
    def hello_world_container(self, message: str = "Hello from Container Poker!") -> Dict[str, Any]:
        """
        LEARNING GOAL: Understand basic container lifecycle
        
        This example demonstrates:
        - Creating a container from an image
        - Running a simple command
        - Capturing output
        - Proper cleanup
        
        Tool: Docker SDK (direct API calls)
        """
        logger.info("📖 Example 1: Basic container lifecycle")
        
        # Step 1: Create and run container
        logger.info("Step 1: Creating container with echo command")
        container = self.manager.spawn_container(
            image='ubuntu:latest',
            command=f'echo "{message}"',
            remove=True,  # Auto-remove when done
            name='hello_world_demo'
        )
        
        # Step 2: Wait for completion
        logger.info("Step 2: Waiting for container to complete")
        result = container.wait()
        
        # Step 3: Get logs
        logger.info("Step 3: Retrieving container output")
        logs = container.logs().decode('utf-8').strip()
        
        # Educational output
        return {
            'container_id': container.short_id,
            'exit_code': result['StatusCode'],
            'output': logs,
            'lesson': (
                "This example showed the basic container lifecycle:\n"
                "1. Create container from image (ubuntu:latest)\n"
                "2. Run command (echo)\n"
                "3. Capture output from logs\n"
                "4. Container auto-removed due to 'remove=True'"
            )
        }
    
    # Example 2: Interactive Shell with dockerpty
    def interactive_shell_example(self, image: str = 'ubuntu:latest') -> Dict[str, Any]:
        """
        LEARNING GOAL: Real-time container interaction
        
        Demonstrates dockerpty for interactive sessions:
        - Attaching to container stdin/stdout
        - Handling user input/output
        - Managing session lifecycle
        
        Tool: dockerpty (pseudo-TTY for real terminal experience)
        """
        logger.info("📖 Example 2: Interactive shell session with dockerpty")
        
        # Create container but don't start it yet
        logger.info("Creating container for interactive session")
        container = self.client.containers.create(
            image=image,
            command='/bin/bash',
            tty=True,
            stdin_open=True,
            name='interactive_demo'
        )
        
        try:
            # Start container
            container.start()
            logger.info(f"✅ Container {container.short_id} started")
            
            # Note: In a real web app, we'd need to handle this differently
            # This is for demonstration purposes
            logger.info("💡 dockerpty would attach here for interactive session")
            logger.info("   In production, use WebSockets for browser-based terminals")
            
            # For demo, just show what would happen
            demo_commands = [
                "ls -la",
                "echo 'Hello from interactive session!'",
                "ps aux",
                "exit"
            ]
            
            return {
                'container_id': container.short_id,
                'demo_commands': demo_commands,
                'lesson': (
                    "dockerpty provides a real terminal experience:\n"
                    "- Full TTY with colors and cursor control\n"
                    "- Handles window resize and signals (Ctrl+C)\n"
                    "- Perfect for interactive debugging\n"
                    "- In web apps, combine with WebSockets for browser terminals"
                ),
                'note': "Run 'make shell' to try interactive mode yourself!"
            }
            
        finally:
            # Cleanup
            try:
                container.stop()
                container.remove()
                logger.info("🧹 Cleaned up interactive container")
            except:
                pass
    
    # Example 3: Automated Commands with pexpect
    def automated_commands_example(self) -> Dict[str, Any]:
        """
        LEARNING GOAL: Automate complex command sequences
        
        Shows how to:
        - Send commands to containers
        - Wait for specific output patterns
        - Parse command results
        - Handle command failures
        
        Tool: pexpect (expect-style automation)
        """
        logger.info("📖 Example 3: Automated command sequences with pexpect")
        
        # Create a container for automation
        container = self.manager.spawn_container(
            image='ubuntu:latest',
            command='/bin/bash',
            name='automation_demo'
        )
        
        try:
            # Use pexpect to automate interactions
            logger.info("🤖 Starting pexpect automation")
            
            # Spawn docker exec process
            cmd = f'docker exec -it {container.id} /bin/bash'
            child = pexpect.spawn(cmd, encoding='utf-8', timeout=30)
            
            results = []
            
            # Wait for prompt
            child.expect(r'root@.*#')
            logger.info("✅ Got shell prompt")
            
            # Command 1: Update package list
            logger.info("📝 Running: apt-get update")
            child.sendline('apt-get update -qq')
            child.expect(r'root@.*#', timeout=60)
            results.append("Package list updated")
            
            # Command 2: Install curl
            logger.info("📝 Running: apt-get install curl")
            child.sendline('apt-get install -y curl > /dev/null 2>&1')
            child.expect(r'root@.*#', timeout=60)
            results.append("curl installed")
            
            # Command 3: Test curl
            logger.info("📝 Testing curl installation")
            child.sendline('curl --version')
            child.expect(r'curl ([0-9.]+)')
            curl_version = child.match.group(1)
            child.expect(r'root@.*#')
            results.append(f"curl version {curl_version} verified")
            
            # Command 4: Create a file
            logger.info("📝 Creating test file")
            child.sendline('echo "Automation successful!" > /tmp/test.txt')
            child.expect(r'root@.*#')
            
            # Command 5: Verify file
            child.sendline('cat /tmp/test.txt')
            child.expect('Automation successful!')
            child.expect(r'root@.*#')
            results.append("Test file created and verified")
            
            # Exit
            child.sendline('exit')
            child.expect(pexpect.EOF)
            
            return {
                'container_id': container.short_id,
                'automation_results': results,
                'lesson': (
                    "pexpect enables powerful automation:\n"
                    "1. Pattern matching with expect()\n"
                    "2. Send commands with sendline()\n"
                    "3. Extract data with regex groups\n"
                    "4. Handle timeouts and errors\n"
                    "Perfect for CI/CD and testing!"
                ),
                'patterns_used': [
                    r'root@.*#' + ' (shell prompt)',
                    r'curl ([0-9.]+)' + ' (version extraction)',
                    'Automation successful!' + ' (exact match)'
                ]
            }
            
        except pexpect.TIMEOUT:
            logger.error("❌ Command timed out")
            raise Exception("Automation timed out - check container logs")
            
        except Exception as e:
            logger.error(f"❌ Automation failed: {e}")
            raise
            
        finally:
            # Cleanup
            self.manager.container_action(container.id, 'remove')
    
    # Example 4: Multi-Container Dependencies
    def dependency_orchestration(self) -> Dict[str, Any]:
        """
        LEARNING GOAL: Container coordination patterns
        
        Demonstrates:
        - Starting containers in correct order
        - Health checks and readiness probes
        - Inter-container communication
        - Graceful shutdown sequences
        
        Tool: pexpect + Docker SDK
        """
        logger.info("📖 Example 4: Multi-container dependency management")
        
        network_name = 'containerpoker_net'
        containers_created = []
        
        try:
            # Step 1: Create network
            logger.info("Step 1: Creating custom network")
            network = self.client.networks.create(
                network_name,
                driver='bridge'
            )
            
            # Step 2: Start database container
            logger.info("Step 2: Starting database container")
            db_container = self.client.containers.run(
                'postgres:alpine',
                name='demo_db',
                environment={
                    'POSTGRES_PASSWORD': 'secretpass',
                    'POSTGRES_DB': 'demoapp'
                },
                network=network_name,
                detach=True
            )
            containers_created.append(db_container)
            
            # Step 3: Wait for database to be ready
            logger.info("Step 3: Waiting for database readiness")
            max_attempts = 30
            for i in range(max_attempts):
                try:
                    # Use pexpect to check if postgres is ready
                    check_cmd = (f'docker exec {db_container.id} '
                               'pg_isready -U postgres')
                    result = pexpect.run(check_cmd, timeout=5, encoding='utf-8')
                    
                    if 'accepting connections' in result:
                        logger.info("✅ Database is ready!")
                        break
                except:
                    pass
                
                time.sleep(1)
                if i == max_attempts - 1:
                    raise Exception("Database failed to start")
            
            # Step 4: Start application container
            logger.info("Step 4: Starting application container")
            app_container = self.client.containers.run(
                'nginx:alpine',
                name='demo_app',
                network=network_name,
                ports={'80/tcp': 8080},
                environment={
                    'DB_HOST': 'demo_db',
                    'DB_NAME': 'demoapp'
                },
                detach=True
            )
            containers_created.append(app_container)
            
            # Step 5: Verify connectivity
            logger.info("Step 5: Verifying inter-container communication")
            ping_cmd = f'docker exec {app_container.id} ping -c 1 demo_db'
            result = pexpect.run(ping_cmd, timeout=5, encoding='utf-8')
            
            connectivity_ok = '1 packets transmitted, 1 received' in result
            
            return {
                'network': network_name,
                'containers': {
                    'database': db_container.short_id,
                    'application': app_container.short_id
                },
                'connectivity_test': 'passed' if connectivity_ok else 'failed',
                'lesson': (
                    "Multi-container orchestration patterns:\n"
                    "1. Create isolated network for security\n"
                    "2. Start dependencies first (database)\n"
                    "3. Wait for readiness before proceeding\n"
                    "4. Use service names for discovery\n"
                    "5. Clean shutdown in reverse order"
                ),
                'tips': [
                    "Use health checks in production",
                    "Consider using docker-compose for complex setups",
                    "Always handle startup failures gracefully"
                ]
            }
            
        finally:
            # Cleanup in reverse order
            logger.info("🧹 Cleaning up multi-container setup")
            for container in reversed(containers_created):
                try:
                    container.stop()
                    container.remove()
                except:
                    pass
            
            try:
                network.remove()
            except:
                pass
    
    # Example 5: Log Monitoring and Event Response
    def log_monitoring_example(self) -> Dict[str, Any]:
        """
        LEARNING GOAL: Event-driven container management
        
        Teaches:
        - Real-time log streaming
        - Pattern matching in logs
        - Automated responses to events
        - Log aggregation techniques
        
        Tool: pexpect for pattern matching
        """
        logger.info("📖 Example 5: Log monitoring and event response")
        
        # Create a container that generates interesting logs
        container = self.manager.spawn_container(
            image='ubuntu:latest',
            command='bash -c "for i in {1..10}; do echo Log entry $i; sleep 1; done"',
            name='log_demo'
        )
        
        try:
            # Monitor logs with pexpect
            log_cmd = f'docker logs -f {container.id}'
            child = pexpect.spawn(log_cmd, encoding='utf-8', timeout=30)
            
            events_detected = []
            responses = []
            
            # Pattern matching for different log entries
            patterns = [
                ('Log entry 3', 'Detected milestone: 30% complete'),
                ('Log entry 5', 'Halfway point reached!'),
                ('Log entry 8', 'Warning: Approaching completion'),
                ('Log entry 10', 'Process completed successfully')
            ]
            
            for pattern, response in patterns:
                try:
                    child.expect(pattern, timeout=15)
                    events_detected.append(pattern)
                    responses.append(response)
                    logger.info(f"📊 Event detected: {pattern} -> {response}")
                except pexpect.TIMEOUT:
                    logger.warning(f"⚠️ Timeout waiting for: {pattern}")
            
            return {
                'container_id': container.short_id,
                'events_detected': events_detected,
                'automated_responses': responses,
                'lesson': (
                    "Log monitoring enables reactive orchestration:\n"
                    "1. Stream logs in real-time\n"
                    "2. Match patterns for events\n"
                    "3. Trigger automated responses\n"
                    "4. Aggregate logs for analysis\n"
                    "Essential for production monitoring!"
                ),
                'use_cases': [
                    "Error detection and alerting",
                    "Performance monitoring",
                    "Security event detection",
                    "Automated scaling triggers"
                ]
            }
            
        finally:
            # Cleanup
            self.manager.container_action(container.id, 'remove')
    
    # Example 6: Health Checks and Recovery
    def health_check_recovery(self) -> Dict[str, Any]:
        """
        LEARNING GOAL: Production-ready reliability patterns
        
        Covers:
        - Defining custom health checks
        - Implementing restart policies
        - Cascading failure handling
        - Monitoring container resources
        
        Tool: Docker SDK + pexpect
        """
        logger.info("📖 Example 6: Health monitoring and auto-recovery")
        
        # Create a container with health check
        health_check = docker.types.Healthcheck(
            test=["CMD", "curl", "-f", "http://localhost/health"],
            interval=5000000000,  # 5 seconds in nanoseconds
            timeout=3000000000,   # 3 seconds
            retries=3,
            start_period=10000000000  # 10 seconds
        )
        
        container = self.client.containers.run(
            'nginx:alpine',
            name='health_demo',
            detach=True,
            healthcheck=health_check,
            restart_policy={"Name": "on-failure", "MaximumRetryCount": 3}
        )
        
        try:
            health_history = []
            
            # Monitor health status
            logger.info("🏥 Monitoring container health")
            for i in range(6):
                container.reload()
                health_status = container.attrs['State'].get('Health', {}).get('Status', 'none')
                health_history.append({
                    'check': i + 1,
                    'status': health_status,
                    'timestamp': time.strftime('%H:%M:%S')
                })
                logger.info(f"Health check {i + 1}: {health_status}")
                time.sleep(3)
            
            # Simulate failure and recovery
            logger.info("💥 Simulating failure scenario")
            container.exec_run('nginx -s stop')
            time.sleep(5)
            
            # Check if container recovered
            container.reload()
            final_status = container.status
            
            return {
                'container_id': container.short_id,
                'health_history': health_history,
                'restart_policy': 'on-failure (max 3 attempts)',
                'final_status': final_status,
                'lesson': (
                    "Health checks ensure reliability:\n"
                    "1. Define health check commands\n"
                    "2. Set appropriate intervals and timeouts\n"
                    "3. Configure restart policies\n"
                    "4. Monitor health transitions\n"
                    "Critical for production deployments!"
                ),
                'best_practices': [
                    "Use lightweight health checks",
                    "Set realistic timeouts",
                    "Log health check failures",
                    "Alert on repeated failures"
                ]
            }
            
        finally:
            # Cleanup
            container.stop()
            container.remove()
    
    # Example 7: Container Networking
    def networking_examples(self) -> Dict[str, Any]:
        """
        LEARNING GOAL: Container networking concepts
        
        Explores:
        - Creating custom networks
        - Container-to-container communication
        - Port mapping strategies
        - Network isolation patterns
        
        Tool: Docker SDK
        """
        logger.info("📖 Example 7: Container networking patterns")
        
        networks_created = []
        containers_created = []
        
        try:
            # Create different network types
            logger.info("🌐 Creating custom networks")
            
            # Bridge network
            bridge_net = self.client.networks.create(
                'demo_bridge',
                driver='bridge',
                internal=False
            )
            networks_created.append(bridge_net)
            
            # Internal network (no external access)
            internal_net = self.client.networks.create(
                'demo_internal',
                driver='bridge',
                internal=True
            )
            networks_created.append(internal_net)
            
            # Container 1: Web server
            web_container = self.client.containers.run(
                'nginx:alpine',
                name='demo_web',
                network='demo_bridge',
                ports={'80/tcp': 8081},
                detach=True
            )
            containers_created.append(web_container)
            
            # Container 2: Backend service
            backend_container = self.client.containers.run(
                'alpine:latest',
                name='demo_backend',
                command='sleep 300',
                network='demo_internal',
                detach=True
            )
            containers_created.append(backend_container)
            
            # Connect web container to internal network too
            internal_net.connect(web_container)
            
            # Test connectivity
            connectivity_tests = []
            
            # Test 1: Web can reach backend
            test_cmd = f'docker exec {web_container.id} ping -c 1 demo_backend'
            result = pexpect.run(test_cmd, timeout=5, encoding='utf-8')
            connectivity_tests.append({
                'test': 'Web -> Backend',
                'result': 'success' if '1 received' in result else 'failed'
            })
            
            # Test 2: Backend cannot reach external
            test_cmd = f'docker exec {backend_container.id} ping -c 1 8.8.8.8'
            result = pexpect.run(test_cmd, timeout=5, encoding='utf-8')
            connectivity_tests.append({
                'test': 'Backend -> External',
                'result': 'blocked' if '0 received' in result else 'allowed'
            })
            
            return {
                'networks': {
                    'bridge': 'demo_bridge (external access)',
                    'internal': 'demo_internal (isolated)'
                },
                'containers': {
                    'web': f"{web_container.short_id} (port 8081)",
                    'backend': f"{backend_container.short_id} (internal only)"
                },
                'connectivity_tests': connectivity_tests,
                'lesson': (
                    "Container networking patterns:\n"
                    "1. Bridge networks for general use\n"
                    "2. Internal networks for isolation\n"
                    "3. Multi-network attachment for flexibility\n"
                    "4. Service discovery via container names\n"
                    "Essential for microservices!"
                ),
                'security_tips': [
                    "Use internal networks for databases",
                    "Minimize exposed ports",
                    "Use network aliases for service discovery",
                    "Consider network policies in production"
                ]
            }
            
        finally:
            # Cleanup
            for container in containers_created:
                try:
                    container.stop()
                    container.remove()
                except:
                    pass
            
            for network in networks_created:
                try:
                    network.remove()
                except:
                    pass
    
    # Example 8: Volume Management
    def volume_management_example(self) -> Dict[str, Any]:
        """
        LEARNING GOAL: Persistent data patterns
        
        Demonstrates:
        - Creating and mounting volumes
        - Data persistence strategies
        - Backup and restore procedures
        - Sharing data between containers
        
        Tool: Docker SDK
        """
        logger.info("📖 Example 8: Volume and data management")
        
        volume_name = 'demo_data'
        containers_created = []
        
        try:
            # Create named volume
            logger.info("💾 Creating named volume")
            volume = self.client.volumes.create(
                name=volume_name,
                labels={'example': 'volume_management'}
            )
            
            # Container 1: Write data
            logger.info("📝 Writing data to volume")
            writer_container = self.client.containers.run(
                'alpine:latest',
                name='data_writer',
                volumes={volume_name: {'bind': '/data', 'mode': 'rw'}},
                command='sh -c "echo \'Persistent data example\' > /data/test.txt && '
                       'echo \'Created at: $(date)\' >> /data/test.txt"',
                remove=True
            )
            
            # Container 2: Read data
            logger.info("📖 Reading data from volume")
            reader_container = self.client.containers.run(
                'alpine:latest',
                name='data_reader',
                volumes={volume_name: {'bind': '/data', 'mode': 'ro'}},
                command='cat /data/test.txt',
                remove=True
            )
            
            data_content = reader_container.decode('utf-8').strip()
            
            # Container 3: Backup volume
            logger.info("💼 Creating volume backup")
            backup_container = self.client.containers.run(
                'alpine:latest',
                name='data_backup',
                volumes={
                    volume_name: {'bind': '/source', 'mode': 'ro'},
                    os.getcwd(): {'bind': '/backup', 'mode': 'rw'}
                },
                command='tar czf /backup/volume_backup.tar.gz -C /source .',
                remove=True
            )
            
            # Check backup file
            backup_exists = os.path.exists('volume_backup.tar.gz')
            if backup_exists:
                backup_size = os.path.getsize('volume_backup.tar.gz')
                os.remove('volume_backup.tar.gz')  # Cleanup
            else:
                backup_size = 0
            
            # Get volume info
            volume_info = volume.attrs
            
            return {
                'volume_name': volume_name,
                'data_written': data_content,
                'backup_created': backup_exists,
                'backup_size': f"{backup_size} bytes",
                'volume_driver': volume_info['Driver'],
                'lesson': (
                    "Volume management patterns:\n"
                    "1. Named volumes for persistence\n"
                    "2. Read-only mounts for safety\n"
                    "3. Backup strategies with tar\n"
                    "4. Volume sharing between containers\n"
                    "Critical for stateful applications!"
                ),
                'use_cases': [
                    "Database data persistence",
                    "Shared configuration files",
                    "Build artifact caching",
                    "User upload storage"
                ]
            }
            
        finally:
            # Cleanup
            try:
                volume.remove()
            except:
                pass
    
    # Helper methods
    def _get_educational_notes(self, flow_name: str) -> List[str]:
        """Get educational notes for a specific flow"""
        notes = {
            'hello_world': [
                "This is the simplest container pattern",
                "The container runs once and exits",
                "Output is captured from logs",
                "Good for batch jobs and one-time tasks"
            ],
            'interactive_shell': [
                "dockerpty provides real terminal emulation",
                "Perfect for debugging and exploration",
                "Handles signals and window resizing",
                "Used by 'docker exec -it' internally"
            ],
            'automated_commands': [
                "pexpect enables scripted interactions",
                "Pattern matching ensures reliability",
                "Great for testing and CI/CD",
                "Can handle complex workflows"
            ],
            'multi_container': [
                "Dependencies require careful ordering",
                "Health checks prevent race conditions",
                "Networks provide isolation and discovery",
                "This pattern scales to microservices"
            ],
            'log_monitoring': [
                "Logs are the window into containers",
                "Pattern matching enables automation",
                "Essential for production monitoring",
                "Foundation for observability"
            ],
            'health_recovery': [
                "Health checks detect failures early",
                "Restart policies provide resilience",
                "Must balance aggression vs stability",
                "Critical for high availability"
            ],
            'networking': [
                "Networks provide isolation and security",
                "Internal networks block external access",
                "Service discovery via DNS names",
                "Foundation for microservices"
            ],
            'volume_management': [
                "Volumes persist beyond container lifecycle",
                "Named volumes are portable",
                "Backup strategies are essential",
                "Consider performance implications"
            ]
        }
        
        return notes.get(flow_name, ["Study this example carefully!"])
    
    def _get_debugging_tips(self, flow_name: str, error: str) -> List[str]:
        """Get debugging tips based on the error"""
        tips = ["Check container logs", "Verify Docker daemon is running"]
        
        if "permission denied" in error.lower():
            tips.append("Check Docker socket permissions")
            tips.append("Run: sudo usermod -aG docker $USER")
        
        if "not found" in error.lower():
            tips.append("Verify the image exists: docker images")
            tips.append("Pull missing images: docker pull <image>")
        
        if "timeout" in error.lower():
            tips.append("Increase timeout values")
            tips.append("Check if container is responding")
            tips.append("Verify network connectivity")
        
        if "port" in error.lower():
            tips.append("Check port availability: netstat -tlnp")
            tips.append("Use different port mapping")
        
        return tips