import os
from flask import Flask

# Import route registrations
from .extract import register_extract_routes
from .ask import register_ask_routes

def create_app(test_config=None):
    
    # Create Flask instance
    app = Flask(__name__)
    
    # Register routes
    register_routes(app)

    return app

def register_routes(app):
    """Register all route blueprints"""
    register_extract_routes(app)
    register_ask_routes(app)