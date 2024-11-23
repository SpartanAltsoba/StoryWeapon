from flask import Blueprint
from common import CustomLogger, log_function

# Initialize the logger for this blueprint
logger = CustomLogger.get_logger(__name__)

civic_info_blueprint = Blueprint('civic_info', __name__)

@civic_info_blueprint.route('/')
@log_function(logger)
def home():
    logger.info("Civic Info home page accessed")
    return "This is the civic_info home page."
