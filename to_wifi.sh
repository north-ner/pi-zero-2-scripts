#!/bin/bash
set -e

echo "Switching to Wi-Fi client mode..."

# Stop hotspot services if running
sudo systemctl stop hostapd dnsmasq || true
sudo systemctl disable hostapd dnsmasq || true
sudo systemctl mask hostapd dnsmasq || true

# Restore /etc/network/interfaces for Wi-Fi client
sudo tee /etc/network/interfaces > /dev/null <<EOF
# minimal /etc/network/interfaces for Wi-Fi client + DietPi
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

allow-hotplug eth0
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
EOF

# Unmask networking if masked
sudo systemctl unmask networking || true

# Restart networking and wpa_supplicant
sudo systemctl restart networking
sudo systemctl restart wpa_supplicant || sudo systemctl start wpa_supplicant

# Obtain IP address on wlan0
sudo dhclient -v wlan0 || true

echo "Wi-Fi client mode activated."
