from flask import Blueprint
from common import CustomLogger, log_function

# Initialize the logger for this blueprint
logger = CustomLogger.get_logger(__name__)

fec_blueprint = Blueprint('fec', __name__)

@fec_blueprint.route('/')
@log_function(logger)
def home():
    logger.info("FEC home page accessed")
    return "This is the fec home page."
