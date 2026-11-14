<#
.SYNOPSIS
    One-Command Startup Script untuk Sistem Informasi Enterprise SMAN 1 Bunut.
.DESCRIPTION
    Menjalankan backend Django Ninja dan frontend React Vite dalam lingkungan lokal pengujian.
    Menangani preflight check, manajemen PID proses terisolasi, dan graceful shutdown.
#>

param (
    [switch]$SkipCheck = $false,
    [string]$BackendHost = "127.0.0.1",
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 3000
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path "$ScriptDir\..").Path

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  SISTEM INFORMASI ENTERPRISE SMAN 1 BUNUT - ONE-COMMAND STARTUP" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Project Root : $ProjectRoot" -ForegroundColor Gray

# 1. Preflight Checks
Write-Host "`n[1/5] Memeriksa dependensi dan runtime..." -ForegroundColor Yellow

$PythonExe = Join-Path $ProjectRoot "backend\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Error "Virtual environment Python tidak ditemukan di '$PythonExe'. Jalankan setup backend terlebih dahulu."
    exit 1
}
Write-Host "  [OK] Python Virtual Environment: $PythonExe" -ForegroundColor Green

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js tidak ditemukan di PATH sistem. Pastikan Node.js v20+ terpasang."
    exit 1
}
$NodeVer = node -v
Write-Host "  [OK] Node.js Runtime: $NodeVer" -ForegroundColor Green

# 2. Environment Files
Write-Host "`n[2/5] Memeriksa berkas environment..." -ForegroundColor Yellow
$BackendEnv = Join-Path $ProjectRoot "backend\.env"
if (-not (Test-Path $BackendEnv)) {
    Write-Warning "Berkas 'backend\.env' tidak ditemukan. Menyalin dari 'backend\.env.example'..."
    Copy-Item (Join-Path $ProjectRoot "backend\.env.example") $BackendEnv
}
Write-Host "  [OK] Backend Environment : $BackendEnv" -ForegroundColor Green

$FrontendEnv = Join-Path $ProjectRoot "frontend\.env"
if (-not (Test-Path $FrontendEnv)) {
    Write-Warning "Berkas 'frontend\.env' tidak ditemukan. Menyalin dari 'frontend\.env.example'..."
    Copy-Item (Join-Path $ProjectRoot "frontend\.env.example") $FrontendEnv
}
Write-Host "  [OK] Frontend Environment: $FrontendEnv" -ForegroundColor Green

# 3. Redis Connectivity
Write-Host "`n[3/5] Memeriksa layanan Redis (Port 6379)..." -ForegroundColor Yellow
$RedisActive = $false
try {
    $RedisPing = wsl -d Ubuntu -- redis-cli ping 2>$null
    if ($RedisPing -match "PONG") {
        $RedisActive = $true
    }
} catch {
    # Fallback to direct TCP connection test
    $TcpTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 6379 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($TcpTest) {
        $RedisActive = $true
    }
}

if (-not $RedisActive) {
    Write-Host "  [*] Memulai layanan Redis di WSL2 Ubuntu..." -ForegroundColor Gray
    try {
        wsl -d Ubuntu -- sudo service redis-server start 2>$null
        Start-Sleep -Seconds 2
        $RedisPing = wsl -d Ubuntu -- redis-cli ping 2>$null
        if ($RedisPing -match "PONG") {
            $RedisActive = $true
        }
    } catch {}
}

if ($RedisActive) {
    Write-Host "  [OK] Redis Server: Berjalan dan merespons PONG di 127.0.0.1:6379" -ForegroundColor Green
} else {
    Write-Warning "  [PERINGATAN] Redis 6379 tidak aktif. Pastikan daemon Redis berjalan di WSL2 untuk mendukung session blacklist & rate limiting."
}

# 4. Django System Check
if (-not $SkipCheck) {
    Write-Host "`n[4/5] Menjalankan Django System Check..." -ForegroundColor Yellow
    Push-Location (Join-Path $ProjectRoot "backend")
    try {
        & $PythonExe manage.py check --fail-level ERROR
        Write-Host "  [OK] Django system check: 0 issues." -ForegroundColor Green
    } catch {
        Write-Error "Django system check gagal. Periksa konfigurasi settings atau database."
        Pop-Location
        exit 1
    }
    Pop-Location
} else {
    Write-Host "`n[4/5] Django System Check dilewati (--SkipCheck)." -ForegroundColor Gray
}

# 5. Menjalankan Backend & Frontend (Spawn Process Terisolasi)
Write-Host "`n[5/5] Menjalankan layanan aplikasi..." -ForegroundColor Yellow

# Start Backend via Granian (atau runserver)
$BackendArgs = @("manage.py", "runserver", "$($BackendHost):$($BackendPort)")
$BackendProc = Start-Process -FilePath $PythonExe -ArgumentList $BackendArgs -WorkingDirectory (Join-Path $ProjectRoot "backend") -PassThru -NoNewWindow
Write-Host "  -> Backend Django Ninja dimulai [PID: $($BackendProc.Id)] di http://$($BackendHost):$($BackendPort)/api" -ForegroundColor Green

# Start Frontend Vite Dev Server
$FrontendProc = Start-Process -FilePath "cmd.exe" -ArgumentList @("/c", "npm", "run", "dev") -WorkingDirectory (Join-Path $ProjectRoot "frontend") -PassThru -NoNewWindow
Write-Host "  -> Frontend React Vite dimulai  [PID: $($FrontendProc.Id)] di http://localhost:$($FrontendPort)" -ForegroundColor Green

Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "  APLIKASI BERJALAN & SIAP DIGUNAKAN" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Frontend Application : http://localhost:$($FrontendPort)" -ForegroundColor White
Write-Host "Backend API Base URL : http://$($BackendHost):$($BackendPort)/api" -ForegroundColor White
Write-Host "Healthcheck Endpoint : http://$($BackendHost):$($BackendPort)/api/health" -ForegroundColor White
Write-Host "OpenAPI Interactive  : http://$($BackendHost):$($BackendPort)/api/docs" -ForegroundColor White
Write-Host "Kredensial Pengujian : docs/guide/ACCOUNTS.local.md" -ForegroundColor Magenta
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Tekan [Ctrl + C] untuk menghentikan seluruh layanan secara bersamaan..." -ForegroundColor Yellow

# Graceful shutdown handler
try {
    while (-not $BackendProc.HasExited -and -not $FrontendProc.HasExited) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "`n`n[*] Menghentikan proses yang dibuat startup script..." -ForegroundColor Yellow
    if ($BackendProc -and -not $BackendProc.HasExited) {
        Write-Host "  -> Menghentikan Backend [PID: $($BackendProc.Id)]..." -ForegroundColor Gray
        Stop-Process -Id $BackendProc.Id -Force -ErrorAction SilentlyContinue
    }
    if ($FrontendProc -and -not $FrontendProc.HasExited) {
        Write-Host "  -> Menghentikan Frontend [PID: $($FrontendProc.Id)]..." -ForegroundColor Gray
        # Kill process tree for cmd/node
        Stop-Process -Id $FrontendProc.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "[OK] Seluruh proses aplikasi telah dihentikan secara aman." -ForegroundColor Green
}
