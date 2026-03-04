@echo off
chcp 65001 >nul
title Claude API SSH Tunnel

REM Read config from config.txt
set SERVER=
set LOCAL_PORT=8080
set REMOTE_PORT=8000

for /f "tokens=1,2 delims==" %%a in (config.txt) do (
    if "%%a"=="SERVER" set SERVER=%%b
    if "%%a"=="LOCAL_PORT" set LOCAL_PORT=%%b
    if "%%a"=="REMOTE_PORT" set REMOTE_PORT=%%b
)

REM Check if SERVER is set
if "%SERVER%"=="" (
    echo [ERROR] Please edit config.txt and set your SERVER address.
    echo.
    echo Example:
    echo SERVER=root@192.168.1.100
    echo.
    pause
    exit /b 1
)

echo ========================================
echo   Claude API SSH Tunnel
echo ========================================
echo.
echo Server: %SERVER%
echo Local Port: %LOCAL_PORT%
echo Remote Port: %REMOTE_PORT%
echo.
echo Establishing SSH tunnel...
echo Access URL: http://localhost:%LOCAL_PORT%
echo.
echo Press Ctrl+C to disconnect
echo.

ssh -L %LOCAL_PORT%:127.0.0.1:%REMOTE_PORT% %SERVER% -N
