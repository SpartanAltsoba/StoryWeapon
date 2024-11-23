# blueprints/gpt_handler/gpt_handler.py

from flask import Blueprint, jsonify, current_app
from dotenv import load_dotenv 
import yaml
import json
import os
from openai import OpenAI
from config import Config
from common import CustomLogger, log_function
import glob

# Initialize logger for GPT Handler Blueprint with its own log file
logger = CustomLogger.get_logger(__name__, log_file=Config.GPT_HANDLER_FILE)
logger.propagate = False

# Create blueprint
gpt_handler_blueprint = Blueprint('gpt_handler', __name__)

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@gpt_handler_blueprint.route('/', methods=['POST'])
@log_function(logger)
def gpt_main():
    try:
        # Call your main GPT processing function
        extracted_data = main()
        if extracted_data:
            # Return the extracted data as JSON
            return jsonify({
                'success': True,
                'message': 'Key information extracted successfully.',
                'extracted_data': extracted_data,
                'download_url': '/dashboard/data'  # Adjust this if needed
            })
        else:
            return jsonify({'success': False, 'message': 'No data extracted.'}), 500
    except Exception as e:
        logger.error(f"Error in GPT handler: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@log_function(logger)
def main():
    # Load the schema, prompts, and output requirements schema
    schema = load_yaml_file(Config.SCHEMA_PATH)
    prompts = load_yaml_file(Config.PROMPTS_PATH)
    output_requirements = load_yaml_file(Config.OUTPUT_REQUIREMENTS_SCHEMA)
    if not schema or not prompts or not output_requirements:
        logger.error("Schema, prompts, or output requirements could not be loaded. Exiting.")
        return None

    # Get list of text files in the directory
    parsed_text_dir = Config.PARSED_TEXT_DIR  # Ensure this is correctly set in Config
    text_files = get_text_files_in_directory(parsed_text_dir)
    if not text_files:
        logger.error("No text files found in the directory. Exiting.")
        return None

    # Delete existing JSON file
    clear_output_file(Config.JSON_RESULTS)

    # Process each text file
    for text_file in text_files:
        logger.info(f"Processing file: {text_file}")
        text_content = read_text_file(text_file)
        if not text_content:
            logger.error(f"Text content could not be loaded from {text_file}. Skipping.")
            continue

        # Generate the prompt
        prompt = generate_prompt(text_content, schema, prompts, output_requirements)
        if not prompt:
            logger.error("Prompt could not be generated. Skipping file.")
            continue

        # Call the GPT API
        response_text = call_gpt_api(prompt)
        if not response_text:
            logger.error("No response from GPT API. Skipping file.")
            continue

        # Parse the GPT response
        json_data = parse_gpt_response(response_text)
        if not json_data:
            logger.error("Failed to parse JSON data. Skipping file.")
            continue

        # Save the JSON data directly to 'results.json'
        output_file_path = Config.JSON_RESULTS
        save_json_data(json_data, output_file_path)
        logger.info(f"Saved results to {output_file_path}")

        # Prepare data for the response
        extracted_data = prepare_extracted_data(json_data)
        return extracted_data  # Return the data for use in the AJAX response

    return None  # If no data was extracted

@log_function(logger)
def load_yaml_file(file_path):
    """
    Loads a YAML file.
    Args:
        file_path (str): Path to the YAML file.
    Returns:
        dict: The YAML content as a dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        logger.info(f"Loaded YAML file: {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error loading YAML file {file_path}: {e}")
        return None

@log_function(logger)
def prepare_extracted_data(json_data):
    """
    Prepares the extracted data for the frontend.

    Args:
        json_data (dict): The JSON data extracted by GPT.

    Returns:
        list: A list of dictionaries containing the data to display.
    """
    try:
        data_list = []
        general_info = json_data.get('general_info', {})
        financial_data = json_data.get('financial_data', {})
        board_members = json_data.get('board_members', [])

        # Prepare compensation details
        compensation_details = []
        for member in board_members:
            name = member.get('name', '')
            compensation = member.get('compensation', 0)
            compensation_details.append(f"{name}: ${compensation:,.2f}")

        data_entry = {
            'name': general_info.get('name', ''),
            'ein': general_info.get('ein', ''),
            'revenue': financial_data.get('total_revenue', 0),
            'expenses': financial_data.get('total_expenses', 0),
            'net_income': financial_data.get('total_revenue', 0) - financial_data.get('total_expenses', 0),
            'compensation': '; '.join(compensation_details) if compensation_details else 'N/A'
        }
        data_list.append(data_entry)
        return data_list
    except Exception as e:
        logger.error(f"Error preparing extracted data: {e}")
        return []

@log_function(logger)
def clear_output_file(file_path):
    """
    Deletes the specified JSON file if it exists.
    Args:
        file_path (str): Path to the JSON file.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted old JSON file: {file_path}")
    except PermissionError as e:
        logger.error(f"Permission error while clearing output file {file_path}: {e}")
    except Exception as e:
        logger.error(f"Error clearing output file {file_path}: {e}")
        
@log_function(logger)
def get_text_files_in_directory(directory_path):
    """
    Gets a list of all text files in the specified directory.
    Args:
        directory_path (str): Path to the directory containing text files.
    Returns:
        list: List of text file paths.
    """
    try:
        pattern = os.path.join(directory_path, '*.txt')
        text_files = glob.glob(pattern)
        logger.info(f"Found {len(text_files)} text files in directory {directory_path}")
        return text_files
    except Exception as e:
        logger.error(f"Error getting text files from directory {directory_path}: {e}")
        return []

@log_function(logger)
def read_text_file(file_path):
    """
    Reads the content of the text file containing Form 990 information.
    Args:
        file_path (str): Path to the text file.
    Returns:
        str: Content of the text file.
    """
    try:
        logger.debug(f"Attempting to read file at: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        logger.info(f"Successfully loaded text file: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {str(e)}")
        return ""

@log_function(logger)
def generate_prompt(text, schema, prompts, output_requirements):
    """
    Generates a prompt for the GPT model using the provided text, schema, prompts, and output requirements.
    Args:
        text (str): The text to be structured.
        schema (dict): The YAML schema defining JSON structure.
        prompts (dict): The prompts loaded from the prompts YAML file.
        output_requirements (dict): Additional output requirements loaded from the output requirements YAML file.
    Returns:
        str: The complete prompt.
    """
    try:
        # Prepare the schema and prompt
        schema_json = json.dumps(schema.get('schema', {}), indent=2)
        output_requirements_text = output_requirements.get('output_requirements', '')
        instructions_text = output_requirements.get('instructions', '')
        batch_extraction_prompt = prompts.get('batch_extraction_prompt', '')  # Changed from data_extraction_prompt
        system_prompt = prompts.get('system_prompt', '')
        prompt = (
            f"{system_prompt}\n\n"
            f"{instructions_text}\n\n"
            f"{batch_extraction_prompt}\n\n"  # Added this line to include the batch extraction prompt
            f"JSON Schema:\n```json\n{schema_json}\n```\n\n"
            f"Output Requirements:\n{output_requirements_text}\n\n"
            f"IRS Form 990 Text:\n```text\n{text}\n```\n\n"
            f"Please output only the JSON data as per the schema without any additional text or markdown."
    )
        logger.info("Generated prompt for GPT model.")
        return prompt
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        return ""

@log_function(logger)
def call_gpt_api(prompt):
    """
    Calls the GPT API with the given prompt.
    Args:
        prompt (str): The prompt to send to the API.
    Returns:
        str: The API response text.
    """
    try:
        response = client.chat.completions.create(
            model="o1-preview-2024-09-12",  
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_completion_tokens=3000,
            n=1,
        )
        gpt_response = response.choices[0].message.content.strip()
        logger.info("GPT API call successful.")
        return gpt_response
    except Exception as e:
        logger.error(f"Error calling GPT API: {e}")
        return ""

@log_function(logger)
def parse_gpt_response(response_text):
    """
    Parses the GPT API response into JSON.
    Args:
        response_text (str): The raw response from GPT.
    Returns:
        dict: The structured JSON data.
    """
    try:
        json_data = json.loads(response_text)
        logger.info("Parsed GPT response into JSON successfully.")
        return json_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse GPT response as JSON: {e}")
        # Attempt to extract JSON from response
        try:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            json_str = response_text[json_start:json_end]
            json_data = json.loads(json_str)
            logger.info("Extracted JSON from GPT response successfully after adjustment.")
            return json_data
        except Exception as e:
            logger.error(f"Error extracting JSON from GPT response: {e}")
            return {}

@log_function(logger)
def save_json_data(json_data, output_path):
    """
    Saves the JSON data to a file.
    Args:
        json_data (dict): The JSON data to save.
        output_path (str): The file path to save the JSON data.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        logger.info(f"JSON data saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving JSON data: {e}")
