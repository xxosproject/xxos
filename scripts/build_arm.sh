#!/bin/bash
set -euo pipefail
ARCH=${1:-arm64}
IMAGE_NAME="xxos-${ARCH}.img"
WORK_DIR="arm-work-${ARCH}"
ROOT_FS="$WORK_DIR/rootfs"

echo "[*] Building ARM image (this is a helper, requires qemu-user-static)"
mkdir -p "$ROOT_FS"
sudo debootstrap --arch="$ARCH" bookworm "$ROOT_FS" http://deb.debian.org/debian
sudo cp /usr/bin/qemu-aarch64-static "$ROOT_FS/usr/bin/"
sudo chroot "$ROOT_FS" /bin/bash -c "apt-get update && apt-get install -y --no-install-recommends linux-image-arm64 cloud-init cloud-guest-utils"
# create image with dd & format (placeholder)
fallocate -l 2G "$IMAGE_NAME"
mkfs.ext4 "$IMAGE_NAME"
echo "[+] ARM image prepared: $IMAGE_NAME (mount and copy rootfs manually)"
