from flask import Blueprint
from common import CustomLogger, log_function

# Initialize the logger for this blueprint
logger = CustomLogger.get_logger(__name__)

edgar_blueprint = Blueprint('edgar', __name__)

@edgar_blueprint.route('/')
@log_function(logger)
def home():
    logger.info("EDGAR home page accessed")
    return "This is the edgar home page."
