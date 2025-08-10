#screens.py
import time
from PIL import Image, ImageDraw, ImageFont
import config, resource_utils, network_utils, qr_utils

font = ImageFont.load_default()
loading_frames = ['-', '\\', '|', '/']  # Spinner frames for loading animation

def draw_loading_screen(device, message="Loading..."):
    # Show loading spinner animation with message
    for frame in loading_frames:
        image = Image.new("1", (device.width, device.height))
        draw = ImageDraw.Draw(image)
        draw.text((0, 20), f"{message} {frame}", font=font, fill=255)
        device.display(image)
        time.sleep(0.1)

def draw_status_screen(device):
    # Draw main status screen with CPU temp, WiFi signal, battery (placeholder)
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "Status", font=font, fill=255)

    cpu_temp = resource_utils.get_cpu_temp()
    cpu_temp_str = f"{cpu_temp:.1f} C" if cpu_temp is not None else "N/A"
    draw.text((0, 12), f"CPU Temp: {cpu_temp_str}", font=font, fill=255)

    wifi_signal = network_utils.get_wifi_signal()
    wifi_str = f"{wifi_signal} dBm" if wifi_signal is not None else "N/A"
    draw.text((0, 24), f"WiFi Signal: {wifi_str}", font=font, fill=255)

    # Placeholder battery percentage
    draw.text((0, 36), "Battery: 100%", font=font, fill=255)

    device.display(image)

def draw_resource_screen(device):
    # Draw resource usage screen (CPU temp, RAM, Disk)
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "Resources", font=font, fill=255)

    cpu_temp = resource_utils.get_cpu_temp()
    cpu_temp_str = f"{cpu_temp:.1f} C" if cpu_temp is not None else "N/A"
    draw.text((0, 12), f"CPU Temp: {cpu_temp_str}", font=font, fill=255)

    ram_usage = resource_utils.get_ram_usage()
    draw.text((0, 24), f"RAM Usage: {ram_usage}%", font=font, fill=255)

    drive_usage = resource_utils.get_drive_usage()
    draw.text((0, 36), f"Disk Usage: {drive_usage}%", font=font, fill=255)

    device.display(image)

def draw_menu_screen(device, selected, scroll_offset=0):
    # Draw menu with selectable items and smooth scrolling highlight
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "Menu", font=font, fill=255)

    max_visible = 4  # Number of menu items visible at once

    # Calculate slice of menu items to display based on scroll offset
    menu_slice = config.MENU_ITEMS[scroll_offset:scroll_offset + max_visible]

    for i, item in enumerate(menu_slice):
        y = 12 + i * 12
        is_selected = (i + scroll_offset) == selected

        if is_selected:
            # Draw highlight rectangle and inverted text for selection
            draw.rectangle((0, y - 1, device.width, y + 11), fill=255)
            draw.text((2, y), item, font=font, fill=0)
        else:
            draw.text((2, y), item, font=font, fill=255)

    device.display(image)

def draw_qr_screen(device):
    # Generate and display hotspot QR code on OLED
    qr_img = qr_utils.generate_hotspot_qr(config.HOTSPOT_SSID, config.HOTSPOT_PASS)
    # Resize QR to fit OLED dimensions if needed
    qr_img = qr_img.resize((device.width, device.height))
    device.display(qr_img)
