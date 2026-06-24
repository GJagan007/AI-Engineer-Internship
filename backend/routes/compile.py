"""
Compilation Routes
"""
from flask import Blueprint, request, jsonify
from pipeline.orchestrator import pipeline
from utils.logger import logger

compile_bp = Blueprint('compile', __name__)


@compile_bp.route('/compile', methods=['POST'])
def compile_prompt():
    """
    Compile user prompt into application configuration
    
    Request body:
        {
            "prompt": "User requirements"
        }
    
    Returns:
        Complete compilation result
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing "prompt" field'}), 400
        
        prompt = data['prompt']
        logger.info(f"Received compile request: {prompt[:100]}...")
        
        result = pipeline.compile(prompt)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Compile route error: {e}")
        return jsonify({'error': str(e)}), 500