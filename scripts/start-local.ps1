<#
.SYNOPSIS
    One-Command Startup & Lifecycle Management Script untuk Sistem Informasi Enterprise SMAN 1 Bunut.
.DESCRIPTION
    Menjalankan backend Django Ninja dan frontend React Vite dalam lingkungan pengujian lokal.
    Menangani preflight check, verifikasi konektivitas Redis, kesiapan port, bounded healthcheck,
    dan graceful process tree management.
.PARAMETER Runner
    Pilihan backend runner: 'granian' (default, ASGI production runner) atau 'runserver' (Django development server).
.PARAMETER BackendHost
    Host bind backend. Wajib loopback ('127.0.0.1' atau 'localhost'). Default: 127.0.0.1.
.PARAMETER BackendPort
    Port untuk backend server. Default: 8000.
.PARAMETER FrontendPort
    Port untuk frontend Vite dev server. Default: 3000.
.PARAMETER Environment
    Environment target: 'development' (default) atau 'integration'.
.PARAMETER SkipCheck
    Lewati pemeriksaan opsional Django system check (pemeriksaan keamanan dan runtime tetap dijalankan).
.PARAMETER OpenBrowser
    Buka peramban web default secara otomatis setelah seluruh layanan terverifikasi siap.
.PARAMETER Migrate
    Jalankan migrasi database Django secara eksplisit sebelum memulai backend.
#>
[CmdletBinding()]
param (
    [ValidateSet("granian", "runserver")]
    [string]$Runner = "granian",

    [string]$BackendHost = "127.0.0.1",

    [ValidateRange(1024, 65535)]
    [int]$BackendPort = 8000,

    [ValidateRange(1024, 65535)]
    [int]$FrontendPort = 3000,

    [ValidateSet("development", "integration")]
    [string]$Environment = "development",

    [switch]$SkipCheck,
    [switch]$OpenBrowser,
    [switch]$Migrate
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path "$ScriptDir\..").Path

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  SISTEM INFORMASI ENTERPRISE SMAN 1 BUNUT - STARTUP SCRIPT" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Project Root : $ProjectRoot" -ForegroundColor Gray
Write-Host "Backend Mode : $Runner (Host: $BackendHost, Port: $BackendPort)" -ForegroundColor Gray
Write-Host "Frontend Mode: Vite (Port: $FrontendPort, StrictPort: ON)" -ForegroundColor Gray
Write-Host "Environment  : $Environment" -ForegroundColor Gray

# -----------------------------------------------------------------------------
# 1. Validasi Keamanan Host Binding (Localhost Only Guard)
# -----------------------------------------------------------------------------
if ($BackendHost -ne "127.0.0.1" -and $BackendHost -ne "localhost") {
    Write-Error "Binding backend ke host non-localhost ('$BackendHost') ditolak. Lingkungan pengujian lokal ini menggunakan kredensial sederhana dan wajib dibatasi hanya untuk loopback (127.0.0.1/localhost)."
    exit 1
}

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
function Test-TcpPortConnection ($HostAddress, $PortNumber) {
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $iar = $client.BeginConnect($HostAddress, $PortNumber, $null, $null)
        $wait = $iar.AsyncWaitHandle.WaitOne(1000, $false)
        if (-not $wait) {
            $client.Close()
            return $false
        }
        $client.EndConnect($iar)
        $client.Close()
        return $true
    } catch {
        return $false
    }
}

function Get-PortProcessInfo ($PortNumber) {
    try {
        $conn = Get-NetTCPConnection -LocalPort $PortNumber -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($conn -and $conn.OwningProcess) {
            $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
            return [PSCustomObject]@{
                PID = $conn.OwningProcess
                Name = if ($proc) { $proc.ProcessName } else { "Unknown" }
            }
        }
    } catch {}
    return $null
}

