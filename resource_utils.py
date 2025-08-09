# resource_utils.py
import os, psutil

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return float(f.read()) / 1000
    except:
        return None

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def get_drive_usage():
    usage = psutil.disk_usage('/')
    return usage.percent