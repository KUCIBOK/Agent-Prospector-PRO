# TEST SCRIPT - All 3 Improvements (PowerShell)
# Run this after setting PROXYCURL_API_KEY

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🚀 TESTING KUCIBOK V1.2 IMPROVEMENTS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check API key
$apiKey = $env:PROXYCURL_API_KEY
if (-not $apiKey) {
    Write-Host "❌ ERROR: PROXYCURL_API_KEY not set" -ForegroundColor Red
    Write-Host "   Run: `$env:PROXYCURL_API_KEY = 'pk_your_key'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ API Key configured: $($apiKey.Substring(0, 5))..." -ForegroundColor Green
Write-Host ""

# Test 1: Health Check
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "1️⃣  Health Check" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$health = curl.exe -s http://localhost:8000/api/monitoring/health | ConvertFrom-Json
if ($health.status -eq "ok") {
    Write-Host "✅ API is healthy" -ForegroundColor Green
    Write-Host "   Uptime: $($health.uptime_seconds) seconds" -ForegroundColor Gray
} else {
    Write-Host "❌ API not responding" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: LinkedIn Curator Monitoring
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "2️⃣  LinkedIn Curator Monitoring" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "Triggering LinkedIn monitoring job..." -ForegroundColor Yellow
$linkedinResult = curl.exe -s -X POST http://localhost:8000/api/monitoring/jobs/monitor-linkedin | ConvertFrom-Json
$taskId = $linkedinResult.task_id
Write-Host "✅ Job queued: $taskId" -ForegroundColor Green
Start-Sleep -Seconds 3
Write-Host ""

# Test 3: Instagram Artist Analysis
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "3️⃣  Instagram Artist Analysis" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "Triggering Instagram analysis job..." -ForegroundColor Yellow
$instagramResult = curl.exe -s -X POST http://localhost:8000/api/monitoring/jobs/analyze-instagram | ConvertFrom-Json
$taskId = $instagramResult.task_id
Write-Host "✅ Job queued: $taskId" -ForegroundColor Green
Start-Sleep -Seconds 3
Write-Host ""

# Test 4: Advanced Artist Re-scoring
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "4️⃣  Advanced Artist Re-scoring" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "Triggering artist re-scoring job..." -ForegroundColor Yellow
$scoringResult = curl.exe -s -X POST http://localhost:8000/api/monitoring/jobs/rescore-artists-advanced | ConvertFrom-Json
$taskId = $scoringResult.task_id
Write-Host "✅ Job queued: $taskId" -ForegroundColor Green
Start-Sleep -Seconds 3
Write-Host ""

# Test 5: View Recent Signals
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "5️⃣  Recent Signals (if any)" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$signals = curl.exe -s "http://localhost:8000/api/monitoring/signals/recent?limit=5&days=7" | ConvertFrom-Json
$signalCount = $signals.total
Write-Host "📊 Signals detected: $signalCount" -ForegroundColor Yellow
Write-Host ""

# Test 6: Dashboard Summary
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "6️⃣  Dashboard Summary" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$summary = curl.exe -s http://localhost:8000/api/monitoring/summary | ConvertFrom-Json
Write-Host "👥 Prospects: $($summary.prospects.total) total ($($summary.prospects.artists) artists, $($summary.prospects.clients) clients)" -ForegroundColor Gray
Write-Host "💬 Messages: $($summary.messages.total) total ($($summary.messages.draft) draft, $($summary.messages.sent) sent)" -ForegroundColor Gray
Write-Host "📊 Signals (7d): $($summary.signals.recent)" -ForegroundColor Gray
Write-Host "⏱️  Uptime: $([math]::Round($summary.uptime_seconds/3600, 1)) hours" -ForegroundColor Gray
Write-Host ""

# Test 7: Job Status
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "7️⃣  Recent Jobs" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$jobs = curl.exe -s "http://localhost:8000/api/monitoring/jobs?limit=5" | ConvertFrom-Json
foreach ($job in $jobs.items) {
    $statusColor = if ($job.status -eq "SUCCESS") { "Green" } elseif ($job.status -eq "RUNNING") { "Yellow" } else { "Red" }
    Write-Host "  [$($job.job_type)] Status: $($job.status) (Results: $($job.result_count))" -ForegroundColor $statusColor
}
Write-Host ""

Write-Host "======================================" -ForegroundColor Green
Write-Host "✅ ALL TESTS COMPLETE!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

Write-Host "📊 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Open Dashboard: http://localhost:3000" -ForegroundColor Yellow
Write-Host "2. Check logs: docker-compose logs -f app" -ForegroundColor Yellow
Write-Host "3. Wait for jobs to complete (5-10 min)" -ForegroundColor Yellow
Write-Host "4. Verify signals appear in API" -ForegroundColor Yellow
Write-Host ""

Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "- IMPROVEMENTS_COMPLETE_GUIDE.md" -ForegroundColor Gray
Write-Host "- LINKEDIN_INSTAGRAM_SETUP.md" -ForegroundColor Gray
Write-Host ""
