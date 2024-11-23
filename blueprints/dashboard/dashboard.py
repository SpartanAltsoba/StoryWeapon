# blueprints/dashboard/dashboard.py

from flask import Blueprint, jsonify
import json
from config import Config
import logging

dashboard_blueprint = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)

@dashboard_blueprint.route('/data', methods=['GET'])
def get_dashboard_data():
    try:
        with open(Config.JSON_RESULTS, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'data': data})
    except Exception as e:
        logger.error(f"Error loading dashboard data: {e}")
        return jsonify({'error': 'Failed to load data'}), 500
