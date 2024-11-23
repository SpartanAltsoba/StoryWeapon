from flask import Blueprint
from common import CustomLogger, log_function

# Initialize the logger for this blueprint
logger = CustomLogger.get_logger(__name__)

court_listener_blueprint = Blueprint('court_listener', __name__)

@court_listener_blueprint.route('/')
@log_function(logger)
def home():
    logger.info("Court Listener home page accessed")
    return "This is the court_listener home page."
