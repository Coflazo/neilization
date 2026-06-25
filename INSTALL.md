# Install neilization

Install once, then trigger the skill from Claude with `/neilization`, `neilize this`, or `make this more cosmic`.

## One-Line Install

macOS / Linux / WSL / Git Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/Coflazo/neilization/main/install.sh | bash
```

Windows PowerShell 5.1+:

```powershell
irm https://raw.githubusercontent.com/Coflazo/neilization/main/install.ps1 | iex
```

The installer always installs the Claude skill at:

```text
~/.claude/skills/neilization/
```

It also installs a copy for Codex when it finds `CODEX_HOME` or an existing `~/.codex/` directory:

```text
$CODEX_HOME/skills/neilization/
~/.codex/skills/neilization/
```

It skips agent homes it cannot find. It is safe to re-run.

## Manual Install

Clone the repository:

```bash
git clone https://github.com/Coflazo/neilization.git
```

Copy the package into Claude:

```bash
mkdir -p ~/.claude/skills
cp -R neilization ~/.claude/skills/neilization
```

Validate:

```bash
node ~/.claude/skills/neilization/scripts/validate.mjs
```

## Custom Paths

Set `CLAUDE_HOME` before running the installer:

```bash
CLAUDE_HOME=/path/to/.claude curl -fsSL https://raw.githubusercontent.com/Coflazo/neilization/main/install.sh | bash
```

Set `CODEX_HOME` to force Codex installation:

```bash
CODEX_HOME=/path/to/.codex curl -fsSL https://raw.githubusercontent.com/Coflazo/neilization/main/install.sh | bash
```

PowerShell:

```powershell
$env:CLAUDE_HOME = "C:\Users\you\.claude"
$env:CODEX_HOME = "C:\Users\you\.codex"
irm https://raw.githubusercontent.com/Coflazo/neilization/main/install.ps1 | iex
```

## What Gets Installed

```text
neilization/
|-- SKILL.md
|-- README.md
|-- INSTALL.md
|-- assets/
|   `-- neilization_backgroundless.png
|-- references/
|   |-- examples.md
|   |-- formulaic-vocabulary.md
|   |-- safety-and-integrity.md
|   |-- structural-patterns.md
|   `-- voice-patterns.md
`-- scripts/
    `-- validate.mjs
```

The installer overwrites managed package files and managed subdirectories inside the target skill folder. It does not touch unrelated agent settings.

## Troubleshooting

If install fails:

1. Confirm `curl` and `tar` exist on macOS / Linux / WSL / Git Bash.
2. Confirm PowerShell can download from GitHub on Windows.
3. Confirm the repository is reachable: `https://github.com/Coflazo/neilization`.
4. Run the validator after install.

If you want the agent to repair its own install, open the agent and say:

```text
Read README.md and INSTALL.md, install neilization for me.
```

## Updating

Re-run the same one-line installer. It refreshes the managed skill files in place.
