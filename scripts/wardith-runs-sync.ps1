[CmdletBinding()]
param(
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet('pull', 'push')]
    [string]$Command,

    [Parameter(Position = 1)]
    [string]$Message = 'Sync wardith-runs data'
)

$ErrorActionPreference = 'Stop'
$userProfile = [Environment]::GetFolderPath('UserProfile')
$repoUrl = if ($env:WARDITH_SYNC_REPO_URL) { $env:WARDITH_SYNC_REPO_URL } else { 'https://github.com/hellonovenuk-lang/wardith-crm-data.git' }
$cloneDir = if ($env:WARDITH_SYNC_CLONE_DIR) { $env:WARDITH_SYNC_CLONE_DIR } else { Join-Path $userProfile '.wardith-runs-repo' }
$runsDir = if ($env:WARDITH_SYNC_RUNS_DIR) { $env:WARDITH_SYNC_RUNS_DIR } else { Join-Path $userProfile 'wardith-runs' }
$dbRelativePath = 'crm\wardith.db'
$dbMarker = Join-Path $runsDir 'crm\.last-synced-db-hash'

function Invoke-Git {
    param([string[]]$Arguments, [switch]$AllowFailure)
    $gitOutput = & git @Arguments 2>&1
    $exitCode = $LASTEXITCODE
    if ($gitOutput) { $gitOutput | ForEach-Object { Write-Host $_ } }
    if ($exitCode -ne 0 -and -not $AllowFailure) {
        throw "git $($Arguments -join ' ') failed with exit code $exitCode"
    }
    return $exitCode
}

function Get-FileHashValue([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return '' }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Copy-AdditiveTree {
    param(
        [string]$Source,
        [string]$Destination,
        [scriptblock]$Include
    )
    Get-ChildItem -LiteralPath $Source -Recurse -Force | ForEach-Object {
        $relative = [System.IO.Path]::GetRelativePath($Source, $_.FullName)
        if (& $Include $_ $relative) {
            $target = Join-Path $Destination $relative
            if ($_.PSIsContainer) {
                New-Item -ItemType Directory -Path $target -Force | Out-Null
            }
            else {
                New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
                Copy-Item -LiteralPath $_.FullName -Destination $target -Force
            }
        }
    }
}

if ($Command -eq 'pull') {
    if (-not (Test-Path -LiteralPath (Join-Path $cloneDir '.git'))) {
        Write-Host "wardith-runs-sync: cloning $repoUrl to $cloneDir"
        Invoke-Git @('clone', $repoUrl, $cloneDir) | Out-Null
    }
    else {
        $exitCode = Invoke-Git @('-C', $cloneDir, 'pull', '--ff-only') -AllowFailure
        if ($exitCode -ne 0) {
            Write-Warning "wardith-runs-sync: pull failed; continuing with the existing local repository copy."
        }
    }

    New-Item -ItemType Directory -Path (Join-Path $runsDir 'crm') -Force | Out-Null
    $sourceDb = Join-Path $cloneDir $dbRelativePath
    $localDb = Join-Path $runsDir $dbRelativePath
    if (Test-Path -LiteralPath $sourceDb -PathType Leaf) {
        $localHash = Get-FileHashValue $localDb
        $markerHash = if (Test-Path -LiteralPath $dbMarker) { (Get-Content -Raw -LiteralPath $dbMarker).Trim() } else { '' }
        if (-not $localHash -or $localHash -eq $markerHash) {
            Copy-Item -LiteralPath $sourceDb -Destination $localDb -Force
            Set-Content -LiteralPath $dbMarker -Value (Get-FileHashValue $localDb) -NoNewline
        }
        else {
            Write-Warning "wardith-runs-sync: local wardith.db has changed since the last sync; it was not overwritten. Run push first, then pull again."
        }
    }

    Copy-AdditiveTree $cloneDir $runsDir {
        param($item, $relative)
        return -not ($relative -eq '.git' -or $relative.StartsWith('.git\') -or $relative -eq $dbRelativePath)
    }
    Write-Host 'wardith-runs-sync: pull complete.'
    exit 0
}

if (-not (Test-Path -LiteralPath (Join-Path $cloneDir '.git'))) {
    Write-Warning "wardith-runs-sync: $cloneDir is not a Git checkout. Run pull first."
    exit 0
}
if (-not (Test-Path -LiteralPath $runsDir -PathType Container)) {
    Write-Warning "wardith-runs-sync: $runsDir does not exist; nothing to push."
    exit 0
}

Copy-AdditiveTree $runsDir $cloneDir {
    param($item, $relative)
    if ($item.PSIsContainer) { return $true }
    return $item.Name -notmatch '\.db-(wal|shm|journal)$' -and
        $item.Name -ne '.last-synced-db-hash' -and
        $item.Name -ne '.DS_Store'
}

$localDb = Join-Path $runsDir $dbRelativePath
if (Test-Path -LiteralPath $localDb -PathType Leaf) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $dbMarker) -Force | Out-Null
    Set-Content -LiteralPath $dbMarker -Value (Get-FileHashValue $localDb) -NoNewline
}

Invoke-Git @('-C', $cloneDir, 'add', '-A') | Out-Null
& git -C $cloneDir diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host 'wardith-runs-sync: nothing changed, nothing to push.'
    exit 0
}
if ($LASTEXITCODE -ne 1) { throw "git diff --cached --quiet failed with exit code $LASTEXITCODE" }

Invoke-Git @('-C', $cloneDir, 'commit', '-m', $Message) | Out-Null
$pushExit = Invoke-Git @('-C', $cloneDir, 'push') -AllowFailure
if ($pushExit -ne 0) {
    Write-Warning "wardith-runs-sync: push failed; the data is committed locally in $cloneDir."
    exit 0
}
Write-Host 'wardith-runs-sync: push complete.'
