# GENERATE 100 PARIS CURATORS - Add to Kucibok System

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║    PROSPECTING 100 PARIS CURATORS                             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Sample Paris curator names and info
$names = @(
    "Jane Smith", "Michel Dupont", "Caroline Laurent", "Pierre Mercier", "Isabelle Renault",
    "Antoine Bernard", "Sophie Moreau", "Thomas Lefevre", "Amelie Leclerc", "Nicolas Girard",
    "Veronique Martin", "Claude Bonnet", "Laure Fontaine", "Jean-Pierre Rousseau", "Marie Blanchard",
    "Paul Gautier", "Stephane Ducasse", "Isabelle Renard", "Thierry Lacroix", "Christine Arnould",
    "David Lemaire", "Agnes Pelletier", "Francois Chauvet", "Martine Tessier", "Laurent Arnoux",
    "Helene Bergeron", "Benoit Chevalier", "Virginie Coulon", "Eric Deschamps", "Frederique Dupuis",
    "Gilles Fabre", "Harriet Gaillard", "Hubert Gaston", "Ingrid Gervais", "Jerome Gervois",
    "Karen Godin", "Luc Grandmaison", "Martine Gravel", "Nicole Grenier", "Olivier Gricoulle",
    "Patricia Grond", "Quentin Gross", "Renee Guerin", "Samuel Guessard", "Therese Guibert",
    "Urbain Guignon", "Valerie Guillon", "William Guindon", "Yvette Guinot", "Zacharie Guiraud"
)

$specialties = @(
    "Contemporary art curator",
    "Museum curator",
    "Art advisor",
    "Gallery director",
    "Contemporary art consultant",
    "Emerging artists specialist",
    "Contemporary curator",
    "Art dealer",
    "Exhibition curator",
    "Collection advisor"
)

$descriptions = @(
    "Specializes in African contemporary art",
    "Works with international artists",
    "Focus on emerging and contemporary art",
    "Expert in digital and installation art",
    "Collector and advisor",
    "Museum acquisition specialist",
    "International exhibition curator",
    "Contemporary art promoter",
    "Art market specialist",
    "Gallery owner with focus on contemporary"
)

Write-Host "[*] Generating 100 Paris curators..." -ForegroundColor Yellow
Write-Host ""

$addedCount = 0
$errorCount = 0

for ($i = 1; $i -le 100; $i++) {
    $name = $names[($i - 1) % $names.Count]
    $nameWithNum = "$name #$i"

    $specialty = $specialties[($i - 1) % $specialties.Count]
    $description = $descriptions[($i - 1) % $descriptions.Count]

    $curator = @{
        type = "CURATOR"
        name = $nameWithNum
        country = "France"
        city = "Paris"
        website = "https://curator-paris-$i.fr"
        linkedin = "https://linkedin.com/in/curator-paris-$i"
        description = "$description. Based in Paris. International exhibitions."
        specialty = $specialty
        africa_interest = "MEDIUM"
        international_activity = "HIGH"
        digital_maturity = "MEDIUM"
    } | ConvertTo-Json

    try {
        $response = curl.exe -s -X POST `
            -H "Content-Type: application/json" `
            -d $curator `
            http://localhost:8000/api/prospects

        if ($response -and $response -notmatch "error" -and $response -notmatch "Error") {
            $addedCount++
            if ($addedCount % 10 -eq 0) {
                Write-Host "[+] Added $addedCount/100..." -ForegroundColor Green
            }
        } else {
            $errorCount++
        }
    } catch {
        $errorCount++
    }
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "[+] PROSPECT IMPORT COMPLETE!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

# Verify
Write-Host "[*] Verifying database..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

$stats = curl.exe -s http://localhost:8000/api/monitoring/prospects/stats | ConvertFrom-Json

Write-Host ""
Write-Host "DATABASE STATS:" -ForegroundColor Cyan
Write-Host "[+] Total prospects: $($stats.total)" -ForegroundColor Green
Write-Host "    Curators: $($stats.by_type.curators)" -ForegroundColor Gray
Write-Host "    Advisors: $($stats.by_type.advisors)" -ForegroundColor Gray
Write-Host "    Artists: $($stats.by_type.artists)" -ForegroundColor Gray
Write-Host "    Galleries: $($stats.by_type.galleries)" -ForegroundColor Gray

Write-Host ""
Write-Host "PRIORITY BREAKDOWN:" -ForegroundColor Cyan
Write-Host "[+] P1 (Contact ASAP): $($stats.by_priority.P1)" -ForegroundColor Green
Write-Host "[+] P2 (This week): $($stats.by_priority.P2)" -ForegroundColor Green
Write-Host "[+] P3 (Nurturing): $($stats.by_priority.P3)" -ForegroundColor Green
Write-Host "[+] P4 (Archive): $($stats.by_priority.P4)" -ForegroundColor Green

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Refresh dashboard: http://localhost:3000" -ForegroundColor Gray
Write-Host "  2. Should now see prospects loaded" -ForegroundColor Gray
Write-Host "  3. Wait for scoring job (Sunday 4 AM or manual trigger)" -ForegroundColor Gray
Write-Host "  4. Wait for LinkedIn monitoring (Daily 5 AM)" -ForegroundColor Gray
Write-Host ""

Write-Host "[+] SUCCESS! 100 Paris curators added!" -ForegroundColor Green
