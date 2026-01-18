import sys
import os
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

def run_aqi_etl():
    csv_path = os.path.join(Config.DATA_DIR, 'csv', 'aqi.csv')
    
    logger.info("Starting AQI ETL for CSV...")
    raw_data = Extractor.extract_csv(csv_path)
    transformed_data = [Transformer.transform_aqi_csv(row) for row in raw_data]
    valid = []
    dropped = 0

    for d in transformed_data:
        if d:
            valid.append(d)
        else:
            dropped += 1

    logger.warning(f"Dropped {dropped} invalid rows")
    
    count = Loader.load_aqi_data(transformed_data)
    logger.info(f"AQI ETL Completed. Inserted {count} records.")

if __name__ == "__main__":
    try:
        run_aqi_etl()
    except Exception as e:
        logger.error(f"ETL Job Failed: {e}")
