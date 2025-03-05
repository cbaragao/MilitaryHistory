import requests
from pathlib import Path
import pandas as pd
import json
from common import Common

class Nara:
    """Handles downloading and processing files from the National Archives."""

    def __init__(self, dataset: str):
        self.dataset = dataset.lower()
        self.current_dir = Path(__file__).parent
        self.definition = self.get_links()
        self.data_dir = self.current_dir / ".." / "opsanal" / self.dataset / "data"

    def get_links(self):
        json_path = self.current_dir / "config" / "datasets.json"
        with json_path.open('r') as file:
            return json.load(file)["data"][0][self.dataset]

    def download_file(self):
        """Download the dataset file if available online."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.data_dir / self.definition["file_name"]

        response = requests.get(self.definition["url"], stream=True)
        response.raise_for_status()
        
        with file_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return file_path

    def read_file(self, file_path: str, widths) -> pd.DataFrame:
        """Reads the downloaded file using appropriate delimiter or column widths."""
        delimiter_map = {"pipe": "|", "tab": "\t", "width": None}
        delimiter = delimiter_map.get(self.definition["delimiter"], None)
        
        if delimiter:
            return pd.read_csv(file_path, delimiter=delimiter, header=None, skiprows=1)
        return pd.read_fwf(file_path, widths=widths, header=None).astype(str)

    def rename_columns(self, df: pd.DataFrame):
        schema = Common(dataset=self.dataset).get_json_data("schema", "schema")
        df.columns = schema['id'].tolist()
        return df

    def get_file(self) -> pd.DataFrame:
        """Download and process the dataset file if available."""
        if self.definition["available_online"]:
            file_path = self.download_file()
            df = self.read_file(file_path, self.get_widths())
            return self.rename_columns(df)
        return pd.DataFrame()

    def get_widths(self) -> list:
        """Retrieve column widths from schema."""
        return Common(dataset=self.dataset).get_json_data("schema", "schema")['length'].tolist()
