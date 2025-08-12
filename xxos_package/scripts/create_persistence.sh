#!/bin/bash
set -euo pipefail
DEVICE=${1:-/dev/sdX1}
LABEL=${2:-XXOS-PERSISTENCE}
echo "[*] Creating persistence filesystem on $DEVICE with label $LABEL"
sudo mkfs.ext4 -L "$LABEL" "$DEVICE"
echo "[+] Persistence partition created. Mount it at /mnt and create /live/persistence.conf with '/ union'"
