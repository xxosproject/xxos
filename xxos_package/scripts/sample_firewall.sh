#!/bin/bash
# Example nftables rules (simple starting point)
set -e
sudo nft flush ruleset || true
sudo nft add table inet xxosfw || true
sudo nft 'add chain inet xxosfw input { type filter hook input priority 0 ; policy drop; }'
sudo nft 'add chain inet xxosfw forward { type filter hook forward priority 0 ; policy drop; }'
sudo nft 'add chain inet xxosfw output { type filter hook output priority 0 ; policy accept; }'
# Allow established
sudo nft add rule inet xxosfw input ct state established,related accept
# Allow SSH from local network (change 192.168.1.0/24 as needed)
sudo nft add rule inet xxosfw input ip saddr 192.168.1.0/24 tcp dport 22 accept
echo "[+] Basic nftables firewall applied. Customize templates/firewall_rules.txt for production."
