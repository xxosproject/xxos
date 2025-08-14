#!/usr/bin/env bash
set -euo pipefail
echo "==> XXOS setup_env (Ubuntu 24.10)"
sudo apt-get update
sudo apt-get install -y --no-install-recommends git curl wget rsync build-essential jq python3 python3-pip python3-venv
sudo apt-get install -y --no-install-recommends live-build debootstrap squashfs-tools xorriso syslinux isolinux grub-pc-bin grub-efi-amd64-bin ca-certificates
sudo apt-get install -y --no-install-recommends nginx nftables python3-gi gir1.2-gtk-3.0
# Optional docker
if ! command -v docker >/dev/null 2>&1; then
  echo "Installing Docker (recommended)"
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker $USER || true
fi
mkdir -p iso build livebuild installer agent branding docs
echo "Setup complete."
