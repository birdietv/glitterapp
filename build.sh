#!/bin/bash

# Exit on error
set -e

# Install Python if not already installed
if ! command -v python3.11 &> /dev/null; then
    curl -L https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz | tar xz
    cd Python-3.11.0
    ./configure --enable-optimizations
    make -j $(nproc)
    make install
    cd ..
fi

# Upgrade pip
python3.11 -m pip install --upgrade pip

# Install dependencies
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install -r requirements-dev.txt

# Create the output directory
mkdir -p dist

# Copy all necessary files to the dist directory
cp -r app.py wsgi.py requirements.txt requirements-dev.txt runtime.txt static templates dist/

# Create a simple server script
cat > dist/_worker.js << EOL
export default {
  async fetch(request, env) {
    try {
      // Add CORS headers
      const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
      };

      // Handle OPTIONS request
      if (request.method === "OPTIONS") {
        return new Response(null, {
          headers: corsHeaders
        });
      }

      // Forward the request to the Flask application
      const url = new URL(request.url);
      const response = await env.FLASK_APP.fetch(request);
      
      // Add CORS headers to the response
      const newHeaders = new Headers(response.headers);
      Object.entries(corsHeaders).forEach(([key, value]) => {
        newHeaders.set(key, value);
      });

      return new Response(response.body, {
        status: response.status,
        headers: newHeaders
      });
    } catch (err) {
      return new Response(err.stack, { status: 500 });
    }
  }
}
EOL

# Make the build script executable
chmod +x build.sh 