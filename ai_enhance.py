import os
import sys
import random
import requests
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFilter

load_dotenv()

class AIEnhancer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv(
            "OPENAI_API_KEY"))
        
    def generate_bg(self, theme, output_path, size="1080x1080"):
        prompt = f"""
        Create a stunning, high-tech abstract background for a blockchain event poster.
        
        THEME: {theme}
        
        STYLE REQUIREMENTS:
        - Dark color scheme with deep reds, blacks, and crimson tones
        - Abstract tech aesthetic with blockchain network patterns
        - Geometric shapes: hexagons, nodes, connection lines, circuits
        - Glowing neon red accents and highlights
        - Digital, futuristic, cyberpunk-inspired atmosphere
        - Depth and layers with gradient effects
        - Professional and modern design
        
        TECHNICAL SPECS:
        - Pure background only - NO text, logos, or characters
        - Suitable for overlaying white text
        - Darker in center, more vibrant at edges
        - High contrast areas for text placement
        - Abstract geometric patterns in corners
        
        MOOD: Innovative, cutting-edge, professional, energetic, tech-forward
        """
        try:
            print(f"Generating the background for: {theme}")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd",
                n=1,
            )
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            temp_path = output_path + ".temp.png"
            with open(temp_path, 'wb') as f:
                f.write(img_response.content)

            self.add_graphics(temp_path, output_path)
            os.remove(temp_path)

            print(f"Background successfully made and saved to {output_path}")
            return True
        except Exception as e:
            print(f"Error generating background: {e}")
            return False
        
    def add_graphics(self, input_path, output_path):
        """ 
        Add random red geometric blocks and tech elements to corners or where there is free space
        """
        img = Image.open(input_path).convert('RGBA')
        width, height = img.size

        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # colors are crimson, dark red, red, firebrick, orange red
        colors = [(220, 20, 60, 180), (139, 0, 0, 160),
                  (255, 0, 0, 140), (178, 34, 34, 170),
                  (255, 69, 0, 150),]
        
        num_blocks = random.randint(3, 6)

        for _ in range(num_blocks):
            color = random.choice(colors)
            
            # random corner selection
            corner = random.choice(['top_left', 'top_right', 'bottom_left', 'bottom_right'])
            
            # block size
            block_w = random.randint(80, 200)
            block_h = random.randint(80, 200)
            
            if corner == 'top_left':
                x, y = random.randint(0, 150), random.randint(0, 150)
            elif corner == 'top_right':
                x, y = random.randint(width - 250, width - 80), random.randint(0, 150)
            elif corner == 'bottom_left':
                x, y = random.randint(0, 150), random.randint(height - 250, height - 80)
            else:  # bottom_right
                x, y = random.randint(width - 250, width - 80), random.randint(height - 250, height - 80)
            
            # draw geometric shape which is either a square/rectangle
            if random.random() > 0.5:
                # rect
                draw.rectangle([x, y, x + block_w, y + block_h], fill=color)
            else:
                # square
                draw.rectangle([x, y, x + block_w, y + block_h], 
                             outline=color, width=random.randint(3, 8))
        
        # scan lines for tech effect
        for i in range(0, height, 4):
            draw.line([(0, i), (width, i)], fill=(255, 255, 255, 5))
        
        # overlay onto original
        img = Image.alpha_composite(img, overlay)
        
        # change back to RGB and save
        rgb_img = Image.new('RGB', img.size, (0, 0, 0))
        rgb_img.paste(img, mask=img.split()[3])
        rgb_img.save(output_path)
    
    def generate_advanced_gradient(self, output_path):
        """
        Generate an advanced gradient with geometric tech elements
        """
        # make base image
        img = Image.new('RGB', (1080, 1080))
        draw = ImageDraw.Draw(img)
        
        # multi color gradient
        for y in range(1080):
            progress = y / 1080
            
            # dark red to black gradient
            r = int(139 - (139 * progress * 0.7))
            g = int(0)
            b = int(0)
            
            draw.line([(0, y), (1080, y)], fill=(r, g, b))
        
        # add radial gradient overlay
        overlay = Image.new('RGBA', (1080, 1080), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        
        center_x, center_y = 540, 540
        max_radius = 750
        
        for radius in range(max_radius, 0, -5):
            alpha = int(50 * (1 - radius / max_radius))
            color = (220, 20, 60, alpha) 
            draw_overlay.ellipse([center_x - radius, center_y - radius,
                                 center_x + radius, center_y + radius],
                                fill=color)
        
        # composite
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        
        # add geometric blocks
        draw_final = ImageDraw.Draw(img)
        
        # corner decorations
        colors = [
            (220, 20, 60, 180),
            (139, 0, 0, 160),
            (255, 0, 0, 140),
        ]
        
        # top left corner
        for i in range(3):
            color = random.choice(colors)
            size = random.randint(60, 150)
            x = random.randint(0, 200)
            y = random.randint(0, 200)
            draw_final.rectangle([x, y, x + size, y + size], 
                                fill=color, outline=(255, 255, 255, 100), width=2)
        
        # top right corner
        for i in range(3):
            color = random.choice(colors)
            size = random.randint(60, 150)
            x = random.randint(880, 1020)
            y = random.randint(0, 200)
            draw_final.rectangle([x, y, x + size, y + size], 
                                fill=color, outline=(255, 255, 255, 100), width=2)
        
        # bottom corners
        for i in range(3):
            color = random.choice(colors)
            size = random.randint(60, 150)
            x = random.randint(0, 200)
            y = random.randint(880, 1020)
            draw_final.rectangle([x, y, x + size, y + size], 
                                fill=color, outline=(255, 255, 255, 100), width=2)
        
        # add grid pattern
        for x in range(0, 1080, 40):
            draw_final.line([(x, 0), (x, 1080)], fill=(255, 255, 255, 15), width=1)
        for y in range(0, 1080, 40):
            draw_final.line([(0, y), (1080, y)], fill=(255, 255, 255, 15), width=1)
        
        # convert and save
        rgb_img = Image.new('RGB', img.size, (0, 0, 0))
        rgb_img.paste(img, mask=img.split()[3])
        rgb_img.save(output_path)
        
        print(f"✓ Advanced gradient with geometric elements saved to {output_path}")
        return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python ai_enhance.py <theme> <output_path> [--simple]")
        print("Example: python ai_enhance.py 'research event' output/bg.png")
        sys.exit(1)
    
    theme = sys.argv[1]
    output_path = sys.argv[2]
    use_simple = '--simple' in sys.argv

    generator = AIEnhancer()

    if use_simple or not os.getenv("OPENAI_API_KEY"):
        print("Using advanced gradient background with no AI...")
        generator.generate_advanced_gradient(output_path)
    else:
        success = generator.generate_bg(theme, output_path)
        if not success:
            print("Going back to advanced gradient...")
            generator.generate_advanced_gradient(output_path)

if __name__ == "__main__":
    main()

                        


