import sys
import os
import argparse
import logging

# Ensure parent directory is in path

from etl.config import Config
from etl.pipeline.extract import Extractor
from etl.pipeline.transform import Transformer
from etl.pipeline.load import Loader

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_weather_etl(source='all'):
    csv_path = os.path.join(Config.DATA_DIR, 'csv', 'weather.csv')
    
    # 1. Process CSV Data
    if source in ['all', 'csv']:
        logger.info("Starting Weather ETL for CSV...")
        raw_data = Extractor.extract_csv(csv_path)
        transformed_data = [Transformer.transform_weather_csv(row) for row in raw_data]
        # Filter None
        valid = []
        dropped = 0

        for d in transformed_data:
            if d:
                valid.append(d)
            else:
                dropped += 1

        logger.warning(f"Dropped {dropped} invalid rows")
        
        count = Loader.load_weather_data(transformed_data)
        logger.info(f"Weather CSV ETL Completed. Inserted {count} records.")

    # 2. Process API Data (Live)
    if source in ['all', 'api']:
        logger.info("Starting Weather ETL for API...")
        api_key = Config.OPENWEATHER_API_KEY
        if not api_key:
            logger.warning("No API Key found for OpenWeatherMap. Skipping API ingestion.")
        else:
            # Delhi Coordinates
            lat, lon = 28.7041, 77.1025
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'metric'
            }
            
            raw_data = Extractor.extract_from_api(url, params)
            if raw_data:
                cleaned = Transformer.transform_weather_api(raw_data)
                if cleaned:
                    count = Loader.load_weather_data([cleaned])
                    logger.info(f"Weather API ETL Completed. Inserted {count} records.")
                else:
                    logger.warning("Transformation of API data failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Weather ETL")
    parser.add_argument('--source', type=str, default='all', choices=['all', 'csv', 'api'], help="Data source to run")
    args = parser.parse_args()
    
    try:
        run_weather_etl(args.source)
    except Exception as e:
        logger.error(f"ETL Job Failed: {e}")
