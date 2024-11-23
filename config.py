import os
from dotenv import load_dotenv

# Determine the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # General Config
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
    DEBUG = True  # Set to False in production

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    FEC_API_KEY = os.getenv('FEC_API_KEY')
    EDGAR_API_KEY = os.getenv('EDGAR_API_KEY')
    GOOGLE_VISION_API_KEY = os.getenv('GOOGLE_VISION_API_KEY')
    GEOCACHING_API_KEY = os.getenv('GEOCACHING_API_KEY')
    COURTLISTENER_TOKEN = os.getenv('COURTLISTENER_TOKEN')
    GOOGLE_CIVIC_API_KEY = os.getenv('GOOGLE_CIVIC_API_KEY')
    GOOGLE_DRIVE_API = os.getenv('GOOGLE_DRIVE_API')
    LOBBY_VIEW_API_KEY = os.getenv('LOBBY_VIEW_API_KEY')
    GPT_API_ENDPOINT = os.getenv('GPT_API_ENDPOINT')
    
    # Base directory
    BASE_DIR = 'C:/17th_SCOG_OSINT_3.0'

    # Directory Paths
    CSV_FOLDER = os.getenv('CSV_PATH', os.path.join(basedir, 'data', 'csv'))
    PDF_FOLDER = os.getenv('PDF_FOLDER', os.path.join(basedir, 'data', 'pdfs'))
    SHARED_ENTITY_990 = os.getenv('SHARED_ENTITY_990', os.path.join(basedir, 'data', 'shared_entity_990'))
    PARSED_TEXT_DIR = os.getenv('PARSED_TEXT_DIR', os.path.join(basedir, 'data', 'parsed_text'))
    JSON_RESULTS = os.getenv('JSON_RESULTS', os.path.join(basedir, 'data', 'json_results'))
    CLEANED_BATCHED_DIR = os.getenv('CLEANED_BATCHED_DIR', os.path.join(basedir, 'data', 'cleaned_batched'))
    SCHEMA_PATH = os.getenv('SCHEMA_PATH', os.path.join(basedir, 'schemas', 'schema.yaml'))
    PROMPTS_PATH = os.getenv('PROMPTS_PATH', os.path.join(basedir, 'data', 'prompts.json'))
    OUTPUT_REQUIREMENTS_SCHEMA= os.getenv('OUTPUT_REQUIREMENTS_SCHEMA', os.path.join(basedir, 'schemas', 'output_requirements_schema.yaml')) # Added SEDB_FOLDER
    SEDB_FOLDER = os.getenv('SEDB_FOLDER', os.path.join(basedir, 'data', 'Shared_Entity_Name_Database_(SEDB)'))
    
    # log file paths
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(basedir, 'logs', 'app.log'))
    UTILS_LOG_FILE = os.getenv('UTILS_LOG_FILE', os.path.join(basedir, 'logs', 'utils.log'))
    SEARCH_LOG_FILE = os.getenv('SEARCH_LOG_FILE', os.path.join(basedir, 'logs', 'search.log'))
    GPT_HANDLER_FILE = os.getenv('GPT_HANDLER_FILE', os.path.join(basedir, 'logs', 'gpt_handler.log'))


    # Processing Configuration
    MAX_ENTITIES = int(os.getenv('MAX_ENTITIES', 20))  # Max number of entities to process
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 4))  # Number of entities per batch
    ENTITY_SIZE_LIMIT = int(os.getenv('ENTITY_SIZE_LIMIT', 2000000))  # 2MB size limit for processing
    PARALLEL_PROCESSING = True  # Enable parallel processing
    MEMORY_LIMIT = os.getenv('MEMORY_LIMIT', '8GB')  # Medium memory limit

    # Logger Configuration (Assuming you have a method to initialize loggers)
    @staticmethod
    def get_logger(name):
        import logging
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Prevent adding multiple handlers to the logger
        if not logger.handlers:
            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = logging.FileHandler(Config.LOG_FILE)
            c_handler.setLevel(logging.DEBUG)
            f_handler.setLevel(logging.DEBUG)

            # Create formatters and add to handlers
            c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)

        return logger
