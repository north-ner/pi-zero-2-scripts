# qr_utils.py
import qrcode
from PIL import Image

def generate_hotspot_qr(ssid, password):
    qr_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(qr_data)
    qr.make()
    img = qr.make_image(fill_color="white", back_color="black").convert("1")
    return img