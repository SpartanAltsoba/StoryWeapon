# utils/utils_functions.py

# Standard library imports
import os
import glob
import shutil
import re
import time
import csv

# Third-party library imports
from pdf2image import convert_from_path
import pytesseract
import PyPDF2  # For direct text extraction from PDFs

# Local imports
from common import CustomLogger, log_function
from config import Config

# Initialize custom logger for utils_functions with its own log file
logger = CustomLogger.get_logger(__name__, log_file=Config.UTILS_LOG_FILE)
logger.propagate = False

@log_function(logger)
def search_csv_for_name(entity_name):
    """
    Searches all CSV files in the Shared Entity Name Database (SEDB) directory
    for the given entity_name in column B (index 1). Extracts the corresponding
    EIN from column A (index 0).
    """
    ein_list = []
    try:
        # Define the path to the SEDB directory
        sedb_directory = Config.SEDB_FOLDER  # We'll define this in config.py
        csv_files = [os.path.join(sedb_directory, f"{i}.csv") for i in range(1, 14)]
        normalized_entity = re.sub(r'\s+', '', entity_name.lower())
        for csv_file in csv_files:
            if not os.path.exists(csv_file):
                logger.warning(f"CSV file not found: {csv_file}")
                continue
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Assuming the first row is the header
                headers = next(reader, None)
                if headers is None:
                    logger.warning(f"CSV file {csv_file} is empty.")
                    continue
                # Determine the indices for EIN and NAME columns
                ein_index = 0  # Column A
                name_index = 1  # Column B
                for row in reader:
                    if len(row) <= max(ein_index, name_index):
                        continue
                    name = row[name_index].strip().lower()
                    ein = row[ein_index].strip()
                    normalized_name = re.sub(r'\s+', '', name)
                    if normalized_entity == normalized_name and ein not in ein_list:
                        ein_list.append(ein)
                        logger.info(f"Found EIN: {ein} for entity: '{entity_name}' in file: {os.path.basename(csv_file)}")
        return ein_list
    except Exception as e:
        logger.error(f"Error searching CSVs: {e}")
        return []

@log_function(logger)
def search_pdf_by_ein(ein):
    """
    Finds PDF files that match the given EIN (first 9 digits of the filename)
    and copies them to the shared_entity_990 directory.
    """
    matched_pdfs = []
    try:
        pdf_root = Config.PDF_FOLDER
        logger.info(f"Searching PDFs for EIN: {ein}")
        # Walk through all subdirectories in the PDF_FOLDER
        for root, dirs, files in os.walk(pdf_root):
            for file in files:
                if file.startswith(ein) and file.endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    try:
                        os.makedirs(Config.SHARED_ENTITY_990, exist_ok=True)
                        shutil.copy(pdf_path, Config.SHARED_ENTITY_990)
                        matched_pdfs.append(os.path.join(Config.SHARED_ENTITY_990, os.path.basename(file)))
                        logger.info(f"Copied PDF: {os.path.basename(file)}")
                    except Exception as copy_err:
                        logger.error(f"Error copying PDF '{pdf_path}': {copy_err}")
        if not matched_pdfs:
            logger.warning(f"No PDFs found for EIN: {ein}")
    except Exception as e:
        logger.error(f"Error searching PDFs for EIN '{ein}': {e}")
    return matched_pdfs

