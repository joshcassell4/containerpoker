# Container Poker Setup for Windows PowerShell
Write-Host "Container Poker Setup for Windows" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Build the Docker image
Write-Host "Building Docker container..." -ForegroundColor Yellow
docker build -t containerpoker-orchestrator .

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker build failed" -ForegroundColor Red
    Write-Host "Make sure Docker Desktop is running" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting the application..." -ForegroundColor Yellow

# Remove existing container if it exists
docker rm -f containerpoker_orchestrator 2>$null

# Run the container
docker run -d `
    --name containerpoker_orchestrator `
    -p 5000:5000 `
    -v /var/run/docker.sock:/var/run/docker.sock `
    -v "${PWD}/src:/app/src" `
    -e FLASK_ENV=development `
    -e FLASK_DEBUG=1 `
    containerpoker-orchestrator

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to start container" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Visit http://localhost:5000" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  docker logs containerpoker_orchestrator -f    (view logs)"
Write-Host "  docker exec -it containerpoker_orchestrator bash    (shell access)"
Write-Host "  docker stop containerpoker_orchestrator    (stop container)"
Write-Host "  docker rm containerpoker_orchestrator    (remove container)"
Write-Host ""
Read-Host "Press Enter to exit"