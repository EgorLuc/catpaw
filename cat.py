import tkinter as tk
from PIL import Image, ImageTk
from pynput import mouse
import time
import ctypes

PAW_IMAGE_PATH = 'cat.png'
PAW_WIDTH = 20
PAW_HEIGHT = 20
FADE_DURATION_MS = 2000

root = tk.Tk()
root.withdraw()

TRANSPARENT_COLOR = '#ff00ff'

def get_scale_factor():
    try:
        user32 = ctypes.windll.user32
        dc = user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)
        return dpi / 120
    except:
        return 1.0

scale_factor = get_scale_factor()

class PawPopup(tk.Toplevel):
    def __init__(self, master, image_path, cursor_x, cursor_y):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.config(bg=TRANSPARENT_COLOR)
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

        image = Image.open(image_path).convert("RGBA").resize(
            (PAW_WIDTH, PAW_HEIGHT), Image.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(image)

        label = tk.Label(self, image=self.photo, borderwidth=0, bg=TRANSPARENT_COLOR)
        label.pack()

        pos_x = (cursor_x - PAW_WIDTH // 2) * scale_factor
        pos_y = (cursor_y - PAW_HEIGHT // 2) * scale_factor

        self.geometry(f'{int(PAW_WIDTH * scale_factor)}x{int(PAW_HEIGHT * scale_factor)}+{int(pos_x)}+{int(pos_y)}')

        self.start_time = time.time()
        self.fade()

    def fade(self):
        elapsed_ms = (time.time() - self.start_time) * 1000
        if elapsed_ms >= FADE_DURATION_MS:
            self.destroy()
        else:
            alpha = 1 - (elapsed_ms / FADE_DURATION_MS)
            self.attributes('-alpha', alpha)
            self.after(50, self.fade)

def create_paw(cursor_x, cursor_y):
    PawPopup(root, PAW_IMAGE_PATH, cursor_x, cursor_y)

def on_click(x, y, button, pressed):
    if pressed:
        root.after(0, create_paw, x, y)

with mouse.Listener(on_click=on_click) as listener:
    print("Кликните мышью, чтобы оставить лапку.")
    root.mainloop()