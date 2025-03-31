# Glitter Text Generator

A web application that generates glittery text effects using custom fonts and glitter animations.

## Features

- Create text with glitter effects
- Choose from various Google Fonts
- Multiple glitter effect options
- Real-time preview
- Download generated images

## Setup

1. Clone this repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your Google Fonts API key:
   - Get an API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Create a `.env` file in the project root
   - Add your API key: `GOOGLE_FONTS_API_KEY=your_api_key_here`

## Running the Application

1. Activate your virtual environment if not already activated
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter the text you want to make glittery
2. Choose a font from the dropdown menu
3. Select a glitter effect
4. Click "Generate Glitter Text" to create your image
5. The generated image will appear below the form
6. Right-click and save the image, or it will automatically download

## Requirements

- Python 3.7+
- Flask
- Pillow (PIL)
- requests
- python-dotenv

## License

MIT License 