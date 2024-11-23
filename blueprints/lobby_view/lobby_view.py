from flask import Blueprint
from common import CustomLogger, log_function

# Initialize the logger for this blueprint
logger = CustomLogger.get_logger(__name__)

lobby_view_blueprint = Blueprint('lobby_view', __name__)

@lobby_view_blueprint.route('/')
@log_function(logger)
def home():
    logger.info("Lobby View home page accessed")
    return "This is the lobby_view home page."