function Stop-ProcessTree ($ProcessId) {
    if (-not $ProcessId) { return }
    try {
        # Menggunakan taskkill /T /F native Windows untuk mematikan seluruh process tree
        & taskkill.exe /PID $ProcessId /T /F 2>$null | Out-Null
    } catch {
        try {
            Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
        } catch {}
    }
}

# -----------------------------------------------------------------------------
# 2. Mandatory Preflight Checks
# -----------------------------------------------------------------------------
Write-Host "`n[1/6] Memeriksa dependensi dan runtime..." -ForegroundColor Yellow

# Python venv
$PythonExe = Join-Path $ProjectRoot "backend\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Error "Virtual environment Python tidak ditemukan di '$PythonExe'. Jalankan setup virtual environment terlebih dahulu."
    exit 1
}
$PyVer = & $PythonExe --version 2>&1
Write-Host "  [OK] Python Virtual Environment: $PyVer ($PythonExe)" -ForegroundColor Green

# Granian executable jika runner adalah granian
$GranianExe = Join-Path $ProjectRoot "backend\.venv\Scripts\granian.exe"
if ($Runner -eq "granian" -and -not (Test-Path $GranianExe)) {
    Write-Error "Granian executable tidak ditemukan di '$GranianExe'. Pasang granian atau gunakan -Runner runserver."
    exit 1
}
if ($Runner -eq "granian") {
    $GranianVer = & $GranianExe --version 2>&1
    Write-Host "  [OK] Granian ASGI Runner: $GranianVer" -ForegroundColor Green
}

# Node.js & npm
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js tidak ditemukan di PATH sistem. Pastikan Node.js v20+ terpasang."
    exit 1
}
$NodeVer = & node -v
if ($LASTEXITCODE -ne 0) { Write-Error "Gagal mengeksekusi node."; exit 1 }

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm tidak ditemukan di PATH sistem."
    exit 1
}
$NpmVer = & npm -v
Write-Host "  [OK] Node.js & npm: Node $NodeVer, npm $NpmVer" -ForegroundColor Green

# Frontend node_modules
$FrontendModules = Join-Path $ProjectRoot "frontend\node_modules"
if (-not (Test-Path $FrontendModules)) {
    Write-Error "Dependensi frontend tidak ditemukan di '$FrontendModules'. Jalankan 'npm install' di direktori frontend."
    exit 1
}
Write-Host "  [OK] Frontend Dependencies: node_modules terpasang" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 3. Environment Files Verification (No Overwrite, No Secret Leak)
# -----------------------------------------------------------------------------
Write-Host "`n[2/6] Memeriksa berkas konfigurasi lingkungan (.env)..." -ForegroundColor Yellow

$BackendEnv = Join-Path $ProjectRoot "backend\.env"
if (-not (Test-Path $BackendEnv)) {
    Write-Error "Berkas 'backend\.env' tidak ditemukan. Harap buat berkas konfigurasi backend sebelum memulai."
    exit 1
}
Write-Host "  [OK] Backend Environment : Ditemukan (backend\.env)" -ForegroundColor Green

$FrontendEnv = Join-Path $ProjectRoot "frontend\.env"
if (-not (Test-Path $FrontendEnv)) {
    Write-Error "Berkas 'frontend\.env' tidak ditemukan. Harap buat berkas konfigurasi frontend sebelum memulai."
    exit 1
}
Write-Host "  [OK] Frontend Environment: Ditemukan (frontend\.env)" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 4. Redis Service Verification (Fail-Closed Security)
# -----------------------------------------------------------------------------
Write-Host "`n[3/6] Memeriksa konektivitas Redis (127.0.0.1:6379)..." -ForegroundColor Yellow

$RedisActive = Test-TcpPortConnection "127.0.0.1" 6379
if (-not $RedisActive) {
    Write-Host "  [*] Redis port 6379 belum aktif. Mencoba memulai service di WSL2 Ubuntu..." -ForegroundColor Gray
    try {
        & wsl -d Ubuntu -- sudo service redis-server start 2>$null | Out-Null
        Start-Sleep -Seconds 2
        $RedisActive = Test-TcpPortConnection "127.0.0.1" 6379
    } catch {}
}

