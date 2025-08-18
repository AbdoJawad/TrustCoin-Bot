@echo off
REM TrustCoin Bots Startup Script for Windows
REM This script helps you manage the TrustCoin bots deployment

setlocal enabledelayedexpansion

REM Function to check if Docker is installed
:check_docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are installed.
goto :eof

REM Function to check environment file
:check_env_file
if not exist ".env" (
    echo [ERROR] .env file not found. Please create it with your bot tokens.
    pause
    exit /b 1
)

findstr /C:"BOT_TOKEN_ENG=" .env >nul
if %errorlevel% neq 0 (
    echo [ERROR] BOT_TOKEN_ENG not found in .env file.
    pause
    exit /b 1
)

findstr /C:"BOT_TOKEN_ARA=" .env >nul
if %errorlevel% neq 0 (
    echo [ERROR] BOT_TOKEN_ARA not found in .env file.
    pause
    exit /b 1
)

findstr /C:"BOT_TOKEN_FR=" .env >nul
if %errorlevel% neq 0 (
    echo [ERROR] BOT_TOKEN_FR not found in .env file.
    pause
    exit /b 1
)

echo [SUCCESS] Environment file is configured correctly.
goto :eof

REM Function to start the bots
:start_bots
echo [INFO] Starting TrustCoin bots...
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo [SUCCESS] All bots started successfully!
    echo [INFO] Running containers:
    docker-compose ps
) else (
    echo [ERROR] Failed to start bots. Check the logs for more information.
    pause
    exit /b 1
)
goto :eof

REM Function to stop the bots
:stop_bots
echo [INFO] Stopping TrustCoin bots...
docker-compose down
echo [SUCCESS] All bots stopped successfully!
goto :eof

REM Function to restart the bots
:restart_bots
echo [INFO] Restarting TrustCoin bots...
docker-compose restart
echo [SUCCESS] All bots restarted successfully!
goto :eof

REM Function to show logs
:show_logs
if "%~2"=="" (
    echo [INFO] Showing logs for all bots...
    docker-compose logs -f
) else (
    echo [INFO] Showing logs for %~2 bot...
    docker-compose logs -f trustcoin-bot-%~2
)
goto :eof

REM Function to show status
:show_status
echo [INFO] TrustCoin Bots Status:
docker-compose ps
echo.
echo [INFO] Resource Usage:
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
goto :eof

REM Main script logic
if "%~1"=="start" (
    call :check_docker
    call :check_env_file
    call :start_bots
) else if "%~1"=="stop" (
    call :stop_bots
) else if "%~1"=="restart" (
    call :restart_bots
) else if "%~1"=="logs" (
    call :show_logs %*
) else if "%~1"=="status" (
    call :show_status
) else (
    echo TrustCoin Bots Management Script
    echo.
    echo Usage: %~nx0 {start^|stop^|restart^|logs^|status}
    echo.
    echo Commands:
    echo   start    - Start all TrustCoin bots
    echo   stop     - Stop all TrustCoin bots
    echo   restart  - Restart all TrustCoin bots
    echo   logs     - Show logs (optional: specify 'english', 'arabic', or 'french'^)
    echo   status   - Show bots status and resource usage
    echo.
    echo Examples:
    echo   %~nx0 start
    echo   %~nx0 logs english
    echo   %~nx0 status
    pause
)

endlocal