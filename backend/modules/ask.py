from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def register_ask_routes(app):
    @app.route('/api/ask', methods=['POST'])
    def ask_gemini():
        data = request.json
        prompt = data.get('prompt', '')

        # Create a chat model instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[])

        # Send the prompt to Gemini and get a response
        response = chat.send_message(prompt)

        return jsonify({'response': response.text})

    @app.route('/api/ask-context', methods=['POST'])   
    def ask_gemini_with_context():
        data = request.json
        prompt = data.get('prompt', '')
        urls = data.get('urls', [])

        content = ["The folliwng text are taken from various websites and will serve as context for the following conversation"]
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            content.append(text)
        content = " ".join(content)
        context = content
        
        # Create a chat model instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": [{"text": context}]
            },
            {
                "role": "model",
                "parts": [{"text": "Understood."}]
            }
        ])

        # Send the prompt to Gemini and get a response
        response = chat.send_message(prompt)

        return jsonify({'response': response.text})