@echo off
echo ========================================
echo    Stopping All TrustCoin Bots
echo ========================================
echo.

echo Killing all Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✅ All Python processes stopped
) else (
    echo ℹ️  No Python processes found running
)

echo.
echo Cleaning up health check files...
if exist bot_healthy_arabic.txt del bot_healthy_arabic.txt
if exist bot_healthy_french.txt del bot_healthy_french.txt
if exist bot_healthy_english.txt del bot_healthy_english.txt

echo.
echo ========================================
echo All bots have been stopped!
echo ========================================
echo.
pause
