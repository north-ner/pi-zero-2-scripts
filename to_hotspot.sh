#!/bin/bash
set -e

echo "Switching to Hotspot mode..."

# Unmask and enable hostapd and dnsmasq
sudo systemctl unmask hostapd dnsmasq || true
sudo systemctl enable hostapd dnsmasq

# Stop any DHCP client on wlan0 to avoid conflicts
sudo dhclient -r wlan0 || true

# Replace /etc/network/interfaces to static IP for hotspot
sudo tee /etc/network/interfaces > /dev/null <<EOF
# minimal /etc/network/interfaces for Hotspot mode + DietPi
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

iface eth0 inet dhcp

auto wlan0
iface wlan0 inet static
    address 192.168.4.1
    netmask 255.255.255.0
EOF

# Restart networking
sudo systemctl restart networking

# Start hotspot services
sudo systemctl start hostapd dnsmasq

echo "Hotspot mode activated."
echo "SSID: MyPiHotspot"
echo "Password: mypassword123"
