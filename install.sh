#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.openclaw/skills/supoclip-zernio-approval"
mkdir -p "$DEST"
cp -R "$ROOT/skills/supoclip-zernio-approval/"* "$DEST/"
echo "Installed OpenClaw skill to $DEST"
echo "Check zernio auth with: zernio auth:check"
