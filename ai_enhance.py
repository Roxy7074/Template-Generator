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
        
    def generate_bg(self, theme, output_path, size="1024x1024"):
        prompt = f"""
        I want to create a high-quality background image for my Blockchain Club event poster.
        Please follow the instructions below on how I need you to do this.
        
        THEME: {theme}
        
        FOLLOW THESE STYLE REQUIREMENTS:
        - Dark color scheme with deep reds, blacks, and crimson tones
        - You may add in a abstract technology aesthetic with lines or waves
        - Include Geometric shapes in the image like: hexagons, nodes, connection lines, circuits
        - Also, for the texts or shapes, add glowing neon red accents and highlights
        - For the overall atmosphere of the post, make it have a 
          digital, futuristic, and cyberpunk-inspired vibe
        - Add in gradient effects
        - Keep the design professional and modern, but make it visually attractive
        
        TECHNICAL SPECS:
        - For the base background, make it a pure background only - NO text, logos, or characters
        - Make the background suitable for overlaying white text
        - Keep it darker in the center and more vibrant at the edges
        - Make some of the areas high in contrast for text placement
        - Add in the geometric shapes and blocks in the corners of the image
        
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
        Add 3D Block Shapes in the image, specifically the edges or corners to support the club theme, 
        again keep them shades of red.
        """
        img = Image.open(input_path).convert('RGBA')
        width, height = img.size

        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # crimson, dark red, red, firebrick, orange red
        colors = [(220, 20, 60, 180), (139, 0, 0, 160),
                  (255, 0, 0, 140), (178, 34, 34, 170),
                  (255, 69, 0, 150),]
        
        num_blocks = random.randint(3, 6)

        for _ in range(num_blocks):
            color = random.choice(colors)
            
            # select a random corner 
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
            else: 
                x, y = random.randint(width - 250, width - 80), random.randint(height - 250, height - 80)
            
            # either draw filled rect or outlined square
            if random.random() > 0.5:
                draw.rectangle([x, y, x + block_w, y + block_h], fill=color)
            else:
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
        Generate an advanced gradient for the background.
        """

        img = Image.new('RGB', (1024, 1024))
        draw = ImageDraw.Draw(img)
    
        for y in range(1024):
            progress = y / 1024
            r = int(139 - (139 * progress * 0.7))
            g = int(0)
            b = int(0)
            
            draw.line([(0, y), (1024, y)], fill=(r, g, b))
        
        # adding gradient overlay
        overlay = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        
        center_x, center_y = 540, 540
        max_radius = 750
        
        for radius in range(max_radius, 0, -5):
            alpha = int(50 * (1 - radius / max_radius))
            color = (220, 20, 60, alpha) 
            draw_overlay.ellipse([center_x - radius, center_y - radius,
                                 center_x + radius, center_y + radius],
                                fill=color)
    
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        
        # add geometric blocks
        draw_final = ImageDraw.Draw(img)
        
        # corner decor
        colors = [
            (220, 20, 60, 180),
            (139, 0, 0, 160),
            (255, 0, 0, 140),
        ]
        
        # top right corner
        for i in range(3):
            color = random.choice(colors)
            size = random.randint(60, 150)
            x = random.randint(880, 1020)
            y = random.randint(0, 200)
            draw_final.rectangle([x, y, x + size, y + size], 
                                fill=color, outline=(255, 255, 255, 100), width=2)
        
        # bottom left corner
        for i in range(3):
            color = random.choice(colors)
            size = random.randint(60, 150)
            x = random.randint(0, 200)
            y = random.randint(880, 1020)
            draw_final.rectangle([x, y, x + size, y + size], 
                                fill=color, outline=(255, 255, 255, 100), width=2)
            
        # bottom right corner
        for i in range(3):
            color = random.choice(colors)
            size = random.randint(60, 150)
            x = random.randint(880, 1020)
            y = random.randint(880, 1020)
            draw_final.rectangle([x, y, x + size, y + size],
                                 fill=color, outline=(225, 255, 255, 100), width=2)
        
        # add grid pattern
        for x in range(0, 1024, 40):
            draw_final.line([(x, 0), (x, 1080)], fill=(255, 255, 255, 15), width=1)
        for y in range(0, 1024, 40):
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

                        


