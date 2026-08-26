# First-time local setup for Catalystdev-dawn
# Run from repo root: .\scripts\setup-local.ps1

$ErrorActionPreference = "Stop"
$Root    = Split-Path $PSScriptRoot -Parent
$Compose = Join-Path $Root "docker-compose.yml"

function Info { param($msg) Write-Host "==> $msg" -ForegroundColor Cyan }
function OK   { param($msg) Write-Host "    $msg" -ForegroundColor Green }
function Warn { param($msg) Write-Host "    $msg" -ForegroundColor Yellow }

# --- 1. Extract media --------------------------------------------------------
Info "Extracting media..."
$MediaArchive = Join-Path $Root "media.tar.gz"
$MediaDir     = Join-Path $Root "media"

if (Test-Path $MediaArchive) {
    if (-not (Test-Path $MediaDir)) {
        New-Item -ItemType Directory $MediaDir | Out-Null
    }
    tar -xzf $MediaArchive -C $Root
    OK "Media extracted to media/"
} else {
    Warn "No media.tar.gz found - images will be missing until media files are added."
}

# --- 2. Ensure .env.local exists ---------------------------------------------
Info "Checking .env.local..."
$EnvLocal = Join-Path $Root ".env.local"
if (-not (Test-Path $EnvLocal)) {
    Copy-Item (Join-Path $Root ".env.example") $EnvLocal
    OK "Created .env.local from .env.example"
} else {
    OK ".env.local already exists."
}

# --- 3. Build image and start container --------------------------------------
Info "Building Docker image and starting container..."
docker compose -f $Compose up -d --build
if ($LASTEXITCODE -ne 0) { throw "docker compose up failed" }
OK "Container started."

# --- 4. Wait for collectstatic + migrate to complete -------------------------
Info "Waiting for app startup (collectstatic + migrate run on container start)..."
$Timeout = 120
$Elapsed = 0
$Ready   = $false

while ($Elapsed -lt $Timeout) {
    $logs = docker compose -f $Compose logs app 2>&1 | Out-String
    if ($logs -match "Booting worker") {
        $Ready = $true
        break
    }
    Start-Sleep -Seconds 3
    $Elapsed += 3
    Write-Host "    ... ${Elapsed}s" -ForegroundColor DarkGray
}

if (-not $Ready) {
    Warn "App did not report ready within ${Timeout}s - check logs with:"
    Warn "  docker compose logs app"
}

# --- 5. Load site content fixture --------------------------------------------
Info "Loading site content from site-content.json..."
docker compose -f $Compose exec app python manage.py loaddata site-content.json
if ($LASTEXITCODE -ne 0) {
    Warn "loaddata returned an error - check output above."
} else {
    OK "Site content loaded."
}

# --- 6. Configure Wagtail Site -----------------------------------------------
Info "Configuring Wagtail Site to localhost:8000..."

$PySite  = "from wagtail.models import Site; "
$PySite += "from home.models import HomePage; "
$PySite += "home = HomePage.objects.filter(live=True).first(); "
$PySite += "print('No HomePage found') if not home else Site.objects.update_or_create("
$PySite += "pk=1, defaults={'hostname':'localhost','port':8000,'root_page':home,"
$PySite += "'site_name':'Catalystdev (local)','is_default_site':True})"

docker compose -f $Compose exec app python manage.py shell -c $PySite
if ($LASTEXITCODE -eq 0) { OK "Wagtail site configured." }

# --- 7. Done -----------------------------------------------------------------
Write-Host ""
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
Write-Host "  Catalystdev local environment is ready" -ForegroundColor Green
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Site:   http://localhost:8000"
Write-Host "  Admin:  http://localhost:8000/admin"
Write-Host ""
Write-Host "  Create a superuser:" -ForegroundColor Yellow
Write-Host "    docker compose exec app python manage.py createsuperuser"
Write-Host ""
Write-Host "  Useful commands:" -ForegroundColor Yellow
Write-Host "    docker compose logs -f app     # tail logs"
Write-Host "    docker compose stop            # stop"
Write-Host "    docker compose down -v         # stop + destroy volumes"
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
