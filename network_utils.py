# network_utils.py
import os, re

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

def set_wifi_mode(enable=True):
    if enable:
        os.system("bash wifi_on.sh")
    else:
        os.system("bash wifi_off.sh")

def set_hotspot_mode(enable=True):
    if enable:
        os.system("bash hotspot_on.sh")
    else:
        os.system("bash hotspot_off.sh")