from etl.db import get_db_cursor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_cities():
    cities = [
        (1, 'Mumbai', 'Maharashtra', 19.0760, 72.8777),
        (2, 'Delhi', 'Delhi', 28.7041, 77.1025),
        (3, 'Bangalore', 'Karnataka', 12.9716, 77.5946),
        (4, 'Chennai', 'Tamil Nadu', 13.0827, 80.2707),
        (5, 'Kolkata', 'West Bengal', 22.5726, 88.3639)
    ]

    try:
        with get_db_cursor(commit=True) as cursor:
            # Check if exists
            cursor.execute("SELECT COUNT(*) FROM city")
            count = cursor.fetchone()[0]
            if count == 0:
                logger.info("Seeding Cities...")
                for c in cities:
                    cursor.execute(
                        "INSERT INTO city (city_id, city_name, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s)",
                        c
                    )
                logger.info(f"Seeded {len(cities)} cities.")
            else:
                logger.info(f"Cities table already has {count} records. Skipping seed.")
    except Exception as e:
        logger.error(f"Seed failed: {e}")

if __name__ == "__main__":
    seed_cities()