if (-not $RedisActive) {
    Write-Error "Layanan Redis pada 127.0.0.1:6379 tidak dapat dihubungi. Startup dihentikan demi menjaga keamanan token blacklist dan rate limiting (Fail-Closed Policy)."
    exit 1
}
Write-Host "  [OK] Redis Server: Berjalan dan terhubung pada port 6379" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 5. Port Availability & Existing Instance Check
# -----------------------------------------------------------------------------
Write-Host "`n[4/6] Memeriksa ketersediaan port ($BackendPort dan $FrontendPort)..." -ForegroundColor Yellow

$BackendPortActive = Test-TcpPortConnection $BackendHost $BackendPort
$FrontendPortActive = Test-TcpPortConnection "127.0.0.1" $FrontendPort

# Cek apakah aplikasi sudah berjalan dan sehat
if ($BackendPortActive -and $FrontendPortActive) {
    $ExistingHealth = $false
    try {
        $resp = Invoke-RestMethod -Uri "http://${BackendHost}:${BackendPort}/api/health" -Method Get -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($resp -and $resp.status -eq "ok") {
            $ExistingHealth = $true
        }
    } catch {}

    if ($ExistingHealth) {
        Write-Host "  [INFO] Backend dan Frontend sudah berjalan dan dalam kondisi sehat!" -ForegroundColor Cyan
        Write-Host "         Backend: http://${BackendHost}:${BackendPort}/api/health (status: ok)" -ForegroundColor Cyan
        Write-Host "         Frontend: http://localhost:${FrontendPort}" -ForegroundColor Cyan
        Write-Host "         Tidak membuat instance duplikat." -ForegroundColor Cyan

        if ($OpenBrowser) {
            Write-Host "  [*] Membuka peramban web ke http://localhost:${FrontendPort}..." -ForegroundColor Gray
            Start-Process "http://localhost:${FrontendPort}"
        }

        Write-Host "`n================================================================================" -ForegroundColor Cyan
        Write-Host "  APLIKASI BERJALAN & SIAP DIGUNAKAN (EXISTING HEALTHY INSTANCE)" -ForegroundColor Green
        Write-Host "================================================================================" -ForegroundColor Cyan
        return
    }
}

if ($BackendPortActive) {
    $owner = Get-PortProcessInfo $BackendPort
    Write-Error "Port Backend $BackendPort sedang digunakan oleh proses lain [PID: $($owner.PID), Nama: $($owner.Name)]. Hentikan proses tersebut atau gunakan -BackendPort lain."
    exit 1
}

if ($FrontendPortActive) {
    $owner = Get-PortProcessInfo $FrontendPort
    Write-Error "Port Frontend $FrontendPort sedang digunakan oleh proses lain [PID: $($owner.PID), Nama: $($owner.Name)]. Hentikan proses tersebut atau gunakan -FrontendPort lain."
    exit 1
}
Write-Host "  [OK] Port $BackendPort (Backend) dan $FrontendPort (Frontend) tersedia." -ForegroundColor Green

# -----------------------------------------------------------------------------
# 6. Database Migration (Optional Explicit) & Django System Check
# -----------------------------------------------------------------------------
if ($Migrate) {
    Write-Host "`n[*] Menjalankan migrasi database Django..." -ForegroundColor Yellow
    Push-Location (Join-Path $ProjectRoot "backend")
    try {
        & $PythonExe manage.py migrate
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Migrasi database gagal dieksekusi."
            Pop-Location
            exit 1
        }
        Write-Host "  [OK] Migrasi database selesai." -ForegroundColor Green
    } finally {
        Pop-Location
    }
}

