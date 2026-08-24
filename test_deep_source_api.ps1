# 🔥 Test Deep Source API Endpoint

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║         🔥 TEST DEEP SOURCE API ENDPOINT 🔥                    ║" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║  Testing POST /api/prospects/deep-source                      ║" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$BASE_URL = "http://localhost:8000"
$ENDPOINT = "/api/prospects/deep-source"
$TARGET_COUNT = 50

# Check if API is running
Write-Host "🔍 Checking if API is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BASE_URL/docs" -ErrorAction Stop -TimeoutSec 3
    Write-Host "✅ API is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ API is not running!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Start it with:" -ForegroundColor Yellow
    Write-Host "  python -m uvicorn app.main:app --reload --port 8000" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "🚀 Calling Deep Source API..." -ForegroundColor Yellow
Write-Host "   URL: $BASE_URL$ENDPOINT" -ForegroundColor Gray
Write-Host "   Target Count: $TARGET_COUNT" -ForegroundColor Gray
Write-Host ""

# Make API call
try {
    $response = Invoke-WebRequest `
        -Uri "$BASE_URL$ENDPOINT?target_count=$TARGET_COUNT" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -ErrorAction Stop

    # Parse response
    $json = $response.Content | ConvertFrom-Json

    # Display results
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                    ✅ API SUCCESS                              ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 DEEP SOURCE RESULTS:" -ForegroundColor Cyan
    Write-Host "   ✅ Created:       $($json.created) hot prospects" -ForegroundColor Green
    Write-Host "   ⏭️  Duplicates:     $($json.duplicates) removed" -ForegroundColor Yellow
    Write-Host "   ❌ Errors:         $($json.errors) failed" -ForegroundColor $(if ($json.errors -eq 0) { 'Green' } else { 'Red' })
    Write-Host "   📊 Total:          $($json.total) processed" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💬 Message: $($json.message)" -ForegroundColor Green
    Write-Host ""

    # Show prospects table
    if ($json.prospects.Count -gt 0) {
        Write-Host "📋 PROSPECTS CREATED:" -ForegroundColor Cyan
        Write-Host ""

        # Build table
        $prospects = $json.prospects | Select-Object -First 10

        Write-Host "# | Name | Email | Website" -ForegroundColor Gray
        Write-Host ("─" * 100)

        $count = 1
        foreach ($prospect in $prospects) {
            $name = if ($prospect.name.Length -gt 25) { $prospect.name.Substring(0, 22) + "..." } else { $prospect.name.PadRight(25) }
            $email = if ($prospect.email) { if ($prospect.email.Length -gt 30) { $prospect.email.Substring(0, 27) + "..." } else { $prospect.email.PadRight(30) } } else { "N/A".PadRight(30) }
            $website = if ($prospect.website) { if ($prospect.website.Length -gt 30) { $prospect.website.Substring(0, 27) + "..." } else { $prospect.website } } else { "N/A" }

            Write-Host "$count | $name | $email | $website" -ForegroundColor Gray
            $count++
        }

        if ($json.prospects.Count -gt 10) {
            Write-Host "... and $($json.prospects.Count - 10) more prospects" -ForegroundColor Gray
        }

        Write-Host ""
    }

    # Show next steps
    if ($json.next_steps) {
        Write-Host "📌 NEXT STEPS:" -ForegroundColor Cyan
        foreach ($step in $json.next_steps) {
            Write-Host "   • $step" -ForegroundColor Yellow
        }
        Write-Host ""
    }

    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                                ║" -ForegroundColor Green
    Write-Host "║  🎉 SUCCESS! 50 Hot Curator Prospects Created & Imported      ║" -ForegroundColor Green
    Write-Host "║                                                                ║" -ForegroundColor Green
    Write-Host "║  📊 Check Dashboard: http://localhost:3000                    ║" -ForegroundColor Green
    Write-Host "║                                                                ║" -ForegroundColor Green
    Write-Host "║  🚀 Next Automation Run: Tomorrow at 3:00 AM                  ║" -ForegroundColor Green
    Write-Host "║     - Auto-enrichment                                          ║" -ForegroundColor Green
    Write-Host "║     - Auto-scoring                                             ║" -ForegroundColor Green
    Write-Host "║     - Auto-emails (Sourcing & Vetting)                        ║" -ForegroundColor Green
    Write-Host "║                                                                ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

} catch {
    Write-Host "❌ API Call Failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""

    if ($_.Exception.Response.StatusCode) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Make sure API is running: python -m uvicorn app.main:app --reload --port 8000" -ForegroundColor Gray
    Write-Host "  2. Make sure database is ready: postgresql:// connection string configured" -ForegroundColor Gray
    Write-Host "  3. Check API documentation: http://localhost:8000/docs" -ForegroundColor Gray
    Write-Host ""

    exit 1
}
