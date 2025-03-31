from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import os
import io
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for Cloudflare Pages
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Google Fonts API key (you'll need to set this in .env)
GOOGLE_FONTS_API_KEY = os.getenv('GOOGLE_FONTS_API_KEY', '')

def get_google_fonts():
    """Fetch available Google Fonts"""
    url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={GOOGLE_FONTS_API_KEY}"
    try:
        response = requests.get(url)
        fonts = response.json()
        return [(font['family'], font['files']['regular']) for font in fonts['items']]
    except:
        # Return some default fonts if API call fails
        return [
            ('Roboto', 'https://fonts.googleapis.com/css2?family=Roboto&display=swap'),
            ('Open Sans', 'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap'),
            ('Lato', 'https://fonts.googleapis.com/css2?family=Lato&display=swap'),
            ('Jacquard 12', 'https://fonts.googleapis.com/css2?family=Jacquard+12&display=swap'),
            ('Nabla', 'https://fonts.googleapis.com/css2?family=Nabla&display=swap' ),
            ('Sarina', 'https://fonts.googleapis.com/css2?family=Sarina&display=swap' )
        ]

def download_font(font_url):
    """Download and verify font file"""
    try:
        # If it's a Google Fonts CSS URL, extract the actual font URL
        if 'fonts.googleapis.com/css2' in font_url:
            css_response = requests.get(font_url)
            css_text = css_response.text
            # Extract the actual font URL from the CSS
            import re
            font_url_match = re.search(r'src: url\((.*?)\)', css_text)
            if font_url_match:
                font_url = font_url_match.group(1)

        font_response = requests.get(font_url, headers={'User-Agent': 'Mozilla/5.0'})
        if font_response.status_code != 200:
            raise Exception("Failed to download font")
        
        # Write font to temporary file
        font_path = "temp_font.ttf"
        with open(font_path, "wb") as f:
            f.write(font_response.content)
        
        # Verify the font can be loaded
        try:
            ImageFont.truetype(font_path, 72)
            return font_path
        except Exception as e:
            os.remove(font_path)
            raise Exception(f"Invalid font file: {str(e)}")
            
    except Exception as e:
        raise Exception(f"Font download failed: {str(e)}")

def create_glitter_text(text, font_url, glitter_effect):
    """Create glitter text GIF"""
    try:
        # Download and verify font
        font_path = download_font(font_url)
        
        # Create base image with text
        font_size = 72
        font = ImageFont.truetype(font_path, font_size)
        
        # Get text size
        dummy_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        text_bbox = dummy_draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Create image with padding
        padding = 40
        img_width = text_width + padding * 2
        img_height = text_height + padding * 2
        
        # Load glitter effect
        glitter_path = f'static/gifs/{glitter_effect}.gif'
        if not os.path.exists(glitter_path):
            raise Exception(f"Glitter effect not found: {glitter_effect}")
        
        glitter_gif = Image.open(glitter_path)
        
        # Create frames for the animation
        frames = []
        
        # For each frame in the glitter GIF
        for glitter_frame in ImageSequence.Iterator(glitter_gif):
            # Convert frame to RGBA
            glitter_frame = glitter_frame.convert('RGBA')
            
            # Create a transparent base frame
            frame = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
            
            # Calculate text position
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
            
            # Create a mask for the text
            text_mask = Image.new('L', (img_width, img_height), 0)
            mask_draw = ImageDraw.Draw(text_mask)
            mask_draw.text((x, y), text, font=font, fill=255)
            
            # Create a frame-sized glitter pattern
            pattern = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
            for i in range(0, img_width, glitter_frame.width):
                for j in range(0, img_height, glitter_frame.height):
                    pattern.paste(glitter_frame, (i, j))
            
            # Apply the text mask to the glitter pattern
            pattern.putalpha(text_mask)
            frames.append(pattern)
        
        # Clean up temporary font file
        os.remove(font_path)
        
        # Save as animated GIF
        gif_buffer = io.BytesIO()
        
        # Save with transparency
        frames[0].save(
            gif_buffer,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
            disposal=2
        )
        gif_buffer.seek(0)
        
        return gif_buffer
    except Exception as e:
        # Clean up temporary font file if it exists
        if 'font_path' in locals() and os.path.exists(font_path):
            os.remove(font_path)
        raise e

@app.route('/')
def index():
    fonts = get_google_fonts()
    glitter_effects = [f"glitter{i}" for i in range(1, 9)]
    return render_template('index.html', fonts=fonts, glitter_effects=glitter_effects)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text', 'Glitter')
    font_url = request.form.get('font')
    glitter_effect = request.form.get('effect', 'glitter1')
    
    try:
        gif_buffer = create_glitter_text(text, font_url, glitter_effect)
        return send_file(
            gif_buffer,
            mimetype='image/gif',
            as_attachment=True,
            download_name=f'glitter_text_{datetime.now().strftime("%Y%m%d_%H%M%S")}.gif'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use PORT environment variable if available (for Cloudflare)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
