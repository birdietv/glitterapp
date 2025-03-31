# Glitter Text Generator

A web application that generates animated glitter text GIFs. Users can input custom text, choose fonts, and apply various glitter effects.

## Features

- Custom text input
- Multiple font options
- Various glitter effects
- Animated GIF output
- Transparent background
- Download functionality

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd glittertxt
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
GOOGLE_FONTS_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

## Deployment

This application can be deployed to Render.com:

1. Create a new account on [Render](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: glitter-text-generator (or your preferred name)
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables:
   - GOOGLE_FONTS_API_KEY=your_api_key_here

## License

MIT License 