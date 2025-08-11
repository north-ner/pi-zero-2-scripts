#main.py
import time
import config, buttons, screens
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import network_utils


serial = i2c(port=config.I2C_PORT, address=config.OLED_ADDRESS)
device = ssd1306(serial)

buttons.setup_buttons()
oled_on = True
current_screen = 0  # 0=Status, 1=Menu, 2=Resource
menu_index = 0
scroll_offset = 0
max_visible_menu_items = 4

#hotspot_active = False  # Track current mode
# Detect current mode at startup
if network_utils.is_hotspot_running():
    hotspot_active = True
elif network_utils.is_wifi_connected():
    hotspot_active = False
else:
    hotspot_active = False  # Default to Wi-Fi if no mode is active

print(f"Startup mode: {'Hotspot' if hotspot_active else 'Wi-Fi'}")

def update_scroll():
    global scroll_offset
    if menu_index < scroll_offset:
        scroll_offset = menu_index
    elif menu_index >= scroll_offset + max_visible_menu_items:
        scroll_offset = menu_index - max_visible_menu_items + 1

try:
    while True:
        if oled_on:
            if current_screen == 0:
                screens.draw_status_screen(device, hotspot_active)
            elif current_screen == 1:
                screens.draw_menu_screen(device, menu_index, scroll_offset)
            elif current_screen == 2:
                screens.draw_resource_screen(device, hotspot_active)

        # Button handling for screen cycle
        if buttons.read_button(config.BUTTON_LEFT):
            current_screen = (current_screen - 1) % 3
            time.sleep(0.2)
        if buttons.read_button(config.BUTTON_RIGHT):
            current_screen = (current_screen + 1) % 3
            time.sleep(0.2)

        if current_screen == 1:  # Menu navigation
            if buttons.read_button(config.BUTTON_DOWN):
                menu_index = (menu_index + 1) % len(config.MENU_ITEMS)
                update_scroll()
                time.sleep(0.2)
            if buttons.read_button(config.BUTTON_UP):
                menu_index = (menu_index - 1) % len(config.MENU_ITEMS)
                update_scroll()
                time.sleep(0.2)
            if buttons.read_button(config.BUTTON_MIDDLE):
                selected = config.MENU_ITEMS[menu_index]
                if selected == "Shutdown":
                    from animation import animate_sleeping_cat_oled
                    animate_sleeping_cat_oled(device, repeat=5, delay=0.6)
                    device.clear() 
                    device.hide() 
                    time.sleep(0.5) 
                    import os
                    os.system("sudo shutdown now")
                elif selected == "WiFi Mode":
                    if not hotspot_active:
                        screens.draw_loading_screen(device, "Device Already in WiFi Mode")
                    else:
                        screens.draw_loading_screen(device, "Switching to Wi-Fi")

                        network_utils.set_wifi_mode(True)
                        hotspot_active = False
                        time.sleep(1)

                elif selected == "Hotspot Mode":
                    if hotspot_active:
                        screens.draw_qr_screen(device)
                    else:
                        screens.draw_loading_screen(device, "Switching to Hotspot")
                        network_utils.set_hotspot_mode(True)
                        hotspot_active = True
                        screens.draw_qr_screen(device)
                        time.sleep(10)

                elif selected == "Show IP Address":
                    ip = network_utils.get_ip_address()
                    from PIL import Image, ImageDraw, ImageFont
                    img = Image.new("1", (device.width, device.height))
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()
                    draw.text((0, 20), f"IP: {ip}", font=font, fill=255)
                    device.display(img)
                    time.sleep(5)
        if buttons.read_button(config.BUTTON_SCREEN):
            from animation import toggle_oled_screen
            oled_on = toggle_oled_screen(device, oled_on)
            time.sleep(0.2)

        time.sleep(0.05)

except KeyboardInterrupt:
    buttons.cleanup()
