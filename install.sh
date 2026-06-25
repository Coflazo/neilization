#!/usr/bin/env bash
set -euo pipefail

REPO_TARBALL="${NEILIZATION_TARBALL_URL:-https://github.com/Coflazo/neilization/archive/refs/heads/main.tar.gz}"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "neilization install failed: missing required command: $1" >&2
    exit 1
  fi
}

need curl
need tar

echo "Downloading neilization..."
curl -fsSL "$REPO_TARBALL" -o "$TMP_DIR/neilization.tar.gz"
tar -xzf "$TMP_DIR/neilization.tar.gz" -C "$TMP_DIR"
SRC_DIR="$(find "$TMP_DIR" -maxdepth 1 -type d -name 'neilization-*' | head -n 1)"

if [[ -z "${SRC_DIR:-}" || ! -f "$SRC_DIR/SKILL.md" ]]; then
  echo "neilization install failed: downloaded archive did not contain SKILL.md" >&2
  exit 1
fi

install_one() {
  local target="$1"
  mkdir -p "$target"
  rm -rf "$target/assets" "$target/references" "$target/scripts"
  cp "$SRC_DIR/SKILL.md" "$SRC_DIR/README.md" "$SRC_DIR/INSTALL.md" "$target/"
  cp -R "$SRC_DIR/assets" "$SRC_DIR/references" "$SRC_DIR/scripts" "$target/"
  chmod +x "$target/scripts/validate.mjs" 2>/dev/null || true
  echo "Installed: $target"
}

installed=0

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
install_one "$CLAUDE_HOME/skills/neilization"
installed=$((installed + 1))

if [[ -n "${CODEX_HOME:-}" ]]; then
  install_one "$CODEX_HOME/skills/neilization"
  installed=$((installed + 1))
elif [[ -d "$HOME/.codex" ]]; then
  install_one "$HOME/.codex/skills/neilization"
  installed=$((installed + 1))
fi

echo
echo "neilization installed for $installed supported agent home(s)."
echo "Trigger with: /neilization, 'neilize this', or 'make this more cosmic'."
echo "Validate with: node $CLAUDE_HOME/skills/neilization/scripts/validate.mjs"
