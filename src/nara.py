import requests
from pathlib import Path
import pandas as pd
import json
import zipfile
import tempfile
import re
import duckdb
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
        """Download the dataset file if available online, or reuse existing file."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.data_dir / self.definition["file_name"]

        # Check if file already exists
        if file_path.exists():
            print(f"Using existing file: {file_path}")
            # Check if this is a zip file that needs extraction
            if self.definition.get("is_zipped", False) and file_path.suffix.lower() == ".zip":
                return self._extract_zip_file(file_path)
            return file_path
        
        # File doesn't exist, download it
        print(f"Downloading {self.definition['file_name']} from {self.definition['url']}")
        response = requests.get(self.definition["url"], stream=True)
        response.raise_for_status()
        
        with file_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download completed: {file_path}")
        
        # Check if this is a zip file that needs extraction
        if self.definition.get("is_zipped", False) and file_path.suffix.lower() == ".zip":
            return self._extract_zip_file(file_path)
        
        return file_path

    def _extract_zip_file(self, zip_path: Path):
        """Extract zip file and return path to the main data file, or reuse existing extraction."""
        extract_dir = zip_path.parent / f"{zip_path.stem}_extracted"
        
        # Check if extraction directory already exists with files
        if extract_dir.exists() and any(extract_dir.iterdir()):
            print(f"Using existing extracted files from: {extract_dir}")
            # Find the main data file in the existing extracted contents
            return self._find_main_data_file(extract_dir, zip_path)
        
        # Extract directory doesn't exist or is empty, perform extraction
        print(f"Extracting {zip_path.name} to {extract_dir}")
        extract_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        print(f"Extraction completed: {extract_dir}")
        
        # Find the main data file in the extracted contents
        return self._find_main_data_file(extract_dir, zip_path)
    
    def _find_main_data_file(self, extract_dir: Path, zip_path: Path):
        """Find the main data file in extracted contents."""
        # Look for common data file patterns
        data_extensions = ['.dat', '.txt', '.csv', '.tsv']
        extracted_files = list(extract_dir.glob("*"))
        
        # First, try to find files with data extensions
        for ext in data_extensions:
            data_files = list(extract_dir.glob(f"*{ext}"))
            if data_files:
                # Return the largest file (likely the main dataset)
                main_file = max(data_files, key=lambda f: f.stat().st_size)
                print(f"Using main data file: {main_file}")
                return main_file
        
        # If no data extension files found, return the largest file
        if extracted_files:
            main_file = max(extracted_files, key=lambda f: f.stat().st_size if f.is_file() else 0)
            print(f"Using largest file as main data file: {main_file}")
            return main_file
        
        raise FileNotFoundError(f"No data files found in zip archive: {zip_path}")

    def detect_encoding(self, file_path: str) -> str:
        """Intelligently detect file encoding by sampling content."""
        try:
            # First, try to read a small sample with UTF-8
            with open(file_path, 'rb') as f:
                sample = f.read(1024)  # Read first 1KB
            
            # Check if it's likely EBCDIC by looking for common EBCDIC patterns
            # EBCDIC files often have high byte values and specific patterns
            high_bytes = sum(1 for b in sample if b > 127)
            total_bytes = len(sample)
            
            if total_bytes > 0 and (high_bytes / total_bytes) > 0.3:
                # Likely EBCDIC - try EBCDIC encodings first
                return "ebcdic_priority"
            else:
                # Likely standard text - try standard encodings first
                return "standard_priority"
                
        except Exception:
            # If detection fails, default to standard priority
            return "standard_priority"
    
    def read_file(self, file_path: str, widths) -> pd.DataFrame:
        """Reads the downloaded file using appropriate delimiter or column widths."""
        delimiter_map = {"pipe": "|", "tab": "\t", "comma": ",", "width": None}
        delimiter = delimiter_map.get(self.definition["delimiter"], None)
        
        # Intelligently choose encoding order based on file content
        encoding_priority = self.detect_encoding(file_path)
        
        if encoding_priority == "ebcdic_priority":
            # Try EBCDIC encodings first for mainframe data
            encodings_to_try = ['cp037', 'cp500', 'cp1140', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        else:
            # Try standard encodings first for modern data
            encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'cp037', 'cp500', 'cp1140']
        
        if delimiter:
            for encoding in encodings_to_try:
                try:
                    return pd.read_csv(file_path, delimiter=delimiter, header=None, skiprows=1, encoding=encoding)
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Could not read file {file_path} with any supported encoding")
        else:
            # For fixed-width files with no line terminators, handle specially
            for encoding in encodings_to_try:
                try:
                    # Check if file has line terminators
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read(1000)  # Read first 1000 chars to check
                        if '\n' in content or '\r' in content:
                            # Normal fixed width file
                            return pd.read_fwf(file_path, widths=widths, header=None, encoding=encoding).astype(str)
                        else:
                            # File with no line terminators - need to split manually
                            f.seek(0)
                            full_content = f.read()
                            record_length = sum(widths)
                            
                            # Split into records
                            records = []
                            for i in range(0, len(full_content), record_length):
                                record = full_content[i:i + record_length]
                                if len(record) == record_length:  # Only complete records
                                    # Split record into fields based on widths
                                    fields = []
                                    start = 0
                                    for width in widths:
                                        fields.append(record[start:start + width].strip())
                                        start += width
                                    records.append(fields)
                            
                            if records:
                                return pd.DataFrame(records).astype(str)
                            else:
                                return pd.DataFrame()
                                
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Could not read file {file_path} with any supported encoding")

    def rename_columns(self, df: pd.DataFrame):
        schema = Common(dataset=self.dataset).get_json_data("schema", "schema")
        # Only include FIELD type entries, exclude GROUP entries
        field_rows = schema[schema['field_group'] == 'FIELD']
        df.columns = field_rows['id'].tolist()
        return df

    def get_file(self) -> pd.DataFrame:
        """Download and process the dataset file if available."""
        if self.definition["available_online"]:
            file_path = self.download_file()
            
            # Handle CSV files differently from fixed-width files
            if self.definition["delimiter"] == "comma":
                # For CSV files, read with headers and clean column names
                # Read all columns as strings to match fixed-width file behavior
                df = pd.read_csv(file_path, encoding='utf-8', dtype=str)
                # Clean column names: remove extra spaces and special characters
                df.columns = [col.strip().lstrip('+').strip() for col in df.columns]
                return df
            else:
                # For fixed-width files, use schema-based processing
                df = self.read_file(file_path, self.get_widths())
                return self.rename_columns(df)
        return pd.DataFrame()

    def get_widths(self) -> list:
        """Retrieve column widths from schema."""
        schema_df = Common(dataset=self.dataset).get_json_data("schema", "schema")
        # Only include FIELD type entries, exclude GROUP entries
        field_rows = schema_df[schema_df['field_group'] == 'FIELD']
        lengths = field_rows['length'].tolist()
        return [int(length) for length in lengths if length is not None]
    
    def load_lookup_tables(self, conn: duckdb.DuckDBPyConnection):
        """Load lookup tables into DuckDB for joins (supports AIMS and PSYOPSA)."""
        dataset_lower = self.dataset.lower()
        
        if dataset_lower == 'aims':
            self._load_aims_lookup_tables(conn)
        elif dataset_lower.startswith('psyopsa'):
            self._load_psyopsa_lookup_tables(conn)
        # Add more datasets as needed
        
    def _load_aims_lookup_tables(self, conn: duckdb.DuckDBPyConnection):
        """Load AIMS lookup tables from tab-delimited files."""
        docs_dir = self.current_dir / ".." / "opsanal" / self.dataset / "docs"
        # Get all AIMS lookup files but exclude documentation files (.DOC)
        lookup_files = [f for f in docs_dir.glob("AIMS.8804.CD.*") if not f.name.upper().endswith('.DOC')]
        
        for lookup_file in lookup_files:
            table_suffix = lookup_file.name.split('.')[-1].lower()
            table_name = f"aims_lookup_{table_suffix}"
            
            print(f"Loading lookup table: {table_name} from {lookup_file.name}")
            
            try:
                with open(lookup_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                lookup_data = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse tab-delimited format: CODE\tDESCRIPTION
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        code = parts[0].strip()
                        description = parts[1].strip()
                        if code and description:
                            lookup_data.append({'code': code, 'description': description})
                    elif len(parts) == 1:
                        # Handle single-column entries (code only)
                        code = parts[0].strip()
                        if code:
                            lookup_data.append({'code': code, 'description': code})
                
                if lookup_data:
                    # Create lookup table in DuckDB
                    lookup_df = pd.DataFrame(lookup_data)
                    
                    # Drop table if exists and create new one
                    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM lookup_df")
                    
                    print(f"Created lookup table {table_name} with {len(lookup_data)} entries")
                else:
                    print(f"No valid entries found in {lookup_file.name}")
                    
            except Exception as e:
                print(f"Error loading lookup table {lookup_file.name}: {e}")
                continue
                
    def _load_psyopsa_lookup_tables(self, conn: duckdb.DuckDBPyConnection):
        """Load PSYOPSA lookup tables from JSON files."""
        tables_dir = self.current_dir / ".." / "opsanal" / "psyopsa" / "tables"
        
        if not tables_dir.exists():
            print("PSYOPSA tables directory not found")
            return
        
        # Map filename to expected table suffix in SQL files
        file_to_table_mapping = {
            'conducting_agency.json': 'conag',
            'reporting_unit.json': 'report',  # Used in ps1, but also 'repunit' in ps2
            'operation_codes.json': 'op',
            'campaign_codes.json': 'campn',
            'theme_codes.json': 'them',
            'subtheme_codes.json': 'sthem',
            'audience_codes.json': 'aud'
        }
        
        # Get all JSON lookup files
        lookup_files = list(tables_dir.glob("*.json"))
        
        for lookup_file in lookup_files:
            # Get the expected table suffix from mapping
            table_suffix = file_to_table_mapping.get(lookup_file.name, lookup_file.stem)
            table_name = f"psyopsa_lookup_{table_suffix}"
            
            print(f"Loading lookup table: {table_name} from {lookup_file.name}")
            
            try:
                with open(lookup_file, 'r', encoding='utf-8') as f:
                    lookup_json = json.load(f)
                
                # Extract data array from JSON structure
                if 'data' in lookup_json and isinstance(lookup_json['data'], list):
                    lookup_data = []
                    for item in lookup_json['data']:
                        if isinstance(item, dict) and 'code' in item and 'value' in item:
                            lookup_data.append({
                                'code': str(item['code']).strip(),
                                'description': str(item['value']).strip()
                            })
                    
                    if lookup_data:
                        # Create lookup table in DuckDB
                        lookup_df = pd.DataFrame(lookup_data)
                        
                        # Drop table if exists and create new one
                        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM lookup_df")
                        
                        print(f"Created lookup table {table_name} with {len(lookup_data)} entries")
                        
                        # For reporting_unit, also create the 'repunit' alias used in ps2
                        if table_suffix == 'report':
                            repunit_table_name = "psyopsa_lookup_repunit"
                            conn.execute(f"DROP TABLE IF EXISTS {repunit_table_name}")
                            conn.execute(f"CREATE TABLE {repunit_table_name} AS SELECT * FROM lookup_df")
                            print(f"Created alias table {repunit_table_name} with {len(lookup_data)} entries")
                        
                    else:
                        print(f"No valid entries found in {lookup_file.name}")
                else:
                    print(f"Invalid JSON structure in {lookup_file.name}")
                    
            except Exception as e:
                print(f"Error loading lookup table {lookup_file.name}: {e}")
                continue
