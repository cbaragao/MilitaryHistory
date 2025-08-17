import json
import duckdb
import pandas as pd
from pathlib import Path


class Database:
    """Singleton database connection for DuckDB."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            current_dir = Path(__file__).resolve().parent
            db_dir = current_dir / 'ddb'
            db_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
            db_path = db_dir / 'opsanal.db'
            cls._instance.con = duckdb.connect(str(db_path))
        return cls._instance

    def execute(self, query: str) -> pd.DataFrame:
        return self.con.execute(query).fetchdf()

    def close(self):
        self.con.close()


class Common:
    """Handles JSON data extraction and table creation in DuckDB."""
    
    def __init__(self, dataset: str):
        self.dataset = dataset.lower()
        self.current_dir = Path(__file__).parent
        self.db = Database()

    def get_json_data(self, subdir: str, name: str) -> pd.DataFrame:
        json_path = self.current_dir / ".." / "opsanal" / self.dataset / subdir / f"{name.lower()}.json"
        with json_path.open('r') as file:
            json_data = json.load(file)
            data = json_data.get('data', [])
            if not data:
                print(f"Warning: No data found in {json_path}")
                return pd.DataFrame()
        return pd.DataFrame(data)

    def process_all_files(self):
        parent_dir = self.current_dir / ".." / "opsanal" / self.dataset
        for subdir in ["columns", "tables", "schema"]:
            subdir_path = parent_dir / subdir
            if subdir_path.exists():
                for file in subdir_path.glob("*.json"):
                    try:
                        df = self.get_json_data(subdir, file.stem)
                        if df.empty:
                            print(f"Skipping empty file: {file.stem} in {subdir}")
                            continue
                        df = df.astype(str)
                        table_name = f"{self.dataset}_{file.stem}"
                        
                        # Register the DataFrame with DuckDB before using it in a query
                        self.db.con.register('df_temp', df)
                        
                        # Use the registered name in the SQL query
                        self.db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df_temp")
                        print(f"Processed {file.stem} in {subdir}")
                    except Exception as e:
                        print(f"Error processing {file.stem} in {subdir}: {e}")
                        continue
