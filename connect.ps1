# Claude Code API SSH Tunnel Connection Script
# Usage: .\connect.ps1 -Server user@serverIP [-LocalPort 8080] [-RemotePort 8000]

param(
    [Parameter(Mandatory=$true)]
    [string]$Server,

    [int]$LocalPort = 8080,

    [int]$RemotePort = 8000
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Claude Code API SSH Tunnel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: $Server" -ForegroundColor Yellow
Write-Host "Local Port: $LocalPort" -ForegroundColor Yellow
Write-Host "Remote Port: $RemotePort" -ForegroundColor Yellow
Write-Host ""
Write-Host "Establishing SSH tunnel..." -ForegroundColor Green
Write-Host "Access URL: http://localhost:$LocalPort" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to disconnect" -ForegroundColor Gray
Write-Host ""

# Establish SSH tunnel
ssh -L "${LocalPort}:127.0.0.1:${RemotePort}" $Server -N