if (-not $SkipCheck) {
    Write-Host "`n[*] Menjalankan Django System Check..." -ForegroundColor Yellow
    Push-Location (Join-Path $ProjectRoot "backend")
    try {
        & $PythonExe manage.py check --fail-level ERROR
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Django system check menemukan masalah."
            Pop-Location
            exit 1
        }
        Write-Host "  [OK] Django system check: 0 issues." -ForegroundColor Green
    } finally {
        Pop-Location
    }
} else {
    Write-Host "`n[*] Django System Check dilewati (-SkipCheck)." -ForegroundColor Gray
}

# -----------------------------------------------------------------------------
# 7. Menjalankan Backend & Frontend (Isolated Process Trees)
# -----------------------------------------------------------------------------
Write-Host "`n[5/6] Memulai layanan backend dan frontend..." -ForegroundColor Yellow

$env:DJANGO_ENV = $Environment
$env:REDIS_URL = "redis://127.0.0.1:6379/1"
$env:BACKEND_PROXY_TARGET = "http://${BackendHost}:${BackendPort}"

$BackendProc = $null
$FrontendProc = $null

try {
    # 7.1 Start Backend
    if ($Runner -eq "granian") {
        $backendArgs = @(
            "--interface", "asginl",
            "config.asgi:application",
            "--working-dir", (Join-Path $ProjectRoot "backend"),
            "--host", $BackendHost,
            "--port", $BackendPort.ToString()
        )
        $BackendProc = Start-Process -FilePath $GranianExe -ArgumentList $backendArgs -PassThru -NoNewWindow
    } else {
        $backendArgs = @(
            "manage.py", "runserver",
            "${BackendHost}:${BackendPort}",
            "--noreload"
        )
        $BackendProc = Start-Process -FilePath $PythonExe -ArgumentList $backendArgs -WorkingDirectory (Join-Path $ProjectRoot "backend") -PassThru -NoNewWindow
    }
    Write-Host "  -> Backend ($Runner) dimulai [PID: $($BackendProc.Id)]" -ForegroundColor Green

    # 7.2 Start Frontend
    $frontendArgs = @(
        "/c", "npm", "run", "dev", "--",
        "--port", $FrontendPort.ToString(),
        "--strictPort"
    )
    $FrontendProc = Start-Process -FilePath "cmd.exe" -ArgumentList $frontendArgs -WorkingDirectory (Join-Path $ProjectRoot "frontend") -PassThru -NoNewWindow
    Write-Host "  -> Frontend (Vite) dimulai [PID: $($FrontendProc.Id)]" -ForegroundColor Green

    # -------------------------------------------------------------------------
    # 8. Readiness Verification (Bounded Polling)
    # -------------------------------------------------------------------------
    Write-Host "`n[6/6] Memverifikasi kesiapan layanan (Bounded Healthcheck)..." -ForegroundColor Yellow

    # Poll Backend Healthcheck (max 20 detik)
    $backendReady = $false
    $timeoutSeconds = 20
    $startTime = Get-Date

    Write-Host "  [*] Menunggu respon backend http://${BackendHost}:${BackendPort}/api/health..." -NoNewline -ForegroundColor Gray
    while (-not $backendReady -and ((Get-Date) - $startTime).TotalSeconds -lt $timeoutSeconds) {
        if ($BackendProc.HasExited) {
            Write-Host " GAGAL!" -ForegroundColor Red
            Write-Error "Proses backend berhenti mendadak saat startup (Exit code: $($BackendProc.ExitCode))."
            exit 1
        }
        try {
            $health = Invoke-RestMethod -Uri "http://${BackendHost}:${BackendPort}/api/health" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($health -and $health.status -eq "ok") {
                $backendReady = $true
                break
            }
        } catch {}
        Start-Sleep -Seconds 1
        Write-Host "." -NoNewline -ForegroundColor Gray
    }

    if (-not $backendReady) {
        Write-Host " TIMEOUT!" -ForegroundColor Red
        Write-Error "Backend tidak merespons healthcheck dalam batas waktu $timeoutSeconds detik."
        exit 1
    }
    Write-Host " OK [HEALTHY]" -ForegroundColor Green

    # Poll Frontend HTTP (max 20 detik)
    $frontendReady = $false
    $startTime = Get-Date
    Write-Host "  [*] Menunggu respon frontend http://localhost:${FrontendPort}..." -NoNewline -ForegroundColor Gray
    while (-not $frontendReady -and ((Get-Date) - $startTime).TotalSeconds -lt $timeoutSeconds) {
        if ($FrontendProc.HasExited) {
            Write-Host " GAGAL!" -ForegroundColor Red
            Write-Error "Proses frontend berhenti mendadak saat startup (Exit code: $($FrontendProc.ExitCode))."
            exit 1
        }
        try {
            $resp = Invoke-WebRequest -Uri "http://localhost:${FrontendPort}" -Method Get -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($resp -and $resp.StatusCode -eq 200) {
                $frontendReady = $true
                break
            }
        } catch {}
        Start-Sleep -Seconds 1
        Write-Host "." -NoNewline -ForegroundColor Gray
    }

    if (-not $frontendReady) {
        Write-Host " TIMEOUT!" -ForegroundColor Red
        Write-Error "Frontend tidak merespons dalam batas waktu $timeoutSeconds detik."
        exit 1
    }
    Write-Host " OK [HTTP 200]" -ForegroundColor Green

    # Verifikasi API Proxy melalui Frontend
    try {
        $proxyHealth = Invoke-RestMethod -Uri "http://localhost:${FrontendPort}/api/health" -Method Get -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($proxyHealth -and $proxyHealth.status -eq "ok") {
            Write-Host "  [OK] Vite API Proxy: Berfungsi transparan ke backend (/api/health OK)" -ForegroundColor Green
        }
    } catch {
        Write-Warning "  [PERINGATAN] Vite API Proxy belum merespons /api/health."
    }

    Write-Host "`n================================================================================" -ForegroundColor Cyan
    Write-Host "  APLIKASI BERJALAN & SIAP DIGUNAKAN" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "Frontend URL         : http://localhost:${FrontendPort}" -ForegroundColor White
    Write-Host "Backend API URL      : http://${BackendHost}:${BackendPort}/api" -ForegroundColor White
    Write-Host "Healthcheck          : http://${BackendHost}:${BackendPort}/api/health" -ForegroundColor White
    Write-Host "OpenAPI Interactive  : http://${BackendHost}:${BackendPort}/api/docs" -ForegroundColor White
    Write-Host "Kredensial Pengujian : docs/guide/ACCOUNTS.local.md" -ForegroundColor Magenta
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "Tekan [Ctrl + C] atau [Enter] untuk menghentikan seluruh layanan secara bersamaan..." -ForegroundColor Yellow

    if ($OpenBrowser) {
        Write-Host "  [*] Membuka peramban web ke http://localhost:${FrontendPort}..." -ForegroundColor Gray
        Start-Process "http://localhost:${FrontendPort}"
    }

    # Monitoring Loop
    while (-not $BackendProc.HasExited -and -not $FrontendProc.HasExited) {
        if ([Console]::KeyAvailable) {
            $key = [Console]::ReadKey($true)
            if ($key.Key -eq [ConsoleKey]::Enter -or $key.Key -eq [ConsoleKey]::Escape) {
                break
            }
        }
        Start-Sleep -Milliseconds 500
    }

} finally {
    Write-Host "`n`n[*] Menghentikan proses yang dibuat startup script..." -ForegroundColor Yellow
    if ($BackendProc) {
        Write-Host "  -> Menghentikan Backend Process Tree [PID: $($BackendProc.Id)]..." -ForegroundColor Gray
        Stop-ProcessTree $BackendProc.Id
    }
    if ($FrontendProc) {
        Write-Host "  -> Menghentikan Frontend Process Tree [PID: $($FrontendProc.Id)]..." -ForegroundColor Gray
        Stop-ProcessTree $FrontendProc.Id
    }
    Write-Host "[OK] Seluruh proses aplikasi telah dihentikan secara aman." -ForegroundColor Green
}
