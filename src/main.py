import pandas as pd
from pathlib import Path
from common import Database, Common
from nara import Nara
import duckdb
import os
from utmconverter import UTMConverter

class Main:
    """Main class to process data from multiple sources."""

    def __init__(self, dataset: str):
        self.dataset = dataset.lower()
        current_dir = Path(__file__).resolve().parent
        db_path = current_dir / 'ddb' / 'opsanal.db'
        self.db = duckdb.connect(str(db_path))
        self.utm_converter = UTMConverter()

    def process_all_files(self):
        """Process JSON files and return database connection."""
        c = Common(self.dataset)
        c.process_all_files()
        return c

    def get_nara(self):
        """Retrieve data from NARA and return as DataFrame."""
        nara = Nara(self.dataset)
        return nara.get_file()
    
    def process_utm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Delegates UTM processing to UTMConverter."""
        return self.utm_converter.process_utm(df)  # ✅ Cleaner & reusable

    def create_base_tables(self):
        """Creates base tables in DuckDB with JSON and NARA data."""
        self.process_all_files()
        nara_df = self.get_nara()

        self.db.execute(f"DROP TABLE IF EXISTS {self.dataset}_nara")
        self.db.execute(f"CREATE TABLE {self.dataset}_nara AS SELECT * FROM nara_df")
        
        return self.db
    def get_sql(self):
        """Reads the dataset-specific SQL file and returns the query as a string."""
        current_dir = os.path.dirname(__file__)
        sql_path = os.path.join(current_dir, "sql/opsanal", f"{self.dataset}.sql")

        if not os.path.exists(sql_path):
            raise FileNotFoundError(f"SQL file not found: {sql_path}")

        with open(sql_path, "r") as file:
            query = file.read()
        
        return query  # ✅ Return the SQL query

    def execute(self, query: str) -> pd.DataFrame:
        """Execute a SQL query in DuckDB."""
        return self.db.execute(query)

    def delete_file(self, file: Path):
        """Delete a file if it exists."""
        file_path = Path(file)
        if file_path.exists():
            file_path.unlink()
            print(f"{file} has been deleted.")
        else:
            print(f"{file} does not exist.")
