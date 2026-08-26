#!/usr/bin/env powershell
# 🚀 Démarrer le système complet en une seule commande!

param(
    [switch]$Dashboard = $true,
    [switch]$API = $true,
    [switch]$Worker = $true,
    [int]$Port = 8000,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
🚀 Kucibok Prospector - Démarrage Complet

Utilisation:
    .\START_ALL.ps1                  # Démarre API + Worker + Dashboard
    .\START_ALL.ps1 -API             # Démarre seulement l'API
    .\START_ALL.ps1 -Worker          # Démarre seulement le Worker
    .\START_ALL.ps1 -Port 8001       # Démarre l'API sur le port 8001
    .\START_ALL.ps1 -Help            # Affiche cette aide

Exemples:
    # Démarrer tout (par défaut)
    .\START_ALL.ps1

    # Démarrer API seulement
    .\START_ALL.ps1 -API -Dashboard

    # Démarrer Worker seulement
    .\START_ALL.ps1 -Worker -Dashboard

"@
    exit
}

$ProjectRoot = Get-Location
Write-Host "🚀 Kucibok Prospector - Démarrage Complet" -ForegroundColor Cyan
Write-Host "📍 Projet: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# Fonction pour afficher les messages
function Show-Status {
    param([string]$Message, [ValidateSet("Info", "Success", "Error", "Warning")]$Level = "Info")
    switch ($Level) {
        "Success" { Write-Host "✅ $Message" -ForegroundColor Green }
        "Error" { Write-Host "❌ $Message" -ForegroundColor Red }
        "Warning" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "Info" { Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
    }
}

# Vérifications pré-lancement
Show-Status "Vérification de la configuration..." "Info"

# Vérifier Python
try {
    $PythonVersion = python --version 2>&1
    Show-Status "Python OK: $PythonVersion" "Success"
} catch {
    Show-Status "Python non trouvé! Installez Python 3.11+" "Error"
    exit 1
}

# Vérifier Redis
try {
    $RedisCheck = redis-cli ping 2>&1
    if ($RedisCheck -eq "PONG") {
        Show-Status "Redis OK (localhost:6379)" "Success"
    } else {
        Show-Status "Redis non connecté" "Warning"
    }
} catch {
    Show-Status "Redis pas trouvé - Essayez: choco install redis" "Warning"
}

# Vérifier le port
if ($API) {
    try {
        $PortCheck = netstat -ano 2>$null | Select-String ":$Port " | Select-Object -First 1
        if ($PortCheck) {
            Show-Status "Port $Port déjà utilisé!" "Error"
            Write-Host "Utilisez: taskkill /PID <PID> /F" -ForegroundColor Yellow
            exit 1
        } else {
            Show-Status "Port $Port disponible" "Success"
        }
    } catch {
        Show-Status "Impossible de vérifier le port" "Warning"
    }
}

Write-Host ""
Write-Host "=" * 60

# Démarrer l'API
if ($API) {
    Show-Status "Démarrage de l'API FastAPI sur le port $Port..." "Info"

    $ApiCmd = @"
Write-Host ""
Write-Host "🚀 API FastAPI" -ForegroundColor Cyan
Write-Host "📍 http://localhost:$Port" -ForegroundColor Gray
Write-Host "📖 Swagger: http://localhost:$Port/docs" -ForegroundColor Gray
Write-Host ""

cd '$ProjectRoot'
python -m uvicorn app.main:app --reload --port $Port 2>&1
"@

    $ApiScript = [scriptblock]::Create($ApiCmd)

    # Lancer l'API dans un nouveau processus PowerShell
    $ApiProcess = Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        "& { $ApiScript }"
    ) -PassThru

    $ApiProcessId = $ApiProcess.Id
    Show-Status "API lancée (PID: $ApiProcessId)" "Success"
    Start-Sleep -Seconds 3
}

# Démarrer le Celery Worker
if ($Worker) {
    Show-Status "Démarrage du Celery Worker..." "Info"

    $WorkerCmd = @"
Write-Host ""
Write-Host "⚙️  Celery Worker" -ForegroundColor Cyan
Write-Host "📍 Redis: localhost:6379" -ForegroundColor Gray
Write-Host ""

cd '$ProjectRoot'
celery -A app.workers.tasks worker --loglevel=info 2>&1
"@

    $WorkerScript = [scriptblock]::Create($WorkerCmd)

    # Lancer le Worker dans un nouveau processus PowerShell
    $WorkerProcess = Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        "& { $WorkerScript }"
    ) -PassThru

    $WorkerId = $WorkerProcess.Id
    Show-Status "Worker lancé (PID: $WorkerId)" "Success"
    Start-Sleep -Seconds 2
}

# Ouvrir le Dashboard
if ($Dashboard -and $API) {
    Show-Status "Ouverture du Dashboard..." "Info"
    Start-Sleep -Seconds 2

    $DashboardUrl = "http://localhost:$Port/dashboard.html"
    Show-Status "Dashboard: $DashboardUrl" "Success"

    # Ouvrir dans le navigateur par défaut
    try {
        Start-Process $DashboardUrl
        Show-Status "Dashboard ouvert dans le navigateur" "Success"
    } catch {
        Show-Status "Impossible d'ouvrir le navigateur - Allez à $DashboardUrl manuellement" "Warning"
    }
}

Write-Host ""
Write-Host "=" * 60
Write-Host ""
Write-Host "✅ SYSTÈME LANCÉ!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Dashboard:" -ForegroundColor Cyan
Write-Host "   http://localhost:$Port/dashboard.html" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 API Swagger:" -ForegroundColor Cyan
Write-Host "   http://localhost:$Port/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "🔥 PROCHAINE ÉTAPE:" -ForegroundColor Yellow
Write-Host "   1. Attendez 3-5 secondes que les services démarrent" -ForegroundColor Gray
Write-Host "   2. Allez sur http://localhost:$Port/dashboard.html" -ForegroundColor Gray
Write-Host "   3. Cliquez sur '🔥 Deep Source Curators'" -ForegroundColor Gray
Write-Host "   4. Attendez ~30-60 secondes" -ForegroundColor Gray
Write-Host "   5. Voyez 50 prospects s'afficher!" -ForegroundColor Gray
Write-Host ""
Write-Host "=" * 60
Write-Host ""

# Garder le script en cours d'exécution
Write-Host "💡 Le système est en cours d'exécution..." -ForegroundColor Cyan
Write-Host "⏸️  Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

# Afficher les PIDs pour faciliter l'arrêt
if ($API) {
    Write-Host "   API Process ID: $ApiProcessId" -ForegroundColor Gray
}
if ($Worker) {
    Write-Host "   Worker Process ID: $WorkerId" -ForegroundColor Gray
}
Write-Host ""

# Garder en cours d'exécution et surveiller les processes
while ($true) {
    Start-Sleep -Seconds 5

    # Vérifier si les processes sont toujours actifs
    if ($API -and -not (Get-Process -Id $ApiProcessId -ErrorAction SilentlyContinue)) {
        Show-Status "API arrêtée de manière inattendue!" "Error"
    }
    if ($Worker -and -not (Get-Process -Id $WorkerId -ErrorAction SilentlyContinue)) {
        Show-Status "Worker arrêté de manière inattendue!" "Error"
    }
}
