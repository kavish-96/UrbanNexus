import sys
import os
import argparse
import logging

# Ensure parent directory is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from etl.config import Config
from pipeline.extract import Extractor
from pipeline.transform import Transformer
from pipeline.load import Loader

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_agriculture_etl(source='all'):
    # CSV Source
    if source in ['all', 'csv']:
        csv_path = os.path.join(Config.DATA_DIR, 'csv', 'agriculture.csv')
        logger.info("Starting Agriculture ETL for CSV...")
        raw_data = Extractor.extract_csv(csv_path)
        transformed_data = [Transformer.transform_agriculture_csv(row) for row in raw_data]
        valid = []
        dropped = 0

        for d in transformed_data:
            if d:
                valid.append(d)
            else:
                dropped += 1

        logger.warning(f"Dropped {dropped} invalid rows")
        
        count = Loader.load_agriculture_data(transformed_data)
        logger.info(f"Agriculture CSV ETL Completed. Inserted {count} records.")

    # JSON Source (Optional alternative)
    if source in ['all', 'json']:
        json_path = os.path.join(Config.DATA_DIR, 'json', 'agriculture.json')
        if os.path.exists(json_path):
            logger.info("Starting Agriculture ETL for JSON...")
            raw_data = Extractor.extract_json(json_path)
            transformed_data = [Transformer.transform_agriculture_json(row) for row in raw_data]
            valid = []
            dropped = 0

            for d in transformed_data:
                if d:
                    valid.append(d)
                else:
                    dropped += 1

            logger.warning(f"Dropped {dropped} invalid rows")
                            
            count = Loader.load_agriculture_data(transformed_data)
            logger.info(f"Agriculture JSON ETL Completed. Inserted {count} records.")
        else:
            logger.warning(f"JSON file not found at {json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Agriculture ETL")
    parser.add_argument('--source', type=str, default='all', choices=['all', 'csv', 'json'], help="Data source to run")
    args = parser.parse_args()
    
    try:
        run_agriculture_etl(args.source)
    except Exception as e:
        logger.error(f"ETL Job Failed: {e}")
