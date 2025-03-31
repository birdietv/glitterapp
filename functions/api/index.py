from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import io
import os
import requests
from datetime import datetime

app = Flask(__name__)

def create_glitter_text(text, font_url, glitter_effect):
    try:
        # Download and use the selected font
        font_response = requests.get(font_url)
        font_path = "/tmp/temp_font.ttf"
        with open(font_path, "wb") as f:
            f.write(font_response.content)
        
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
        glitter_path = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'gifs', f'{glitter_effect}.gif')
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

@app.route('/api/generate', methods=['POST'])
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
        return {'error': str(e)}, 500 