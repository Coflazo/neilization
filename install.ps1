$ErrorActionPreference = "Stop"

$RepoZip = if ($env:NEILIZATION_ZIP_URL) {
  $env:NEILIZATION_ZIP_URL
} else {
  "https://github.com/Coflazo/neilization/archive/refs/heads/main.zip"
}

$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("neilization-" + [System.Guid]::NewGuid().ToString("N"))
$ZipPath = Join-Path $TempRoot "neilization.zip"

function Install-Neilization {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$Target
  )

  New-Item -ItemType Directory -Force -Path $Target | Out-Null

  foreach ($DirName in @("assets", "references", "scripts")) {
    $ManagedPath = Join-Path $Target $DirName
    if (Test-Path $ManagedPath) {
      Remove-Item -Recurse -Force $ManagedPath
    }
  }

  Copy-Item (Join-Path $Source "SKILL.md") $Target -Force
  Copy-Item (Join-Path $Source "README.md") $Target -Force
  Copy-Item (Join-Path $Source "INSTALL.md") $Target -Force
  Copy-Item (Join-Path $Source "assets") $Target -Recurse -Force
  Copy-Item (Join-Path $Source "references") $Target -Recurse -Force
  Copy-Item (Join-Path $Source "scripts") $Target -Recurse -Force

  Write-Host "Installed: $Target"
}

try {
  New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
  Write-Host "Downloading neilization..."
  Invoke-WebRequest -Uri $RepoZip -OutFile $ZipPath
  Expand-Archive -Path $ZipPath -DestinationPath $TempRoot -Force

  $SourceDir = Get-ChildItem -Path $TempRoot -Directory |
    Where-Object { $_.Name -like "neilization-*" } |
    Select-Object -First 1

  if (-not $SourceDir -or -not (Test-Path (Join-Path $SourceDir.FullName "SKILL.md"))) {
    throw "Downloaded archive did not contain SKILL.md"
  }

  $Installed = 0
  $ClaudeHome = if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $HOME ".claude" }
  Install-Neilization -Source $SourceDir.FullName -Target (Join-Path $ClaudeHome "skills\neilization")
  $Installed += 1

  if ($env:CODEX_HOME) {
    Install-Neilization -Source $SourceDir.FullName -Target (Join-Path $env:CODEX_HOME "skills\neilization")
    $Installed += 1
  } else {
    $CodexHome = Join-Path $HOME ".codex"
    if (Test-Path $CodexHome) {
      Install-Neilization -Source $SourceDir.FullName -Target (Join-Path $CodexHome "skills\neilization")
      $Installed += 1
    }
  }

  Write-Host ""
  Write-Host "neilization installed for $Installed supported agent home(s)."
  Write-Host "Trigger with: /neilization, 'neilize this', or 'make this more cosmic'."
  Write-Host "Validate with: node $(Join-Path $ClaudeHome 'skills\neilization\scripts\validate.mjs')"
} finally {
  if (Test-Path $TempRoot) {
    Remove-Item -Recurse -Force $TempRoot
  }
}
