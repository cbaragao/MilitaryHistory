#!/usr/bin/env python3
"""
NARA Catalog API Data Fetcher
Retrieves information for National Archives Identifier 644345
and saves it as a structured CSV file.

Author: Generated for Military History Project
Date: August 18, 2025
"""

import requests
import json
import csv
import pandas as pd
from datetime import datetime
import os
import sys
import toml
import re

def load_config():
    """Load configuration from settings.toml file."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the config directory: ../../../src/config/settings.toml
    config_path = os.path.join(script_dir, '..', '..', '..', 'src', 'config', 'settings.toml')
    config_path = os.path.abspath(config_path)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = toml.load(f)
            print(f"✅ Loaded configuration from {config_path}")
            return config
        except Exception as e:
            print(f"⚠️  Warning: Could not load config from {config_path}: {e}")
            return {}
    else:
        print(f"⚠️  Warning: Config file not found at {config_path}")
        return {}

class NARACatalogFetcher:
    """Fetches data from the NARA Catalog API for a specific identifier."""
    
    def __init__(self, api_key=None):
        """
        Initialize the NARA Catalog API fetcher.
        
        Args:
            api_key (str, optional): API key for NARA Catalog API v2. 
                                   Note: API v2 requires an API key for access.
        """
        self.base_url = "https://catalog.archives.gov/api/v2/"
        self.session = requests.Session()
        
        # Set up headers with API key if provided
        if api_key:
            self.session.headers.update({
                'User-Agent': 'MilitaryHistory-Research-Project/1.0',
                'Accept': 'application/json',
                'x-api-key': api_key
            })
        else:
            self.session.headers.update({
                'User-Agent': 'MilitaryHistory-Research-Project/1.0',
                'Accept': 'application/json'
            })
            print("⚠️  Warning: No API key provided. API v2 may require an API key for access.")
            print("   Contact Catalog_API@nara.gov for an API key if requests fail.")
    
    def get_records_by_parent_naid(self, parent_naid):
        """
        Fetch records using the parentNaId endpoint (API v2).
        
        Args:
            parent_naid (str/int): Parent National Archives Identifier
            
        Returns:
            dict: JSON response from NARA API v2
        """
        url = f"{self.base_url}records/parentNaId/{parent_naid}"
        
        try:
            print(f"Fetching records for Parent NAID: {parent_naid}")
            print(f"API URL: {url}")
            
            response = self.session.get(url, timeout=30)
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response content length: {len(response.content)}")
            print(f"First 500 chars of response: {response.text[:500]}")
            
            response.raise_for_status()
            
            if response.content.strip():
                data = response.json()
                print(f"✅ Successfully retrieved records for Parent NAID {parent_naid}")
                return data
            else:
                print(f"❌ Empty response from API for Parent NAID {parent_naid}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching records for Parent NAID {parent_naid}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            print(f"Raw response content: {response.text}")
            return None
    
    def search_by_naid(self, naid):
        """
        Alternative method: Search for records using the search API v2.
        
        Args:
            naid (str/int): National Archives Identifier
            
        Returns:
            dict: JSON response from NARA search API v2
        """
        search_url = f"{self.base_url}search"
        params = {
            'naIds': naid,
            'resultTypes': 'item',
            'sort': 'naIdSort asc'
        }
        
        try:
            print(f"Trying search API v2 for NAID: {naid}")
            print(f"Search URL: {search_url}")
            print(f"Parameters: {params}")
            
            response = self.session.get(search_url, params=params, timeout=30)
            print(f"Search response status code: {response.status_code}")
            print(f"Search response content length: {len(response.content)}")
            print(f"First 500 chars of search response: {response.text[:500]}")
            
            response.raise_for_status()
            
            if response.content.strip():
                data = response.json()
                print(f"✅ Successfully retrieved search data for NAID {naid}")
                return data
            else:
                print(f"❌ Empty response from search API for NAID {naid}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching for NAID {naid}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing search JSON response: {e}")
            print(f"Raw search response content: {response.text}")
            return None
    
    def flatten_json_response(self, record_data):
        """
        Flatten the nested JSON structure into a tabular format.
        
        Args:
            record_data (dict): Raw JSON data from NARA API
            
        Returns:
            list: List of flattened records
        """
        flattened_records = []
        
        def extract_value(obj, key, default=""):
            """Helper function to safely extract values from nested objects."""
            if isinstance(obj, dict):
                return obj.get(key, default)
            elif isinstance(obj, list) and len(obj) > 0:
                return obj[0].get(key, default) if isinstance(obj[0], dict) else str(obj[0])
            else:
                return str(obj) if obj is not None else default
        
        def flatten_object(obj, parent_key="", separator="_"):
            """Recursively flatten nested dictionaries and lists."""
            items = []
            
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent_key}{separator}{k}" if parent_key else k
                    if isinstance(v, (dict, list)):
                        items.extend(flatten_object(v, new_key, separator).items())
                    else:
                        items.append((new_key, v))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_key = f"{parent_key}{separator}{i}" if parent_key else str(i)
                    if isinstance(item, (dict, list)):
                        items.extend(flatten_object(item, new_key, separator).items())
                    else:
                        items.append((new_key, item))
            else:
                items.append((parent_key, obj))
            
            return dict(items)
        
        # Check for v2 API response format first
        if record_data and 'body' in record_data:
            # v2 API format: body.hits.hits
            hits = record_data.get('body', {}).get('hits', {}).get('hits', [])
            
            for hit in hits:
                # Extract the source record
                source_record = hit.get('_source', {}).get('record', {})
                
                # Flatten the entire source record
                flattened = flatten_object(source_record)
                
                # Add metadata from the hit
                flattened['_index'] = hit.get('_index', '')
                flattened['_id'] = hit.get('_id', '')
                flattened['_score'] = hit.get('_score', '')
                flattened['fetch_timestamp'] = datetime.now().isoformat()
                flattened['api_source'] = 'NARA Catalog API v2'
                
                flattened_records.append(flattened)
                
        # Fallback to legacy v1 API format
        elif record_data and 'opaResponse' in record_data:
            # v1 API format: opaResponse.results
            results = record_data.get('opaResponse', {}).get('results', [])
            
            for result in results:
                # Flatten the entire result object
                flattened = flatten_object(result)
                
                # Add metadata
                flattened['fetch_timestamp'] = datetime.now().isoformat()
                flattened['api_source'] = 'NARA Catalog API v1'
                
                flattened_records.append(flattened)
        
        return flattened_records
    
    def parse_battalion_table(self, text_content):
        """
        Parse the battalion tracking table from the extracted text.
        
        Args:
            text_content (str): Raw text content containing the table
            
        Returns:
            list: List of dictionaries containing table data
        """
        battalion_data = []
        
        # Look for the specific table pattern in the text
        # Pattern: RG335.BNTRK.BN## followed by LRECL and Unit description
        pattern = r'RG335\.BNTRK\.BN\w+\s+(\d+)\s+(.+?)(?=\nRG335\.BNTRK\.BN|\nReproducer|\nReference|\nTwo versions|$)'
        
        matches = re.findall(pattern, text_content, re.MULTILINE | re.DOTALL)
        
        # Also look for the file names separately
        file_pattern = r'(RG335\.BNTRK\.BN\w+)'
        file_matches = re.findall(file_pattern, text_content)
        
        # Process the text line by line to capture the table structure
        lines = text_content.split('\n')
        current_file = None
        current_lrecl = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if this line contains a data file name
            if line.startswith('RG335.BNTRK.BN'):
                current_file = line
                # Look ahead for LRECL and unit description
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # Check if next line is a number (LRECL)
                    if next_line.isdigit():
                        current_lrecl = int(next_line)
                        # Look for unit description
                        if i + 2 < len(lines):
                            unit_line = lines[i + 2].strip()
                            if unit_line and not unit_line.startswith('RG335') and not unit_line.isdigit():
                                # Clean up unit description
                                unit_description = unit_line
                                # Handle multi-line unit descriptions
                                j = i + 3
                                while j < len(lines) and not lines[j].strip().startswith('RG335') and not lines[j].strip().isdigit() and lines[j].strip():
                                    if not lines[j].strip().startswith('Reference') and not lines[j].strip().startswith('Reproduc'):
                                        unit_description += ' ' + lines[j].strip()
                                    j += 1
                                
                                battalion_data.append({
                                    'data_file_name': current_file,
                                    'lrecl': current_lrecl,
                                    'unit': unit_description
                                })
        
        return battalion_data
    
    def save_raw_text(self, record_data, output_path):
        """
        Save raw text content from digital objects to a text file.
        
        Args:
            record_data (dict): Raw JSON data from NARA API
            output_path (str): Path to save the text file
        """
        try:
            all_text = []
            
            if record_data and 'body' in record_data:
                hits = record_data.get('body', {}).get('hits', {}).get('hits', [])
                
                for hit in hits:
                    source_record = hit.get('_source', {}).get('record', {})
                    digital_objects = source_record.get('digitalObjects', [])
                    
                    for obj in digital_objects:
                        if 'completeExtractedText' in obj:
                            text = obj['completeExtractedText']
                            if text:
                                all_text.append(f"=== {obj.get('objectDescription', 'Digital Object')} ===\n")
                                all_text.append(text)
                                all_text.append("\n" + "="*80 + "\n")
            
            if all_text:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(all_text))
                print(f"✅ Raw text content saved to {output_path}")
                return True
            else:
                print("⚠️  No text content found to save")
                return False
                
        except Exception as e:
            print(f"❌ Error saving raw text: {e}")
            return False
    
    def save_battalion_table(self, battalion_data, output_path):
        """
        Save parsed battalion table data to CSV.
        
        Args:
            battalion_data (list): List of battalion data dictionaries
            output_path (str): Path to save the CSV file
        """
        if not battalion_data:
            print("❌ No battalion data to save")
            return False
        
        try:
            df = pd.DataFrame(battalion_data)
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"✅ Battalion table saved to {output_path}")
            print(f"📊 Battalion Table Summary:")
            print(f"   • Records: {len(battalion_data)}")
            print(f"   • LRECL values: {sorted(df['lrecl'].unique())}")
            print(f"   • File size: {os.path.getsize(output_path):,} bytes")
            
            # Show sample entries
            print(f"\n📝 Sample Entries:")
            for i, row in df.head(5).iterrows():
                print(f"   {i+1}. {row['data_file_name']} (LRECL: {row['lrecl']}) - {row['unit'][:50]}{'...' if len(row['unit']) > 50 else ''}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving battalion table: {e}")
            return False
    
    def save_to_csv(self, records, output_path):
        """
        Save flattened records to CSV file.
        
        Args:
            records (list): List of flattened record dictionaries
            output_path (str): Path to save the CSV file
        """
        if not records:
            print("❌ No records to save")
            return
        
        try:
            # Create DataFrame
            df = pd.DataFrame(records)
            
            # Sort columns for better readability
            priority_columns = [
                'naId', 'title', 'description_description', 'productionDate_logicalDate',
                'creators_creator_name', 'locationIds_locationId', 'type',
                'fetch_timestamp', 'api_source'
            ]
            
            # Get all columns
            all_columns = list(df.columns)
            
            # Reorder columns: priority columns first, then the rest
            ordered_columns = []
            for col in priority_columns:
                if col in all_columns:
                    ordered_columns.append(col)
                    all_columns.remove(col)
            
            # Add remaining columns
            ordered_columns.extend(sorted(all_columns))
            
            # Reorder DataFrame
            df = df[ordered_columns]
            
            # Save to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"✅ Successfully saved {len(records)} records to {output_path}")
            
            # Print summary statistics
            print(f"\n📊 Dataset Summary:")
            print(f"   • Records: {len(records)}")
            print(f"   • Columns: {len(df.columns)}")
            print(f"   • File size: {os.path.getsize(output_path):,} bytes")
            
            # Show first few column names
            print(f"\n📝 Key Columns (first 10):")
            for i, col in enumerate(ordered_columns[:10]):
                sample_value = df[col].iloc[0] if len(df) > 0 else "N/A"
                print(f"   {i+1:2d}. {col}: {str(sample_value)[:50]}{'...' if len(str(sample_value)) > 50 else ''}")
            
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
    
    def fetch_and_save(self, naid, output_dir):
        """
        Main method to fetch data and save to CSV.
        
        Args:
            naid (str/int): National Archives Identifier
            output_dir (str): Directory to save the output file
        """
        # Try direct ID lookup first
        print("🔍 Attempting direct parent NAID lookup...")
        record_data = self.get_records_by_parent_naid(naid)
        
        # If that fails, try search API
        if not record_data:
            print("🔍 Attempting search API lookup...")
            record_data = self.search_by_naid(naid)
        
        if not record_data:
            print("❌ Failed to fetch data from NARA API using both methods")
            return False
        
        # Flatten the data
        flattened_records = self.flatten_json_response(record_data)
        
        if not flattened_records:
            print("❌ No records found in the response")
            return False
        
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nara_catalog_{naid}_{timestamp}.csv"
        output_path = os.path.join(output_dir, filename)
        
        # Save to CSV
        self.save_to_csv(flattened_records, output_path)
        
        # Extract and save raw text content
        text_filename = f"nara_catalog_{naid}_{timestamp}_text.txt"
        text_path = os.path.join(output_dir, text_filename)
        self.save_raw_text(record_data, text_path)
        
        # Parse and save battalion table data
        print("\n🔍 Parsing battalion table data...")
        all_text = ""
        
        # Extract all text content for parsing
        if record_data and 'body' in record_data:
            hits = record_data.get('body', {}).get('hits', {}).get('hits', [])
            for hit in hits:
                source_record = hit.get('_source', {}).get('record', {})
                digital_objects = source_record.get('digitalObjects', [])
                for obj in digital_objects:
                    if 'completeExtractedText' in obj and obj['completeExtractedText']:
                        all_text += obj['completeExtractedText'] + "\n"
        
        # Parse the battalion table
        battalion_data = self.parse_battalion_table(all_text)
        
        if battalion_data:
            # Save battalion table CSV
            battalion_filename = f"nara_battalion_table_{naid}_{timestamp}.csv"
            battalion_path = os.path.join(output_dir, battalion_filename)
            self.save_battalion_table(battalion_data, battalion_path)
        else:
            print("⚠️  No battalion table data found in extracted text")
        
        # Also save raw JSON for reference
        json_filename = f"nara_catalog_{naid}_{timestamp}_raw.json"
        json_path = os.path.join(output_dir, json_filename)
        
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(record_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Raw JSON data saved to {json_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not save raw JSON: {e}")
        
        return True

def main():
    """Main execution function."""
    print("🏛️  NARA Catalog API Data Fetcher")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Get API key from config
    api_key = None
    if 'nara' in config and 'api_key' in config['nara']:
        api_key = config['nara']['api_key']
        print(f"🔑 Using API key from configuration")
    else:
        print("⚠️  No API key found in configuration")
    
    # Configuration
    naid = "644345"
    output_dir = "/home/chris/Documents/MilitaryHistory/opsanal/battalion/catalog"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize fetcher with API key and execute
    fetcher = NARACatalogFetcher(api_key=api_key)
    success = fetcher.fetch_and_save(naid, output_dir)
    
    if success:
        print(f"\n✅ Data fetch completed successfully!")
        print(f"📁 Output saved to: {output_dir}")
    else:
        print(f"\n❌ Data fetch failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
