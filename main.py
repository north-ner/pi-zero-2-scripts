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
                screens.draw_status_screen(device)
            elif current_screen == 1:
                screens.draw_menu_screen(device, menu_index, scroll_offset)
            elif current_screen == 2:
                screens.draw_resource_screen(device)

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
                    screens.draw_loading_screen(device, "Shutting down")
                    time.sleep(1)
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
                        screens.draw_loading_screen(device, "Already in Hotspot mode")
                    else:
                        screens.draw_loading_screen(device, "Switching to Hotspot")
                        network_utils.set_hotspot_mode(True)
                        hotspot_active = True
                        screens.draw_qr_screen(device)
                        time.sleep(5)

                elif selected == "Show IP Address":
                    ip = network_utils.get_ip_address()
                    from PIL import Image, ImageDraw, ImageFont
                    img = Image.new("1", (device.width, device.height))
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()
                    draw.text((0, 20), f"IP: {ip}", font=font, fill=255)
                    device.display(img)
                    time.sleep(3)

        if buttons.read_button(config.BUTTON_SCREEN):
            from luma.core.render import canvas
            if oled_on:
                device.hide()
            else:
                device.show()
            oled_on = not oled_on
            time.sleep(0.2)

        time.sleep(0.05)

except KeyboardInterrupt:
    buttons.cleanup()
