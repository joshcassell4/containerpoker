@echo off
echo Container Poker Setup for Windows
echo =================================
echo.

REM Build the Docker image
echo Building Docker container...
docker build -t containerpoker-orchestrator .
if %errorlevel% neq 0 (
    echo ERROR: Docker build failed
    echo Make sure Docker Desktop is running
    pause
    exit /b 1
)

echo.
echo Starting the application...
docker run -d ^
    --name containerpoker_orchestrator ^
    -p 5000:5000 ^
    -v /var/run/docker.sock:/var/run/docker.sock ^
    -v "%cd%/src":/app/src ^
    -e FLASK_ENV=development ^
    -e FLASK_DEBUG=1 ^
    containerpoker-orchestrator

if %errorlevel% neq 0 (
    echo ERROR: Failed to start container
    echo Trying to remove existing container...
    docker rm -f containerpoker_orchestrator
    echo Please run setup.bat again
    pause
    exit /b 1
)

echo.
echo ================================
echo Setup complete!
echo Visit http://localhost:5000
echo ================================
echo.
echo Useful commands:
echo   docker logs containerpoker_orchestrator -f    (view logs)
echo   docker exec -it containerpoker_orchestrator bash    (shell access)
echo   docker stop containerpoker_orchestrator    (stop container)
echo   docker rm containerpoker_orchestrator    (remove container)
echo.
pause