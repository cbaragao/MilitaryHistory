import os
import pandas as pd
from pathlib import Path
from main import Main
from transformcoordinates import TransformCoordinates
from ddw import DDW

class DatasetProcessor:
    """Handles processing, transformation, and uploading of dataset files."""

    def __init__(self, dataset: str, datadotworld_project: str, lat_lon_pairs: list = None):
        self.dataset = dataset.lower()
        self.datadotworld_project = datadotworld_project
        self.processor = Main(self.dataset)
        self.transformer = TransformCoordinates()
        self.lat_lon_pairs = lat_lon_pairs or []  # Default to empty if none provided

    def process(self):
        """Main function to process and upload dataset."""
        db = self.processor.create_base_tables()
        df = db.execute(self.processor.get_sql()).fetchdf()

        # Process UTM coordinates if applicable
        df_transformed = self.process_utm(df)

        # Save transformed data to DuckDB
        db.sql(f"DROP TABLE IF EXISTS {self.dataset}_tx")
        db.sql(f"CREATE TABLE {self.dataset}_tx AS SELECT * FROM df_transformed")

        # Export to CSV and upload
        self.upload_to_datadotworld(df_transformed)

        # Cleanup
        self.processor.delete_file(f"{self.dataset}_tx.csv")
        self.processor.delete_file(f"{self.dataset}_schema.csv")

        # Close database connection
        db.close()

    def process_utm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converts UTM to lat/lon if applicable, then applies WGS 1984 transformation."""
    
        print("Running process_utm() for", self.dataset)

        # Step 1️⃣: Convert UTM to lat/lon if UTM columns exist
        if any("utm" in col.lower() for col in df.columns):
            df = self.processor.process_utm(df)
            print("After UTM to lat/lon conversion:")
            print(df.head())  # ✅ Should now have _lat and _lon columns

        # Step 2️⃣: Convert lat/lon to WGS 1984 if those columns exist
        lat_lon_found = False
        for lat_col, lon_col in self.lat_lon_pairs:
            if lat_col in df.columns and lon_col in df.columns:
                print(f"Converting {lat_col}, {lon_col} to WGS84...")
                df = self.transformer.transform_coordinates(df, lat_col, lon_col)
                lat_lon_found = True

        if lat_lon_found:
            print("After WGS 1984 conversion:")
            print(df.head())  # ✅ Should now have _wgs84 columns

        return df  # ✅ Now contains UTM lat/lon and WGS 1984 lat/lon

    def transform_coordinates(self, row):
        """Converts lat/lon to WGS84 format if valid."""
        for lat_col, lon_col in self.lat_lon_pairs:
            if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
                coords = {lat_col: [row[lat_col]], lon_col: [row[lon_col]]}
                transformed = self.transformer.transform_coordinates(coords, lat_col, lon_col)
                row[lat_col], row[lon_col] = transformed[f"{lat_col}_wgs84"].iloc[0], transformed[f"{lon_col}_wgs84"].iloc[0]
        return row

    def upload_to_datadotworld(self, df: pd.DataFrame):
        """Uploads dataset and schema to Data.World."""
        csv_file = f"{self.dataset}_tx.csv"
        schema_file = f"{self.dataset}_schema.csv"

        # Save to CSV
        df.to_csv(csv_file, index=False)
        DDW(files=[csv_file], owner_id="aragaocb").upload_to_dataset(self.datadotworld_project)

        # Save schema
        schema_df = self.processor.execute(f"SELECT * FROM {self.dataset}_schema").fetchdf()
        schema_df.to_csv(schema_file, index=False)
        DDW([schema_file], owner_id="aragaocb").upload_to_dataset(self.datadotworld_project)
