from flask import Flask, render_template, request
import os
from config import Config
from blueprints.dashboard import dashboard_blueprint
from blueprints.search import search_blueprint
from blueprints.gpt_handler import gpt_handler_blueprint
from blueprints.civic_info import civic_info_blueprint
from blueprints.fec import fec_blueprint
from blueprints.edgar import edgar_blueprint
from blueprints.court_listener import court_listener_blueprint
from blueprints.lobby_view import lobby_view_blueprint
from common import CustomLogger, log_function

# Initialize the logger
logger = CustomLogger.get_logger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(search_blueprint, url_prefix='/search')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(gpt_handler_blueprint, url_prefix='/gpt_handler')
app.register_blueprint(civic_info_blueprint, url_prefix='/civic_info')
app.register_blueprint(fec_blueprint, url_prefix='/fec')
app.register_blueprint(edgar_blueprint, url_prefix='/edgar')
app.register_blueprint(court_listener_blueprint, url_prefix='/court_listener')
app.register_blueprint(lobby_view_blueprint, url_prefix='/lobby_view')


# Define the home route with logging
@app.route('/')
@log_function(logger)
def home():
    logger.info("Home page accessed")
    return render_template('index.html')  # Ensure 'index.html' exists in templates/

# Unified 404 Error Handler with logging
@app.errorhandler(404)
@log_function(logger)
def not_found_error(error):
    logger.error(f'404 Error: {error} - Path: {request.path}')
    return render_template('404.html'), 404

# 500 Internal Server Error Handler with logging
@app.errorhandler(500)
@log_function(logger)
def internal_error(error):
    logger.error(f'500 Error: {error} - Path: {request.path} - Method: {request.method}', exc_info=True)
    return render_template('500.html'), 500

# Ensure required directories exist before running the app
required_dirs = [
    Config.CSV_FOLDER,
    Config.PDF_FOLDER,
    Config.SHARED_ENTITY_990,
    Config.PARSED_TEXT_DIR,
    Config.JSON_RESULTS,
    Config.CLEANED_BATCHED_DIR,
    os.path.dirname(Config.SCHEMA_PATH),
    os.path.dirname(Config.LOG_FILE),
]

for directory in required_dirs:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created missing directory: {directory}")
    except OSError as e:
        print(f"Error creating directory {directory}: {e}")
        raise  # Re-raise the exception after logging

# Run the application
if __name__ == '__main__':
    logger.info("Starting the application")
    app.run(debug=True)
