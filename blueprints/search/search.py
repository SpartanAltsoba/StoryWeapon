# blueprints/search.py

import os
from flask import Blueprint, render_template, request, jsonify
from utils.utils_functions import search_csv_for_name, search_pdf_by_ein, process_pdfs, get_parsed_files
from config import Config
from common import CustomLogger, log_function

# Initialize logger for Search Blueprint with its own log file
logger = CustomLogger.get_logger(__name__, log_file=Config.SEARCH_LOG_FILE)
logger.propagate = False

# Initialize the Search Blueprint
search_blueprint = Blueprint('search', __name__, template_folder='templates')

@search_blueprint.route('/', methods=['GET', 'POST'])
@log_function(logger)
def handle_search():
    if request.method == 'GET':
        logger.info("Accessed search home page.")
        return render_template('search.html')

    elif request.method == 'POST':
        logger.info("Received POST request for search.")
        try:
            # Get JSON data from the request
            data = request.get_json()
            if not data:
                logger.warning("No JSON received in the POST request.")
                return jsonify({'message': 'Invalid request. No data provided.'}), 400

            entity_name = data.get('entity_name', '').strip()
            if not entity_name:
                logger.warning("Entity name is empty or missing.")
                return jsonify({'message': 'Entity name is required.'}), 400

            logger.info(f"Searching for entity: {entity_name}")
            
            # Step 1: Search for EIN
            ein_list = search_csv_for_name(entity_name)
            if not ein_list:
                logger.warning(f"No EIN found for entity: {entity_name}")
                return jsonify({'message': 'Entity not found.'}), 404

            logger.info(f"EINs found: {ein_list}")

            # Step 2: Search for PDFs using EINs
            matched_pdfs = []
            for ein in ein_list:
                pdfs = search_pdf_by_ein(ein)
                matched_pdfs.extend(pdfs)
            
            if not matched_pdfs:
                logger.warning(f"No PDFs found for EINs: {ein_list}")
                return jsonify({'message': 'No PDFs found.'}), 404

            logger.info(f"PDFs found: {matched_pdfs}")

            # Step 3: Parse and clean PDFs
            process_pdfs()
            parsed_files = get_parsed_files(Config.PARSED_TEXT_DIR)
            if not parsed_files:
                logger.warning("No parsed files created.")
                return jsonify({'message': 'Parsing failed.'}), 500

            logger.info(f"Parsed files created: {parsed_files}")

            # Step 4: Signal success
            logger.info("Search and parsing workflow completed successfully.")
            return jsonify({
                'message': 'Search and parsing completed successfully.',
                'parsed_files': parsed_files
            }), 200

        except Exception as e:
            logger.error(f"Error during search workflow: {e}")
            return jsonify({'message': 'An error occurred during the search process.'}), 500
