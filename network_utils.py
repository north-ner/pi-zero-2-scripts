import os
import re
import subprocess

TO_WIFI_SCRIPT = "./to_wifi.sh"
TO_HOTSPOT_SCRIPT = "./to_hotspot.sh"

def get_wifi_signal():
    try:
        iwconfig_out = os.popen("iwconfig wlan0").read()
        match = re.search(r"Signal level=([-0-9]+) dBm", iwconfig_out)
        return int(match.group(1)) if match else None
    except:
        return None

def get_ip_address():
    try:
        ip = os.popen("hostname -I").read().strip()
        return ip if ip else "No IP"
    except:
        return "Error"

def is_wifi_connected():
    """Return True if wlan0 is connected to a Wi-Fi network."""
    ssid = os.popen("iwgetid -r").read().strip()
    return bool(ssid)

def is_hotspot_running():
    """Return True if hostapd service is active."""
    status = os.popen("systemctl is-active hostapd").read().strip()
    return status == "active"

def set_wifi_mode(enable=True):
    """Switch to Wi-Fi mode using the to_wifi script."""
    if enable:
        if is_wifi_connected():
            print("Already in Wi-Fi mode")
            return
        os.system(f"bash {TO_WIFI_SCRIPT}")
    else:
        set_hotspot_mode(True)

def set_hotspot_mode(enable=True):
    """Switch to hotspot mode using the to_hotspot script."""
    if enable:
        if is_hotspot_running():
            print("Already in Hotspot mode")
            return
        os.system(f"bash {TO_HOTSPOT_SCRIPT}")
    else:
        set_wifi_mode(True)
