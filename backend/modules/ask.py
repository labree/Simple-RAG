from flask import Flask, request, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Blueprint('ask', __name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/', methods=['POST'])
def ask_gemini():
    data = request.json
    prompt = data.get('prompt', '')

    # Create a chat model instance
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])

    # Send the prompt to Gemini and get a response
    response = chat.send_message(prompt)

    return jsonify({'response': response.text})