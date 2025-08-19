@echo off
echo ========================================
echo    TrustCoin Bots Launcher (Windows)
echo ========================================
echo.

echo Starting bots with different configurations...

echo [1/3] Starting Arabic Bot (Port 8444)...
start "Arabic Bot" cmd /k "cd /d %cd% && python ARABIC/bot.py"
timeout /t 3 >nul

echo [2/3] Starting French Bot (Port 8445)...
start "French Bot" cmd /k "cd /d %cd% && python FRANCE/bot.py"
timeout /t 3 >nul

echo [3/3] Attempting English Bot (Port 8443)...
echo Note: If English bot fails with 'Conflict', it may be running elsewhere
start "English Bot" cmd /k "cd /d %cd% && python ENGLISH/bot.py"
timeout /t 3 >nul

echo.
echo ========================================
echo All bots have been launched!
echo Check individual windows for status.
echo ========================================
echo.
echo Press any key to continue...
pause >nul
