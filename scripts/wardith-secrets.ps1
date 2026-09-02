$ErrorActionPreference = 'Stop'

$requiredKeys = @(
    'OPENAI_API_KEY', 'OPENAI_MODEL',
    'GEMINI_API_KEY', 'GEMINI_MODEL',
    'PERPLEXITY_API_KEY', 'PERPLEXITY_MODEL',
    'COMPANIES_HOUSE_API_KEY', 'ZOHO_CREDENTIALS_JSON'
)
$configDir = if ($env:WARDITH_SECRETS_CONFIG_DIR) {
    $env:WARDITH_SECRETS_CONFIG_DIR
} else {
    Join-Path $HOME '.wardith/secrets-manager'
}
$configPath = Join-Path $configDir 'config.json'
$tokenPath = Join-Path $configDir 'token.dpapi'
$bws = if ($env:WARDITH_BWS_CLI) { $env:WARDITH_BWS_CLI } else { 'bws' }

function Get-PlainText([Security.SecureString]$SecureValue) {
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureValue)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
}

function Read-StoredConfiguration {
    if (-not (Test-Path -LiteralPath $configPath) -or -not (Test-Path -LiteralPath $tokenPath)) {
        throw 'Bitwarden is not configured. Run: pwsh -File scripts/wardith-secrets.ps1 setup <project-id>'
    }
    $config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json
    if ([string]::IsNullOrWhiteSpace($config.projectId)) { throw 'Bitwarden configuration has no project ID.' }
    $secureToken = Get-Content -Raw -LiteralPath $tokenPath | ConvertTo-SecureString
    return @{ ProjectId = $config.projectId; Token = Get-PlainText $secureToken }
}

function Get-WardithSecrets {
    $stored = Read-StoredConfiguration
    $previousToken = [Environment]::GetEnvironmentVariable('BWS_ACCESS_TOKEN', 'Process')
    try {
        [Environment]::SetEnvironmentVariable('BWS_ACCESS_TOKEN', $stored.Token, 'Process')
        $json = & $bws secret list $stored.ProjectId --output json 2>$null
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($json -join "`n"))) {
            throw 'Bitwarden secret retrieval failed. Check the machine token, project access, and network connection.'
        }
    }
    finally {
        [Environment]::SetEnvironmentVariable('BWS_ACCESS_TOKEN', $previousToken, 'Process')
        $stored.Token = $null
    }

    try { $items = ($json -join "`n") | ConvertFrom-Json }
    catch { throw 'Bitwarden returned malformed secret data.' }
    $values = @{}
    foreach ($item in $items) {
        if ($requiredKeys -contains $item.key -and -not [string]::IsNullOrEmpty([string]$item.value)) {
            $values[$item.key] = [string]$item.value
        }
    }
    $missing = @($requiredKeys | Where-Object { -not $values.ContainsKey($_) })
    if ($missing.Count -gt 0) {
        throw "Bitwarden is missing required secret(s): $($missing -join ', ')"
    }
    try { $zoho = $values.ZOHO_CREDENTIALS_JSON | ConvertFrom-Json }
    catch { throw 'Bitwarden secret ZOHO_CREDENTIALS_JSON is not valid JSON.' }
    $requiredZohoFields = @('client_id', 'client_secret', 'refresh_token', 'account_id', 'api_domain', 'accounts_domain')
    $missingZohoFields = @($requiredZohoFields | Where-Object {
        -not $zoho.PSObject.Properties[$_] -or [string]::IsNullOrWhiteSpace([string]$zoho.$_)
    })
    if ($missingZohoFields.Count -gt 0) {
        throw "Bitwarden secret ZOHO_CREDENTIALS_JSON is missing field(s): $($missingZohoFields -join ', ')"
    }
    return $values
}

function Invoke-Setup([string]$ProjectId) {
    if ([string]::IsNullOrWhiteSpace($ProjectId)) { throw 'setup requires the Bitwarden Secrets Manager project ID.' }
    if (-not (Get-Command $bws -ErrorAction SilentlyContinue)) { throw 'Bitwarden Secrets Manager CLI (bws) is not installed or not on PATH.' }
    $secureToken = Read-Host 'Bitwarden read-only machine access token' -AsSecureString
    $plainToken = Get-PlainText $secureToken
    $previousToken = [Environment]::GetEnvironmentVariable('BWS_ACCESS_TOKEN', 'Process')
    try {
        [Environment]::SetEnvironmentVariable('BWS_ACCESS_TOKEN', $plainToken, 'Process')
        $check = & $bws secret list $ProjectId --output json 2>$null
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($check -join "`n"))) {
            throw 'Bitwarden rejected the token or it cannot read that project; nothing was saved.'
        }
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        ConvertFrom-SecureString $secureToken | Set-Content -LiteralPath $tokenPath -NoNewline
        @{ projectId = $ProjectId } | ConvertTo-Json | Set-Content -LiteralPath $configPath
    }
    finally {
        [Environment]::SetEnvironmentVariable('BWS_ACCESS_TOKEN', $previousToken, 'Process')
        $plainToken = $null
    }
    Write-Host 'Wardith Bitwarden access configured for this Windows account.'
}

function Invoke-Status {
    $values = Get-WardithSecrets
    Write-Host "Bitwarden connection ready: $($requiredKeys.Count) required secrets available."
    $values.Clear()
}

function Invoke-WithSecrets([string[]]$ChildCommand) {
    if ($ChildCommand.Count -eq 0) { throw 'run requires a command to execute.' }
    $values = Get-WardithSecrets
    $tempDir = Join-Path ([IO.Path]::GetTempPath()) ('wardith-secrets-' + [guid]::NewGuid())
    $zohoPath = Join-Path $tempDir 'zoho-credentials.json'
    $names = @($requiredKeys | Where-Object { $_ -ne 'ZOHO_CREDENTIALS_JSON' }) + 'WARDITH_ZOHO_CREDENTIALS'
    $previous = @{}
    foreach ($name in $names) { $previous[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
    try {
        New-Item -ItemType Directory -Path $tempDir | Out-Null
        [IO.File]::WriteAllText($zohoPath, $values.ZOHO_CREDENTIALS_JSON, [Text.UTF8Encoding]::new($false))
        foreach ($name in $requiredKeys) {
            if ($name -ne 'ZOHO_CREDENTIALS_JSON') {
                [Environment]::SetEnvironmentVariable($name, $values[$name], 'Process')
            }
        }
        [Environment]::SetEnvironmentVariable('WARDITH_ZOHO_CREDENTIALS', $zohoPath, 'Process')
        & $ChildCommand[0] @($ChildCommand | Select-Object -Skip 1)
        $childExit = $LASTEXITCODE
    }
    finally {
        foreach ($name in $names) { [Environment]::SetEnvironmentVariable($name, $previous[$name], 'Process') }
        $values.Clear()
        Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    exit $childExit
}

try {
    $action = if ($args.Count -gt 0) { $args[0] } else { 'status' }
    switch ($action) {
        'setup' { Invoke-Setup $(if ($args.Count -gt 1) { $args[1] } else { $null }) }
        'status' { Invoke-Status }
        'run' { Invoke-WithSecrets @($args | Select-Object -Skip 1) }
        default { throw "Unknown action '$action'. Use setup, status, or run." }
    }
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
