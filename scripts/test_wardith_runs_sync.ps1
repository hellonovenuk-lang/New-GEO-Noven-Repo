$ErrorActionPreference = 'Stop'

function Assert-True([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

function Invoke-Git([string]$WorkingDirectory, [string[]]$Arguments) {
    $output = & git -C $WorkingDirectory @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed: $output"
    }
    return $output
}

$root = Join-Path ([System.IO.Path]::GetTempPath()) ("wardith-sync-test-" + [guid]::NewGuid())
$seed = Join-Path $root 'seed'
$remote = Join-Path $root 'remote.git'
$clone = Join-Path $root 'clone'
$runs = Join-Path $root 'runs'
$script = Join-Path $PSScriptRoot 'wardith-runs-sync.ps1'

try {
    New-Item -ItemType Directory -Path $seed | Out-Null
    Invoke-Git $seed @('init', '-b', 'main') | Out-Null
    Invoke-Git $seed @('config', 'user.email', 'sync-test@example.invalid') | Out-Null
    Invoke-Git $seed @('config', 'user.name', 'Wardith Sync Test') | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $seed 'crm') | Out-Null
    Set-Content -LiteralPath (Join-Path $seed 'crm/wardith.db') -Value 'remote-db-v1' -NoNewline
    Set-Content -LiteralPath (Join-Path $seed 'campaign.json') -Value '{"version":1}' -NoNewline
    Invoke-Git $seed @('add', '-A') | Out-Null
    Invoke-Git $seed @('commit', '-m', 'seed') | Out-Null
    & git clone --bare $seed $remote 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'failed to create bare remote' }

    $env:WARDITH_SYNC_REPO_URL = $remote
    $env:WARDITH_SYNC_CLONE_DIR = $clone
    $env:WARDITH_SYNC_RUNS_DIR = $runs

    & $script pull
    if ($LASTEXITCODE -ne 0) { throw 'initial pull failed' }
    Assert-True (Test-Path -LiteralPath (Join-Path $runs 'campaign.json')) 'pull did not copy campaign data'
    Assert-True ((Get-Content -Raw (Join-Path $runs 'crm/wardith.db')) -eq 'remote-db-v1') 'pull did not copy the CRM database'

    Set-Content -LiteralPath (Join-Path $runs 'crm/wardith.db') -Value 'local-unsynced-change' -NoNewline
    Set-Content -LiteralPath (Join-Path $seed 'crm/wardith.db') -Value 'remote-db-v2' -NoNewline
    Invoke-Git $seed @('add', '-A') | Out-Null
    Invoke-Git $seed @('commit', '-m', 'remote db update') | Out-Null
    Invoke-Git $seed @('push', $remote, 'main') | Out-Null

    $protectivePullOutput = (& $script pull 3>&1 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) { throw 'protective pull failed' }
    Assert-True (-not $protectivePullOutput.Contains('pull failed')) 'a successful git pull was reported as failed'
    Assert-True ((Get-Content -Raw (Join-Path $runs 'crm/wardith.db')) -eq 'local-unsynced-change') 'pull overwrote a locally changed CRM database'

    Set-Content -LiteralPath (Join-Path $runs 'new-run.json') -Value '{"ready":true}' -NoNewline
    Set-Content -LiteralPath (Join-Path $runs 'crm/wardith.db-wal') -Value 'transient' -NoNewline
    & $script push 'sync test update'
    if ($LASTEXITCODE -ne 0) { throw 'push failed' }
    Invoke-Git $seed @('pull', $remote, 'main') | Out-Null
    Assert-True (Test-Path -LiteralPath (Join-Path $seed 'new-run.json')) 'push did not publish run data'
    Assert-True (-not (Test-Path -LiteralPath (Join-Path $seed 'crm/wardith.db-wal'))) 'push included a transient SQLite file'

    Write-Host 'wardith-runs-sync.ps1 integration tests passed'
}
finally {
    Remove-Item Env:WARDITH_SYNC_REPO_URL -ErrorAction SilentlyContinue
    Remove-Item Env:WARDITH_SYNC_CLONE_DIR -ErrorAction SilentlyContinue
    Remove-Item Env:WARDITH_SYNC_RUNS_DIR -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
