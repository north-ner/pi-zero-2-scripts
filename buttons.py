# buttons.py
import RPi.GPIO as GPIO
import config

def setup_buttons():
    GPIO.setmode(GPIO.BCM)
    for pin in [config.BUTTON_LEFT, config.BUTTON_MIDDLE, config.BUTTON_RIGHT,
                config.BUTTON_DOWN, config.BUTTON_UP, config.BUTTON_SCREEN]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_button(pin):
    return GPIO.input(pin) == GPIO.LOW  # True if pressed

def cleanup():
    GPIO.cleanup()