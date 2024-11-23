# 17thSCOG Application

Table of Contents

Overview
Features
Architecture
Workflow Diagrams
Installation
Configuration
Usage
Logging & Error Handling
Contributing
License
Contact
Overview
17thSCOG (Special Citizen Operations Group) is a Flask-based web application designed to process and analyze IRS Form 990 data for non-profit organizations. The application enables users to search for non-profits by name, extract relevant data from CSV and PDF files, parse and clean the extracted text, and structure the data into a JSON format using the GPT-4-turbo Mini API. The system incorporates robust logging, error handling, and a user-friendly interface with status indicators to ensure a seamless user experience.

Features
Entity Search: Users can search for non-profit entities by name. Data Extraction: Extracts EIN numbers from CSV databases and locates corresponding IRS Form 990 PDFs. PDF Parsing: Utilizes pdfplumber to extract and clean text from PDFs. JSON Structuring: Structures cleaned data into JSON format using the GPT-4-turbo Mini API, following a predefined YAML schema. User Feedback: Provides real-time workflow status indicators and actionable buttons. Error Handling: Comprehensive logging and user-friendly error messages. Modular Architecture: Built with Flask blueprints for scalability and maintainability. Interactive UI: Features a responsive interface with Bootstrap and DataTables for enhanced user interaction.

Architecture
Complete OSINT Sequence

PlantUML Sequence Diagram: Complete_OSINT_Sequence.puml
GPT Analytical Process

PlantUML Sequence Diagram: GPT_Analytical_Process.puml
For detailed workflows, refer to the PlantUML files provided in the diagrams/ directory.

Installation
Prerequisites
Python 3.8+
pip (Python package installer)
Virtual Environment (recommended)
Steps
Clone the repository:
git clone [https://github.com/yourusername/17thSCOG.git](https://github.com/yourusername/17thSCOG.git)
cd 17thSCOG
Create a Virtual Environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Set Up Data Directories
Ensure the following directories exist and have the necessary data:
C:\17_SOG\data\Shared_Entity_Name_Database_(SEDB)
C:\17_SOG\data\pdfs
C:\17_SOG\data\shared_entity_990
C:\17_SOG\data\parsed
C:\17_SOG\data\cleaned_batched
C:\17_SOG\data\json_results
C:\17_SOG\data\schemas\gpt_schema.yaml
Configuration
Create a .env file in the project root with the following content:

Secret Key
FLASK_SECRET_KEY=your_flask_secret_key

API Keys
OPENAI_API_KEY=your_openai_api_key GOOGLE_SEARCH_API_KEY=your_google_search_api_key GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id FEC_API_KEY=your_fec_api_key EDGAR_API_KEY=your_edgar_api_key GOOGLE_VISION_API_KEY=your_google_vision_api_key GEOCACHING_API_KEY=your_geocaching_api_key

Paths for data directories
CSV_FOLDER=C:\17_SOG\data\Shared_Entity_Name_Database_(SEDB) LOBBY_VIEW_API_KEY=your_lobby_view_api_key Shared_Entity_Name_Database_(SEDB)

Logging Configuration
LOG_TO_STDOUT=false GPT_4o_MINI_TASKING=C:\17_SOG\gpt-40_tasking.yaml JSON_RESULTS=C:\17_SOG\data\json_results LOG_TO_STDOUT=false Ensure all API keys and paths are correctly set according to your environment.

Determine the base directory
basedir = os.path.abspath(os.path.dirname(file))

Load environment variables from .env file
load_dotenv(os.path.join(basedir, '.env'))

class Config: # Flask Configuration SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

## API Keys

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

## Paths for data directories

CSV_PATH = os.getenv('CSV_FOLDER', 'C:\\17_SOG\\data\\Shared_Entity_Name_Database_(SEDB)')
PDF_FOLDER = os.getenv('PDF_FOLDER', 'C:\\17_SOG\\data\\pdfs')
SHARED_ENTITY_990 = os.getenv('SHARED_ENTITY_990', 'C:\\17_SOG\\data\\shared_entity_990')
PARSED_TEXT = os.getenv('PARSED_TEXT', 'C:\\17_SOG\\data\\parsed')
SCHEMA_PATH = os.getenv('SCHEMA_PATH', 'C:\\17_SOG\\data\\schemas\\gpt_schema.yaml')
JSON_RESULTS = os.getenv('JSON_RESULTS', 'C:\\17_SOG\\data\\json_results')

## Logging Configuration

LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')
Logging The application uses a rotating file handler to manage logs, ensuring logs do not grow indefinitely.

Log File: logs/app.log Log Level: DEBUG for detailed logs The application will run in debug mode by default. Access it via <http://localhost:5000>.

Running the Application Activate Virtual Environment

source venv/bin/activate # On Windows: venv\Scripts\activate

Start the Flask Application The application will run in debug mode by default. Access it via <http://localhost:5000>.

python app.py The application will run in debug mode by default. Access it via <http://localhost:5000>.

Application Workflow Search for an Entity

Navigate to the Search Page. Enter the non-profit entity name and click Button A (Search). The system searches CSV files for the entity name, extracts the EIN, and locates the corresponding IRS Form 990 PDF.

Parsing and Cleaning

The located PDF is copied to the shared_entity_990 directory. pdfplumber extracts text from the PDF, which is then cleaned and batched every 1500 words.

User Feedback

Upon completion of parsing and cleaning, a Green Light Indicator is displayed. Button B becomes active, allowing users to initiate JSON structuring.

JSON Structuring

Clicking Button B triggers an API call to the GPT-4-turbo Mini API. The cleaned text batches are structured into JSON format based on the predefined YAML schema. The structured JSON is saved in the json_results directory.

Error Handling

Any errors encountered during the workflow are logged in logs/app.log and user-friendly messages are displayed.

Logging & Error Handling Logging Location: logs/app.log Configuration: Implemented using RotatingFileHandler to manage log sizes. Details Logged: Application startup Blueprint registrations Data retrieval and parsing status API interactions Errors and exceptions

Error Handling Scenarios Handled: EIN not found PDF not found API request failures User Notifications: Friendly error messages are displayed on the UI. Log Entries: Detailed error information is logged for debugging purposes.

Contributing Contributions are welcome! Please follow these steps to contribute:

Fork the Repository Create a Feature Branch bash Copy code git checkout -b feature/YourFeature Commit Your Changes Push to the Branch bash Copy code git push origin feature/YourFeature Open a Pull Request Please ensure your code adheres to the project's coding standards and includes appropriate tests.

Email: <andyfayal@gmail.com>

License This project is licensed under the MIT License.
