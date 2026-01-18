import pandas as pd

FILE_PATH = "etl/data_sources/csv/health.csv"  # change as needed

df = pd.read_csv(FILE_PATH)

# Define what "duplicate" means (logical duplicate)
key_columns = ["city", "date", "health_risk_score", "risk_level"]

# Check duplicates
duplicates = df[df.duplicated(subset=key_columns, keep=False)]

print(f"Total rows: {len(df)}")
print(f"Duplicate rows (same city + date): {len(duplicates)}")

if not duplicates.empty:
    print("\nSample duplicate records:")
    print(duplicates.head(10))
else:
    print("\nNo logical duplicates found.")
