from flask import request, jsonify
import requests
from bs4 import BeautifulSoup

def register_extract_routes(app):
    @app.route('/api/extract', methods=['POST'])
    def extract_content():
        data = request.json
        urls = data.get('urls', [])

        content = []
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            content.append(text)

        # Here you would integrate with the Gemini API using the extracted content and prompt.
        # For demonstration, we'll return the raw text.
        return jsonify({'content': content})
