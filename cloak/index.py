from flask import Flask, request, send_file, jsonify
import requests
import socks
import socket
from io import BytesIO

app = Flask(__name__)

# Configure the SOCKS5 proxy
SOCKS5_PROXY = '113.121.248.200'
SOCKS5_PORT = 8118

# Setup SOCKS5 proxy globally
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY, SOCKS5_PORT)
socket.socket = socks.socksocket


@app.route('/')
def index():
    # Serve the HTML content directly from this route
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Proxy Browser</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f4f4f4;
            }
            input, button {
                padding: 10px;
                margin: 5px;
            }
            iframe {
                width: 80%;
                height: 80%;
                border: none;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Proxy Browser</h1>
        <input type="text" id="proxy-url" placeholder="Enter URL">
        <button onclick="browse()">Browse</button>
        <iframe id="proxy-iframe" src=""></iframe>

        <script>
            function browse() {
                let url = document.getElementById('proxy-url').value;
                if (!url.startsWith('http')) {
                    url = 'http://' + url;
                }

                // Use the backend server to fetch the proxied URL
                document.getElementById('proxy-iframe').src = '/proxy?url=' + encodeURIComponent(url);
            }
        </script>
    </body>
    </html>
    '''
    return html_content


@app.route('/proxy')
def proxy():
    # Get the URL to proxy from the query string
    target_url = request.args.get('url')

    if not target_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Fetch the content from the target URL using the SOCKS5 proxy
        response = requests.get(target_url)
        return response.content, response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
