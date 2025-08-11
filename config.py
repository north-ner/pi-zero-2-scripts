# config.py

# GPIO configuration
BUTTON_LEFT = 26
BUTTON_MIDDLE = 27
BUTTON_RIGHT = 22
BUTTON_DOWN = 5
BUTTON_UP = 6
BUTTON_SCREEN = 23

# OLED I2C config
I2C_PORT = 1
OLED_ADDRESS = 0x3C

# Hotspot/WiFi credentials (for QR code)
HOTSPOT_SSID = "MyPiHotspot"
HOTSPOT_PASS = "7249980833"

# Menu items
MENU_ITEMS = [
    "WiFi Mode",
    "Hotspot Mode",
    "Show IP Address",
    "Shutdown"
]