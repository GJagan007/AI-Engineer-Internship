"""
Main Flask Application
"""
import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from routes.compile import compile_bp
from routes.metrics import metrics_bp
from routes.health import health_bp
from utils.logger import logger

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Register blueprints
app.register_blueprint(compile_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(health_bp)


@app.route('/')
def index():
    """Serve frontend"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/css/<path:path>')
def serve_css(path):
    """Serve CSS files"""
    return send_from_directory('../frontend/css', path)


@app.route('/js/<path:path>')
def serve_js(path):
    """Serve JS files"""
    return send_from_directory('../frontend/js', path)


@app.route('/assets/<path:path>')
def serve_assets(path):
    """Serve asset files"""
    return send_from_directory('../frontend/assets', path)


if __name__ == '__main__':
    logger.info(f"🚀 Starting AI Compiler Server on port {config.port}")
    logger.info(f"📡 Mode: {'Production' if config.has_openai_key else 'Mock'}")
    logger.info(f"🌐 Open: http://localhost:{config.port}")
    
    app.run(
        host='0.0.0.0',
        port=config.port,
        debug=config.debug
    )