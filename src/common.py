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
            cls._instance.con = duckdb.connect('ddb/opsanal.db')
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
            data = json.load(file)['data']
        return pd.DataFrame(data)

    def process_all_files(self):
        parent_dir = self.current_dir / ".." / "opsanal" / self.dataset
        for subdir in ["columns", "tables", "schema"]:
            subdir_path = parent_dir / subdir
            if subdir_path.exists():
                for file in subdir_path.glob("*.json"):
                    df = self.get_json_data(subdir, file.stem).astype(str)
                    table_name = f"{self.dataset}_{file.stem}"
                    self.db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
                    print(f"Processed {file.stem} in {subdir}")
