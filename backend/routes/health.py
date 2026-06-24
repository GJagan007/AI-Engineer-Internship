"""
Health Check Routes
"""
from flask import Blueprint, jsonify
from datetime import datetime
from config import config
from utils.logger import logger

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        System health status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'mode': 'production' if config.has_openai_key else 'mock',
        'version': '1.0.0'
    })