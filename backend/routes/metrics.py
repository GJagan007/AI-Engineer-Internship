"""
Metrics Routes
"""
from flask import Blueprint, jsonify
from pipeline.orchestrator import pipeline
from utils.logger import logger

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Get pipeline performance metrics
    
    Returns:
        Metrics object with success rate, latency, etc.
    """
    try:
        metrics = pipeline.get_metrics()
        return jsonify(metrics)
        
    except Exception as e:
        logger.error(f"Metrics route error: {e}")
        return jsonify({'error': str(e)}), 500