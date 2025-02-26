from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
#client = genai.Client(api_key="GEMINI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def register_ask_routes(app):
    @app.route('/api/ask', methods=['POST'])
    def ask_gemini():
        data = request.json
        prompt = data.get('prompt', '')

        # Create a chat model instance
        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(prompt)

        return jsonify({'response': response.text})

    @app.route('/api/ask-context', methods=['POST'])
    def ask_gemini_with_context():
        data = request.json
        prompt = data.get('prompt', '')
        urls = data.get('urls', [])

        content = ["The following text are taken from various websites and will serve as context for the following conversation:"]
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                content.append(text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL {url}: {e}")
                content.append(f"Error retrieving content from {url}.")
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                content.append(f"Error processing content from {url}.")

        context = " ".join(content)

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            [context, prompt]
        )

        return jsonify({'response': response.text})