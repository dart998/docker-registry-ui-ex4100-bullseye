$ErrorActionPreference = "Stop"

$Image = "ovelayos/docker-registry-ui-wd-ex4100"
$Tag = "2.6.0-bullseye-r2"

Write-Host "Building and pushing $Image`:$Tag for linux/arm/v7..."

docker buildx build `
  --platform linux/arm/v7 `
  --no-cache `
  -t "$Image`:$Tag" `
  -t "$Image`:latest" `
  --push `
  .

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Published:"
Write-Host "  $Image`:$Tag"
Write-Host "  $Image`:latest"
