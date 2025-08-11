# resource_utils.py
import os
import psutil
import subprocess

def get_cpu_temp():
    """Return CPU temperature in °C or None if unavailable."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return float(f.read()) / 1000
    except:
        return None

def get_cpu_load():
    """Return CPU usage percentage over 1 second."""
    try:
        return psutil.cpu_percent(interval=1)
    except:
        return None

def get_cpu_freq():
    """Return current CPU frequency in MHz."""
    try:
        freq = psutil.cpu_freq()
        return freq.current if freq else None
    except:
        return None

def get_ram_usage():
    """Return RAM usage percentage."""
    mem = psutil.virtual_memory()
    return mem.percent

def get_drive_usage():
    """Return disk usage percentage for root filesystem."""
    usage = psutil.disk_usage('/')
    return usage.percent

def get_free_space():
    """Return free space in GB."""
    usage = psutil.disk_usage('/')
    return round(usage.free / (1024 ** 3), 1)

def get_uptime():
    """Return human-readable uptime."""
    try:
        return os.popen("uptime -p").read().strip()
    except:
        return None
