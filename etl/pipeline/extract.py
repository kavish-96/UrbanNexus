import csv
import json
import requests
import logging

logger = logging.getLogger(__name__)

class Extractor:
    @staticmethod
    def extract_csv(file_path):
        """
        Reads a CSV file and yields records as dictionaries.
        """
        try:
            logger.info(f"Extracting data from CSV: {file_path}")
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                logger.info(f"Extracted {len(data)} records from CSV.")
                return data
        except Exception as e:
            logger.error(f"Failed to extract CSV {file_path}: {e}")
            return []

    @staticmethod
    def extract_json(file_path):
        """
        Reads a JSON file and returns the data payload.
        Assumes JSON is a list of records or has a 'data' key.
        """
        try:
            logger.info(f"Extracting data from JSON: {file_path}")
            with open(file_path, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle cases where data might be wrapped
                if isinstance(data, dict):
                    # Try to find the list
                    for key in ['data', 'results', 'records']:
                        if key in data and isinstance(data[key], list):
                            data = data[key]
                            break
                if not isinstance(data, list):
                    # If it's a single dict, make it a list
                    data = [data]
                
                logger.info(f"Extracted {len(data)} records from JSON.")
                return data
        except Exception as e:
            logger.error(f"Failed to extract JSON {file_path}: {e}")
            return []

    @staticmethod
    def extract_from_api(url, params=None):
        """
        Fetches data from an API endpoint.
        """
        try:
            logger.info(f"Fetching data from API: {url} with params: {params}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info("API request successful.")
            return data
        except Exception as e:
            logger.error(f"API extraction failed: {e}")
            return None