@log_function(logger)
@log_function(logger)
def wait_for_pdf(timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        pdf_files = glob.glob(os.path.join(Config.SHARED_ENTITY_990, '*.pdf'))
        if pdf_files:
            return pdf_files[0]  # Return the first PDF found
        time.sleep(1)  # Wait for 1 second before checking again
    return None  # Return None if no PDF is found within the timeout period

@log_function(logger)
def process_pdfs():
    """
    Processes all PDFs in the SHARED_ENTITY_990 directory.
    Uses both direct text extraction and OCR for parsing.
    """
    pdf_files = glob.glob(os.path.join(Config.SHARED_ENTITY_990, '*.pdf'))
    logger.info(f"Found {len(pdf_files)} PDF files in {Config.SHARED_ENTITY_990}")

    for pdf_path in pdf_files:
        try:
            logger.info(f"Processing PDF: {os.path.basename(pdf_path)}")
            # First attempt direct text extraction
            raw_text = extract_text_from_pdf_direct(pdf_path)
            if not raw_text.strip():
                logger.info(f"No text extracted using direct method for {os.path.basename(pdf_path)}. Attempting OCR.")
                # If direct extraction fails, use OCR
                raw_text = extract_text_from_pdf_ocr(pdf_path)
            if not raw_text.strip():
                logger.warning(f"No text extracted from {os.path.basename(pdf_path)}. Skipping file.")
                continue

            cleaned_text = clean_batch_txt(raw_text)
            output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '_parsed.txt'
            output_path = os.path.join(Config.PARSED_TEXT_DIR, output_filename)
            save_text_to_file(cleaned_text, output_path)
        except Exception as e:
            logger.error(f"Error processing PDF {os.path.basename(pdf_path)}: {e}")
            pass

@log_function(logger)
def extract_text_from_pdf_direct(pdf_path):
    """
    Extracts text from a PDF using PyPDF2 (direct text extraction).
    """
    try:
        logger.info(f"Extracting text directly from PDF: {os.path.basename(pdf_path)}")
        reader = PyPDF2.PdfReader(pdf_path)
        full_text = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                full_text.append(f"\n[Page {page_number}]\n{text}")
        combined_text = "\n".join(full_text)
        logger.info(f"Successfully extracted text directly from PDF: {os.path.basename(pdf_path)}")
        return combined_text
    except Exception as e:
        logger.error(f"Error during direct text extraction for {os.path.basename(pdf_path)}: {e}")
        return ""

@log_function(logger)
def extract_text_from_pdf_ocr(pdf_path):
    """
    Extracts text from a PDF using OCR (pytesseract).
    """
    try:
        logger.info(f"Converting PDF to images for OCR: {os.path.basename(pdf_path)}")
        images = convert_from_path(pdf_path, dpi=300)
        full_text = []

        for page_number, image in enumerate(images, start=1):
            text = pytesseract.image_to_string(image)
            if text:
                full_text.append(f"\n[Page {page_number}]\n{text}")
        combined_text = "\n".join(full_text)
        logger.info(f"Successfully extracted text via OCR from PDF: {os.path.basename(pdf_path)}")
        return combined_text
    except Exception as e:
        logger.error(f"Error during OCR for {os.path.basename(pdf_path)}: {e}")
        return ""

def clean_batch_txt(raw_text):
    """
    Cleans the raw text extracted from the PDF.
    """
    try:
        logger.info("Cleaning extracted text...")
        # Preserve headings and key naming conventions
        # Remove unnecessary whitespace but keep line breaks
        cleaned_text = re.sub(r'[ \t]+', ' ', raw_text)
        # Normalize line endings
        cleaned_text = cleaned_text.replace('\r\n', '\n').replace('\r', '\n')
        # Remove non-printable characters
        cleaned_text = ''.join(c for c in cleaned_text if c.isprintable())
        logger.info("Text cleaned successfully.")
        return cleaned_text
    except Exception as e:
        logger.error(f"Error during text cleaning: {e}")
        return raw_text

@log_function(logger)
def get_parsed_files(directory):
    """
    Get a list of parsed text files from the specified directory.
    """
    try:
        if not os.path.exists(directory):
            logger.error(f"Directory does not exist: {directory}")
            return []
        
        # Filter for files with a .txt extension
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        parsed_files = [os.path.join(directory, f) for f in files if f.endswith('.txt')]
        logger.info(f"Found {len(parsed_files)} parsed files in {directory}")
        return parsed_files
    except Exception as e:
        logger.error(f"Error getting parsed files: {str(e)}")
        return []

@log_function(logger)
def save_text_to_file(cleaned_text, output_path):
    """
    Saves cleaned text to a .txt file.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        logger.info(f"Saved cleaned text to {output_path}")
    except Exception as e:
        logger.error(f"Error saving text file: {e}")