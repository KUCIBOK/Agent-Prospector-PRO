# SEED SAMPLE DATA - Add test prospects to the system

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         ADDING SAMPLE DATA - Test Prospects                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Sample Artists (African contemporary)
$artists = @(
    @{
        "type" = "ARTIST"
        "name" = "Yinka Shonibare"
        "country" = "Nigeria"
        "city" = "Lagos"
        "website" = "https://www.yinkashonibare.com"
        "instagram" = "@yinkashonibare"
        "description" = "Contemporary installation artist. Exhibited at Documenta, Venice Biennale. Works with textiles and technology."
        "specialty" = "Installation art, textiles"
        "africa_interest" = "HIGH"
        "digital_maturity" = "HIGH"
    },
    @{
        "type" = "ARTIST"
        "name" = "El Anatsui"
        "country" = "Ghana"
        "city" = "Accra"
        "website" = "https://www.elanatsui.com"
        "instagram" = "@elanatsui.official"
        "description" = "Sculptor using recycled materials. FIAC participant. International exhibitions worldwide. Studio in Accra."
        "specialty" = "Sculpture, mixed media"
        "africa_interest" = "HIGH"
        "digital_maturity" = "MEDIUM"
    },
    @{
        "type" = "ARTIST"
        "name" = "Cyril Hahn"
        "country" = "Democratic Republic of Congo"
        "city" = "Kinshasa"
        "website" = "https://www.cyrilhahn.com"
        "instagram" = "@cyrilhahn"
        "description" = "Emerging contemporary painter. Active on Instagram (8.2k followers). Participated in 1-54 Contemporary Art Fair."
        "specialty" = "Painting, contemporary"
        "africa_interest" = "HIGH"
        "digital_maturity" = "MEDIUM"
    }
)

# Sample Curators/Art Advisors
$curators = @(
    @{
        "type" = "ART_ADVISOR"
        "name" = "Jane Smith"
        "country" = "France"
        "city" = "Paris"
        "website" = "https://www.janesmith-artadvisor.com"
        "linkedin" = "https://www.linkedin.com/in/janesmith"
        "instagram" = "@janesmith.advisor"
        "description" = "Art advisor specializing in contemporary African art. 15+ years experience. Works with collectors worldwide. Founder of African Art Consulting."
        "specialty" = "Art advisor"
        "africa_interest" = "HIGH"
        "international_activity" = "HIGH"
        "digital_maturity" = "HIGH"
    },
    @{
        "type" = "CURATOR"
        "name" = "Michael Johnson"
        "country" = "United Kingdom"
        "city" = "London"
        "website" = "https://www.michaeljcurator.com"
        "linkedin" = "https://www.linkedin.com/in/michaeljohnson"
        "description" = "Museum curator at prestigious London gallery. Curator of multiple Africa-focused exhibitions. Speaker at international art fairs."
        "specialty" = "Museum curator"
        "africa_interest" = "HIGH"
        "international_activity" = "HIGH"
        "digital_maturity" = "MEDIUM"
    },
    @{
        "type" = "GALLERY"
        "name" = "Galerie Cécile Fakhoury"
        "country" = "Senegal"
        "city" = "Dakar"
        "website" = "https://www.galeriececilefakhoury.com"
        "instagram" = "@galeriececilefakhoury"
        "description" = "Prestigious gallery representing African contemporary artists. Partner of FIAC. Works with top international curators and collectors."
        "specialty" = "Contemporary African art"
        "africa_interest" = "HIGH"
        "international_activity" = "HIGH"
        "digital_maturity" = "HIGH"
    }
)

# Add Artists
Write-Host "[*] Adding sample artists..." -ForegroundColor Yellow
$artistCount = 0

foreach ($artist in $artists) {
    $body = $artist | ConvertTo-Json

    try {
        $response = curl.exe -s -X POST `
            -H "Content-Type: application/json" `
            -d $body `
            http://localhost:8000/api/prospects

        if ($response) {
            Write-Host "    [+] Added: $($artist.name)" -ForegroundColor Green
            $artistCount++
        }
    } catch {
        Write-Host "    [!] Error adding $($artist.name)" -ForegroundColor Red
    }
}

Write-Host "[+] Total artists added: $artistCount" -ForegroundColor Green
Write-Host ""

# Add Curators
Write-Host "[*] Adding sample curators/advisors..." -ForegroundColor Yellow
$curatorCount = 0

foreach ($curator in $curators) {
    $body = $curator | ConvertTo-Json

    try {
        $response = curl.exe -s -X POST `
            -H "Content-Type: application/json" `
            -d $body `
            http://localhost:8000/api/prospects

        if ($response) {
            Write-Host "    [+] Added: $($curator.name)" -ForegroundColor Green
            $curatorCount++
        }
    } catch {
        Write-Host "    [!] Error adding $($curator.name)" -ForegroundColor Red
    }
}

Write-Host "[+] Total curators added: $curatorCount" -ForegroundColor Green
Write-Host ""

# Verify
Write-Host "[*] Verifying data..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

$stats = curl.exe -s http://localhost:8000/api/monitoring/prospects/stats | ConvertFrom-Json

Write-Host "=== DATABASE STATS ===" -ForegroundColor Cyan
Write-Host "[+] Total prospects: $($stats.total)" -ForegroundColor Green
Write-Host "    Artists: $($stats.by_type.artists)" -ForegroundColor Gray
Write-Host "    Advisors: $($stats.by_type.advisors)" -ForegroundColor Gray
Write-Host "    Curators: $($stats.by_type.curators)" -ForegroundColor Gray
Write-Host "    Galleries: $($stats.by_type.galleries)" -ForegroundColor Gray
Write-Host ""

Write-Host "=== NEXT STEPS ===" -ForegroundColor Yellow
Write-Host "[1] Open dashboard: http://localhost:3000" -ForegroundColor Gray
Write-Host "[2] You should see prospects listed now!" -ForegroundColor Gray
Write-Host "[3] Wait 5 sec for page to load and refresh" -ForegroundColor Gray
Write-Host ""

Write-Host "[+] Sample data loaded successfully!" -ForegroundColor Green
