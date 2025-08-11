import time
from luma.core.render import canvas

def toggle_oled_screen(device, oled_on):
    # ASCII art animation frames
    frames_off = [
        "(=^.^=)",
        "(=^.^ )",
        "(= ^.^)",
        "(=^.^=)"
    ]  # Cat animation for See You Soon!

    frames_on = [
        "\\_/\\",
        "(o.o)",
        "> ^ <",
        "\\_/\\"
    ]  # Dog animation for Welcome

    def animate_message(message, frames, repeat=3, delay=0.3):
        for _ in range(repeat):
            for frame in frames:
                with canvas(device) as draw:
                    draw.text((2, 2), message, fill=255)
                    draw.text((2, 20), frame, fill=255)
                time.sleep(delay)

    if oled_on:
        # Show goodbye animation, then turn off display
        animate_message("See You Soon!", frames_off)
        device.hide()
        return False
    else:
        device.show()
        animate_message("Welcome!", frames_on)
        return True

def animate_sleeping_cat_oled(device, repeat=5, delay=0.5):
    # Frames to animate "Z" growing with varying capitalization for visual effect
    zzz_frames = ["Z", "Zz", "zZz", "zzZz", "zZzzZ"]

    # Fixed cat body lines
    cat_body = [
        r"           |\      _,,,--,,_ ",
        r"           /,`.-'`'   ._  \-;;,_",
        r"           |,4-  ) )_   .;.(  `'-'",
        r"          '---''(_/._)-'(_\_)"
    ]
    for _ in range(repeat):
        for i, zzz in enumerate(zzz_frames):
            with canvas(device) as draw:
                draw.text((0, 0), zzz, fill=255)  # Animated Zzz line at top
                # Draw cat body lines starting slightly lower on display
                for idx, line in enumerate(cat_body):
                    draw.text((0, 10 + idx * 10), line, fill=255)
            time.sleep(delay)