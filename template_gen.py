import cairo
import subprocess
import os
import sys

class Template:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.cr = cairo.Context(self.surface)

class Color:
    def __init__ (self, r, g, b):
        self.r = r
        self.g = g
        self.b = b 
    
def hex_to_rgb(hx):
    if hx.startswith('#'):
        hx = hx[1:]
        value = int(hx, 16)
        return Color(((value >> 16) & 0xFF) / 255.0, ((value >> 8) & 0xFF) / 255.0,
                     (value & 0xFF) / 255.0)

def create_temp(width, height):
    try: 
        return Template(width, height) 
    except Exception as e:
        print("Error creating template: {e}", file=sys.stderr)
        return None
    
def set_bg(tg, hxcol):
    color = hex_to_rgb(hxcol)
    tg.cr.set_source_rgb(color.r, color.g, color.b)
    tg.cr.paint()

def set_gradient(tg, c1, c2, vertical=True):
    one = hex_to_rgb(c1)
    two = hex_to_rgb(c2)
    if vertical:
        pat = cairo.LinearGradient(0, 0, 0, tg.height)
    else:
        pat = cairo.LinearGradient(0, 0, tg.width, 0)
    pat.add_color_stop_rgb(0, one.r, one.g, one.b)
    pat.add_color_stop_rgb(1, two.r, two.g, two.b)
    tg.cr.set_source(pat)
    tg.cr.paint()

def add_text(tg, text, x, y):
    tg.cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    tg.cr.set_font_size(30.0)
    tg.cr.set_source_rgb(1.0, 1.0, 1.0)
    tg.cr.move_to(x, y)
    tg.cr.show_text(text)

def add_logo(tg, image_path, x, y, width, height):
    try:
        image = cairo.ImageSurface.create_from_png(image_path)
        if image.get_width() == 0 or image.get_height() == 0:
            print(f"Error loading image: {image_path}")
            return
        scale_x = width / image.get_width()
        scale_y = height / image.get_height()
        tg.cr.save()
        tg.cr.translate(x, y)
        tg.cr.scale(scale_x, scale_y)
        tg.cr.set_source_surface(image, 0, 0)
        tg.cr.paint()
        tg.cr.restore()
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")

def add_rectangle(tg, x, y, width, height, fill_color=None, outline_color=None, outline_width=1):
    if fill_color:
        fill = hex_to_rgb(fill_color)
        tg.cr.set_source_rgb(fill.r, fill.g, fill.b)
        tg.cr.rectangle(x, y, width, height)
        tg.cr.fill()
    if outline_color:
        outline = hex_to_rgb(outline_color)
        tg.cr.set_source_rgb(outline.r, outline.g, outline.b)
        tg.cr.set_line_width(outline_width)
        tg.cr.rectangle(x, y, width, height)
        tg.cr.stroke()

def save_template(tg, filename):
    os.makedirs("output", exist_ok=True)
    try:
        tg.surface.write_to_png(filename)
        print(f"Saved image to {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}", file=sys.stderr)

def generate_ai_bg(theme, output_path):
    os.makedirs("output", exist_ok=True)
    cmd = ["python3", "ai_enhance.py", theme, output_path]
    print("Generating AI background...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: AI background generation failed (code {result.returncode}). Continuing without it.")
            print(f"Stderr: {result.stderr}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"Error running AI script: {e}", file=sys.stderr)
        return False

def main():
    print("Generating template...")

    if not generate_ai_bg("Blockchain Research Event", "output/bg_temp.png"):
        print("Using default background (AI failed).")

    tg = create_temp(1024, 1024)
    if tg is None:
        print("Failed to create template. Exiting.", file=sys.stderr)
        return 1

    add_logo(tg, "output/bg_temp.png", 0, 0, 1024, 1024)

    tg.cr.set_source_rgba(0, 0, 0, 0.4)
    tg.cr.paint()

    add_logo(tg, "Logo Design.png", 30, 30, 130, 130)

    tg.cr.set_font_size(30.0)
    add_text(tg, "Northeastern Blockchain", 170, 100)

    tg.cr.set_font_size(70.0)
    add_text(tg, "Speaker Event", 100, 300)

    save_template(tg, "output_template.png")
    print("Template generation is complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())