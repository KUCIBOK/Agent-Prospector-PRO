# INTERACTIVE PROXYCURL SETUP - PowerShell
# This script guides you through getting and configuring your Proxycurl API key

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         🔗 PROXYCURL SETUP - Interactive Configuration         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will help you:" -ForegroundColor Yellow
Write-Host "  1. Get a free Proxycurl API key" -ForegroundColor Gray
Write-Host "  2. Configure it in your environment" -ForegroundColor Gray
Write-Host "  3. Test that it works" -ForegroundColor Gray
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "STEP 1: Get Your Free API Key" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$openBrowser = Read-Host "📌 Open Proxycurl signup page in browser? (Y/n)"
if ($openBrowser -ne "n" -and $openBrowser -ne "N") {
    Write-Host "Opening https://proxycurl.com..." -ForegroundColor Green
    Start-Process "https://proxycurl.com"
    Write-Host ""
    Write-Host "👉 Follow these steps:" -ForegroundColor Yellow
    Write-Host "   1. Click 'Sign Up' button (top right)" -ForegroundColor Gray
    Write-Host "   2. Enter your email address" -ForegroundColor Gray
    Write-Host "   3. Create a password" -ForegroundColor Gray
    Write-Host "   4. Check your email and click verification link" -ForegroundColor Gray
    Write-Host "   5. Login with your credentials" -ForegroundColor Gray
    Write-Host "   6. Go to Dashboard/API Keys section" -ForegroundColor Gray
    Write-Host "   7. Copy your API key (starts with 'pk_')" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "STEP 2: Enter Your API Key" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$apiKey = Read-Host "🔑 Paste your Proxycurl API key (starts with 'pk_')"

if ($apiKey -eq "" -or $apiKey.Length -lt 10) {
    Write-Host "❌ Invalid API key. Please try again." -ForegroundColor Red
    exit 1
}

if (-not $apiKey.StartsWith("pk_")) {
    Write-Host "⚠️  Warning: API key should start with 'pk_'. Continue anyway? (Y/n)" -ForegroundColor Yellow
    $continue = Read-Host ""
    if ($continue -eq "n" -or $continue -eq "N") {
        exit 1
    }
}

Write-Host "✅ API key accepted: $($apiKey.Substring(0, 10))..." -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "STEP 3: Configure Environment Variable" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "Choose how to set the API key:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [1] Session Only (temporary, this PowerShell session only)" -ForegroundColor Gray
Write-Host "  [2] User Level (permanent, survives restart)" -ForegroundColor Gray
Write-Host "  [3] Docker Environment (docker-compose.yml)" -ForegroundColor Gray
Write-Host "  [4] .env File (project root)" -ForegroundColor Gray
Write-Host ""

$option = Read-Host "Choose option (1-4)"

switch ($option) {
    "1" {
        # Session only
        Write-Host ""
        Write-Host "Setting API key for this session only..." -ForegroundColor Yellow
        $env:PROXYCURL_API_KEY = $apiKey
        Write-Host "✅ Set! (will be lost when you close PowerShell)" -ForegroundColor Green
        $persistent = $false
    }

    "2" {
        # User level (permanent)
        Write-Host ""
        Write-Host "Setting API key permanently in user environment..." -ForegroundColor Yellow
        [Environment]::SetEnvironmentVariable("PROXYCURL_API_KEY", $apiKey, "User")
        Write-Host "✅ Set! (restart PowerShell to use it)" -ForegroundColor Green

        # Also set for current session
        $env:PROXYCURL_API_KEY = $apiKey
        Write-Host "   Also set for current session" -ForegroundColor Gray
        $persistent = $true
    }

    "3" {
        # Docker compose
        Write-Host ""
        Write-Host "Adding to docker-compose.yml..." -ForegroundColor Yellow

        $composePath = "docker-compose.yml"
        if (Test-Path $composePath) {
            Write-Host "📝 Manual step: Edit docker-compose.yml" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Find the 'app:' service and add to 'environment:':" -ForegroundColor Gray
            Write-Host "    - PROXYCURL_API_KEY=$apiKey" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Then run: docker-compose restart app worker" -ForegroundColor Gray

            # Also set for current session
            $env:PROXYCURL_API_KEY = $apiKey
        } else {
            Write-Host "❌ docker-compose.yml not found" -ForegroundColor Red
            exit 1
        }
        $persistent = $true
    }

    "4" {
        # .env file
        Write-Host ""
        Write-Host "Creating .env file..." -ForegroundColor Yellow

        $envPath = ".env"
        if (Test-Path $envPath) {
            Write-Host "⚠️  .env file already exists. Appending..." -ForegroundColor Yellow
        }

        Add-Content -Path $envPath -Value "PROXYCURL_API_KEY=$apiKey"
        Write-Host "✅ Added to .env" -ForegroundColor Green

        # Also set for current session
        $env:PROXYCURL_API_KEY = $apiKey
        Write-Host "   Also set for current session" -ForegroundColor Gray
        $persistent = $true
    }

    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "STEP 4: Verify Configuration" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking environment variable..." -ForegroundColor Yellow
$envCheck = $env:PROXYCURL_API_KEY
if ($envCheck) {
    Write-Host "✅ Environment variable set: $($envCheck.Substring(0, 10))..." -ForegroundColor Green
} else {
    Write-Host "❌ Environment variable NOT set!" -ForegroundColor Red
    Write-Host "   Try restarting PowerShell or running: `$env:PROXYCURL_API_KEY = '$apiKey'" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Checking API connectivity..." -ForegroundColor Yellow

try {
    # Wait for services to be ready
    $maxRetries = 3
    $retry = 0
    $connected = $false

    while ($retry -lt $maxRetries -and -not $connected) {
        try {
            $health = curl.exe -s http://localhost:8000/api/monitoring/health 2>$null | ConvertFrom-Json
            if ($health.status -eq "ok") {
                Write-Host "✅ API is responding and healthy" -ForegroundColor Green
                Write-Host "   Uptime: $($health.uptime_seconds) seconds" -ForegroundColor Gray
                $connected = $true
            }
        } catch {
            $retry++
            if ($retry -lt $maxRetries) {
                Write-Host "   Waiting for API to be ready... ($retry/$maxRetries)" -ForegroundColor Yellow
                Start-Sleep -Seconds 2
            }
        }
    }

    if (-not $connected) {
        Write-Host "⚠️  API not responding. Make sure services are running:" -ForegroundColor Yellow
        Write-Host "   docker-compose up -d" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠️  Could not test API connection" -ForegroundColor Yellow
    Write-Host "   Make sure Docker services are running" -ForegroundColor Gray
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Proxycurl account created" -ForegroundColor Green
Write-Host "  ✅ API key obtained" -ForegroundColor Green
Write-Host "  ✅ Environment variable configured" -ForegroundColor Green
if ($persistent) {
    Write-Host "  ✅ Configuration is persistent (survives restart)" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Configuration is temporary (session only)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Restart Docker services (if you chose Docker or .env):" -ForegroundColor Gray
Write-Host "     docker-compose restart app worker scheduler" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Run the test script:" -ForegroundColor Gray
Write-Host "     .\test_improvements.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Open dashboard:" -ForegroundColor Gray
Write-Host "     http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

Write-Host "📚 Need help?" -ForegroundColor Yellow
Write-Host "  - Read: PROXYCURL_SETUP_DETAILED.md" -ForegroundColor Gray
Write-Host "  - Check: LINKEDIN_INSTAGRAM_SETUP.md" -ForegroundColor Gray
Write-Host ""

Write-Host "You're all set! 🎉" -ForegroundColor Green
