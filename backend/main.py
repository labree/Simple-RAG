from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from backend.modules.extract import app as extract
from backend.modules.ask import app as ask

app = Flask(__name__)
app.register_blueprint(extract, url_prefix='/api/extract')
app.register_blueprint(ask, url_prefix='/api/ask')

if __name__ == '__main__':
    app.run(debug=True)
