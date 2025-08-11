import os
import time

# Frames to animate "Z" growing
zzz_frames = ["Z", "Zz", "zZz", "zzZz", "zZzzZ"]

# Fixed cat body lines
cat_body = [
r"            |\      _,,,--,,_ ",
r"            /,`.-'`'   ._  \-;;,_",
r"           |,4-  ) )_   .;.(  `'-'",
r"          '---''(_/._)-'(_\_)"
]

def clear_screen():
    # Clear terminal screen, works on Windows/Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_sleeping_cat_terminal(repeat=5, delay=0.5):
    for _ in range(repeat):
        for i, zzz in enumerate(zzz_frames):
            clear_screen()
            print(zzz)               # Print the animated "Zzz"
            for line in cat_body:    # Print static cat body
                print(line)
            time.sleep(delay)

if __name__ == "__main__":
    animate_sleeping_cat_terminal()
