#!/bin/bash
set -euo pipefail
ARCH=${1:-amd64}
DISTRO=${2:-bookworm}
WORK_DIR="work-${ARCH}"
ROOT_FS="$WORK_DIR/rootfs"
ISO_DIR="iso"
ISO_NAME="xxos-${ARCH}.iso"

echo "[*] Building XXOS ISO for: $ARCH (distro: $DISTRO)"
mkdir -p "$ROOT_FS" "$ISO_DIR"
sudo debootstrap --arch="$ARCH" "$DISTRO" "$ROOT_FS" http://deb.debian.org/debian

# install minimal packages inside chroot
sudo chroot "$ROOT_FS" /bin/bash -c "apt-get update && apt-get install -y --no-install-recommends linux-image-amd64 live-boot live-config systemd-sysv ca-certificates grub-pc"

# persistence config
mkdir -p "$ROOT_FS/live"
echo "/ union" > "$ROOT_FS/live/persistence.conf"

# simple grub config for booting
mkdir -p "$ROOT_FS/boot/grub"
cat > "$ROOT_FS/boot/grub/grub.cfg" <<'EOF'
set default=0
set timeout=5
menuentry "XXOS (Persistent)" {
    linux /boot/vmlinuz boot=live persistence persistence-label=XXOS-PERSISTENCE quiet
    initrd /boot/initrd.img
}
menuentry "XXOS (Non-Persistent)" {
    linux /boot/vmlinuz boot=live quiet
    initrd /boot/initrd.img
}
EOF

# build iso (use grub-mkrescue)
sudo grub-mkrescue -o "$ISO_DIR/$ISO_NAME" "$ROOT_FS"
echo "[+] ISO created: $ISO_DIR/$ISO_NAME"
