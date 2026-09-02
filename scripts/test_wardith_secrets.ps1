$ErrorActionPreference = 'Stop'

function Assert-True([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

$root = Join-Path ([System.IO.Path]::GetTempPath()) ("wardith-secrets-test-" + [guid]::NewGuid())
$configDir = Join-Path $root 'config'
$binDir = Join-Path $root 'bin'
$probe = Join-Path $root 'probe.ps1'
$result = Join-Path $root 'result.json'
$script = Join-Path $PSScriptRoot 'wardith-secrets.ps1'
$powershell = (Get-Process -Id $PID).Path

try {
    New-Item -ItemType Directory -Path $configDir, $binDir | Out-Null

    $secureToken = ConvertTo-SecureString 'machine-token-for-test' -AsPlainText -Force
    ConvertFrom-SecureString $secureToken | Set-Content -LiteralPath (Join-Path $configDir 'token.dpapi') -NoNewline
    '{"projectId":"project-for-test"}' | Set-Content -LiteralPath (Join-Path $configDir 'config.json') -NoNewline

    @'
@echo off
echo [{"key":"OPENAI_API_KEY","value":"openai-test"},{"key":"OPENAI_MODEL","value":"gpt-test"},{"key":"GEMINI_API_KEY","value":"gemini-test"},{"key":"GEMINI_MODEL","value":"gemini-model-test"},{"key":"PERPLEXITY_API_KEY","value":"perplexity-test"},{"key":"PERPLEXITY_MODEL","value":"sonar-test"},{"key":"COMPANIES_HOUSE_API_KEY","value":"ch-test"},{"key":"ZOHO_CREDENTIALS_JSON","value":"{\"client_id\":\"id\",\"client_secret\":\"secret\",\"refresh_token\":\"refresh\",\"account_id\":\"123\",\"api_domain\":\"https://mail.zoho.eu\",\"accounts_domain\":\"https://accounts.zoho.eu\"}"},{"key":"UNEXPECTED_SECRET","value":"must-not-leak"}]
'@ | Set-Content -LiteralPath (Join-Path $binDir 'bws.cmd')

    @'
param([string]$ResultPath)
$names = @('OPENAI_API_KEY','OPENAI_MODEL','GEMINI_API_KEY','GEMINI_MODEL','PERPLEXITY_API_KEY','PERPLEXITY_MODEL','COMPANIES_HOUSE_API_KEY')
$values = @{}
foreach ($name in $names) { $values[$name] = [Environment]::GetEnvironmentVariable($name) }
$zohoPath = [Environment]::GetEnvironmentVariable('WARDITH_ZOHO_CREDENTIALS')
[ordered]@{
    values = $values
    zoho_path = $zohoPath
    zoho_exists_during_run = Test-Path -LiteralPath $zohoPath
    unexpected = [Environment]::GetEnvironmentVariable('UNEXPECTED_SECRET')
    bws_token = [Environment]::GetEnvironmentVariable('BWS_ACCESS_TOKEN')
} | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $ResultPath
'@ | Set-Content -LiteralPath $probe

    $env:WARDITH_SECRETS_CONFIG_DIR = $configDir
    $env:WARDITH_BWS_CLI = Join-Path $binDir 'bws.cmd'
    & $script run $powershell -NoProfile -File $probe $result
    if ($LASTEXITCODE -ne 0) { throw 'secret-wrapped child process failed' }

    $observed = Get-Content -Raw $result | ConvertFrom-Json
    Assert-True ($observed.values.OPENAI_API_KEY -eq 'openai-test') 'allowed API key was not injected'
    Assert-True ($observed.values.COMPANIES_HOUSE_API_KEY -eq 'ch-test') 'Companies House key was not injected'
    Assert-True $observed.zoho_exists_during_run 'temporary Zoho credentials were unavailable to the child'
    Assert-True (-not (Test-Path -LiteralPath $observed.zoho_path)) 'temporary Zoho credentials remained after the child exited'
    Assert-True ([string]::IsNullOrEmpty($observed.unexpected)) 'an unapproved Bitwarden secret leaked into the child'
    Assert-True ([string]::IsNullOrEmpty($observed.bws_token)) 'the Bitwarden machine token leaked into the child'

    $missingCli = Join-Path $binDir 'missing-secret-bws.cmd'
    '@echo [{"key":"OPENAI_API_KEY","value":"only-one"}]' | Set-Content -LiteralPath $missingCli
    $env:WARDITH_BWS_CLI = $missingCli
    $ErrorActionPreference = 'Continue'
    $missingOutput = (& $powershell -NoProfile -ExecutionPolicy Bypass -File $script run $powershell -NoProfile -Command 'exit 0' 2>&1 | Out-String)
    $missingExit = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    Assert-True ($missingExit -ne 0) 'missing required secrets did not stop execution'
    Assert-True ($missingOutput -match 'missing\s+required\s+secret') 'missing-secret failure was not explained safely'
    Assert-True (-not ($missingOutput -match 'only-one|machine-token-for-test')) 'a secret appeared in failure output'

    $badZohoCli = Join-Path $binDir 'bad-zoho-bws.cmd'
    (Get-Content -Raw (Join-Path $binDir 'bws.cmd')).Replace('\"client_id\":\"id\",\"client_secret\":\"secret\",\"refresh_token\":\"refresh\",\"account_id\":\"123\",\"api_domain\":\"https://mail.zoho.eu\",\"accounts_domain\":\"https://accounts.zoho.eu\"', '') |
        Set-Content -LiteralPath $badZohoCli
    $env:WARDITH_BWS_CLI = $badZohoCli
    $marker = Join-Path $root 'child-ran'
    $ErrorActionPreference = 'Continue'
    $badZohoOutput = (& $powershell -NoProfile -ExecutionPolicy Bypass -File $script run $powershell -NoProfile -Command "Set-Content -LiteralPath '$marker' -Value ran" 2>&1 | Out-String)
    $badZohoExit = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    Assert-True ($badZohoExit -ne 0) 'malformed Zoho credentials did not stop execution'
    Assert-True (-not (Test-Path -LiteralPath $marker)) 'child ran with malformed Zoho credentials'
    Assert-True ($badZohoOutput -match 'missing field') 'malformed Zoho failure did not identify its safe cause'

    Write-Host 'wardith-secrets.ps1 integration tests passed'
}
finally {
    Remove-Item Env:WARDITH_SECRETS_CONFIG_DIR -ErrorAction SilentlyContinue
    Remove-Item Env:WARDITH_BWS_CLI -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
