#!/usr/bin/env pwsh
# F2F dev helper (PowerShell) — thin wrapper around docker compose.
# Usage:
#   .\infra\scripts\dev.ps1 up           # start stack (detached)
#   .\infra\scripts\dev.ps1 down         # stop stack
#   .\infra\scripts\dev.ps1 logs [svc]   # tail logs, optionally a single service
#   .\infra\scripts\dev.ps1 migrate      # run `alembic upgrade head` inside api
#   .\infra\scripts\dev.ps1 shell [svc]  # open a shell inside a service (default: api)

[CmdletBinding()]
param(
    [Parameter(Position = 0)] [string]$Command = 'up',
    [Parameter(Position = 1)] [string]$Service = ''
)

$ErrorActionPreference = 'Stop'

# Run commands from the repo root (parent of infra/)
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '../..')
Push-Location $repoRoot
try {
    switch ($Command) {
        'up'      { docker compose up -d --build }
        'down'    { docker compose down }
        'logs'    {
            if ($Service) { docker compose logs -f $Service }
            else          { docker compose logs -f }
        }
        'migrate' { docker compose exec api alembic upgrade head }
        'shell'   {
            $svc = if ($Service) { $Service } else { 'api' }
            docker compose exec $svc /bin/bash
        }
        default   {
            Write-Error "Unknown command: $Command. Expected: up | down | logs | migrate | shell"
            exit 2
        }
    }
}
finally {
    Pop-Location
}
