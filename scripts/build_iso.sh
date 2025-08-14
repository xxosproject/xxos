#!/usr/bin/env bash
set -euo pipefail
ARCH=${ARCH:-amd64}
DIST=${DIST:-bookworm}
ISO_NAME=${ISO_NAME:-xxos-${ARCH}-beta.iso}
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LB_DIR="$REPO_ROOT/livebuild"

echo "[*] Building XXOS ISO (BETA) arch=$ARCH dist=$DIST"
cd "$LB_DIR"
sudo lb clean || true

sudo lb config --architecture "$ARCH" --distribution "$DIST" --binary-images iso-hybrid   --iso-application "XXOS (BETA)" --iso-volume "XXOS Live (BETA)" --debian-installer live   --bootappend-live "boot=live components quiet splash persistence persistence-label=XXOS-PERSISTENCE"

sudo lb build

cd "$REPO_ROOT"
mkdir -p iso
mv -f "$LB_DIR"/*.iso "iso/$ISO_NAME" || true
echo "[+] Built iso: iso/$ISO_NAME"
