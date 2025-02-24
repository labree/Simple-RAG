from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from modules import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
