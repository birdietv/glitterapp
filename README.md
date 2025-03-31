# Glitter Text Generator ✨

A web application that generates glitter text GIFs using custom fonts and glitter effects.

## Features

- Create animated glitter text GIFs
- Choose from a variety of Google Fonts
- Multiple glitter effects to choose from
- Download generated GIFs
- Modern, dark-themed UI

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add glitter effect GIFs to the `static/gifs` directory. The GIFs should be named `glitter1.gif`, `glitter2.gif`, etc.

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter the text you want to convert to glitter
2. Choose a font from the dropdown menu
3. Select a glitter effect
4. Click "Generate Glitter Text"
5. Preview your generated GIF
6. Click the download button to save your GIF

## Requirements

- Python 3.7+
- Flask
- Pillow
- requests
- python-dotenv 