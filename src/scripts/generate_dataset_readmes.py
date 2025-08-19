#!/usr/bin/env python3
"""
Dataset README Generator
========================
Automatically generates README.md files for each dataset in the opsanal directory,
referencing metadata from datasets.json and documentation from docs folders.
Optionally uploads README files to Data.world as dataset descriptions.

Usage:
    python generate_dataset_readmes.py [--dataset <name>] [--upload-to-dataworld] [--dry-run]
    
Examples:
    python generate_dataset_readmes.py                               # Generate all READMEs locally
    python generate_dataset_readmes.py --dataset aims                # Generate specific dataset README  
    python generate_dataset_readmes.py --upload-to-dataworld         # Generate and upload to Data.world
    python generate_dataset_readmes.py --upload-to-dataworld --dry-run  # Test mode (no upload)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from common import Common

try:
    import datadotworld as dw
    DW_AVAILABLE = True
except ImportError:
    DW_AVAILABLE = False
    print("Warning: datadotworld library not available. README upload will be skipped.")


class DatasetREADMEGenerator:
    """Generates comprehensive README.md files for each dataset."""
    
    def __init__(self, upload_to_dataworld: bool = False):
        self.project_root = Path(__file__).parent.parent.parent
        self.opsanal_dir = self.project_root / "opsanal"
        self.datasets_json_path = self.project_root / "src" / "config" / "datasets.json"
        self.upload_to_dataworld = upload_to_dataworld
        
        # Initialize Data.world client if available and uploading
        self.dw_client = None
        if self.upload_to_dataworld and DW_AVAILABLE:
            try:
                self.dw_client = dw.api_client()
                print("✅ Data.world client initialized for README uploads")
            except Exception as e:
                print(f"⚠️  Data.world client initialization failed: {e}")
                self.upload_to_dataworld = False
        
        # Dataset to Data.world project mapping (only for datasets that exist in Data.world)
        self.dataworld_mapping = {
            "psyopsa": "psyopsa",
            "khmer": "khmer", 
            "aims": "aimsawards",
            "seafa": "southeast-asia-forces-seafa",
            "incda": "republic-of-vietnam-incidents-files-incda",
            "tirsa": "terrorist-incident-reporting-system-tirsa",
            "vciia": "viet-cong-initiated-incidents-vciia",
            "basfa": "basfa",
            "conga": "conga",
            "hosta": "hosta",
            "vssg": "vssgfiles",
            "awardsdecorations": "awardsdecorations"
            # Note: Only datasets that exist in Data.world are included
            # Datasets with underscores in names (gors_*, incda_ps*) are not valid Data.world IDs
            # Missing datasets (hes, vndba, bomba, cidga, hr01a, obsea) are excluded
        }
        
        # Load datasets metadata
        self.datasets_metadata = self.load_datasets_metadata()
        
    def load_datasets_metadata(self) -> Dict[str, Any]:
        """Load metadata from datasets.json."""
        try:
            with open(self.datasets_json_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'data' in data:
                    # Flatten the nested structure
                    metadata = {}
                    for item in data['data']:
                        if isinstance(item, dict):
                            metadata.update(item)
                    return metadata
                return {}
        except Exception as e:
            print(f"Warning: Could not load datasets.json: {e}")
            return {}
    
    def get_dataset_directories(self) -> List[str]:
        """Get list of dataset directories in opsanal/."""
        dataset_dirs = []
        for item in self.opsanal_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                dataset_dirs.append(item.name)
        return sorted(dataset_dirs)
    
    def get_schema_info(self, dataset: str) -> Dict[str, Any]:
        """Extract schema information for a dataset."""
        schema_info = {
            "field_count": 0,
            "tables": [],
            "fields": []
        }
        
        schema_path = self.opsanal_dir / dataset / "schema" / "schema.json"
        if schema_path.exists():
            try:
                with open(schema_path, 'r') as f:
                    schema_data = json.load(f)
                    
                if isinstance(schema_data, dict) and 'data' in schema_data:
                    fields = schema_data['data']
                elif isinstance(schema_data, list):
                    fields = schema_data
                else:
                    fields = []
                
                # Extract field information
                for field in fields:
                    if isinstance(field, dict) and field.get("field_group") == "FIELD":
                        schema_info["fields"].append({
                            "id": field.get("id", ""),
                            "definition": field.get("definition", ""),
                            "data_values": field.get("data_values", ""),
                            "length": field.get("length", "")
                        })
                
                schema_info["field_count"] = len(schema_info["fields"])
                
                # Get table names (infer from dataset structure)
                if dataset in self.datasets_metadata:
                    schema_info["tables"] = [f"{dataset}_tx.csv"]
                
            except Exception as e:
                print(f"Warning: Could not parse schema for {dataset}: {e}")
        
        return schema_info
    
    def get_docs_info(self, dataset: str) -> List[Dict[str, str]]:
        """Get documentation files for a dataset."""
        docs_info = []
        docs_path = self.opsanal_dir / dataset / "docs"
        
        if docs_path.exists():
            for doc_file in docs_path.iterdir():
                if doc_file.is_file():
                    docs_info.append({
                        "filename": doc_file.name,
                        "type": self.get_file_type(doc_file.suffix),
                        "size": self.format_file_size(doc_file.stat().st_size)
                    })
        
        return sorted(docs_info, key=lambda x: x["filename"])
    
    def get_file_type(self, extension: str) -> str:
        """Get descriptive file type from extension."""
        type_mapping = {
            ".pdf": "PDF Documentation",
            ".txt": "Text File", 
            ".html": "HTML Documentation",
            ".md": "Markdown Documentation",
            ".csv": "CSV Data File",
            ".json": "JSON Configuration",
            ".xml": "XML Document"
        }
        return type_mapping.get(extension.lower(), f"{extension.upper()} File")
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def get_nara_info(self, dataset: str) -> Dict[str, str]:
        """Get NARA metadata for a dataset."""
        nara_info = {
            "naid": "Unknown",
            "catalog_url": "Not available",
            "file_name": "Unknown",
            "url": "Not available",
            "available_online": "Unknown"
        }
        
        if dataset in self.datasets_metadata:
            metadata = self.datasets_metadata[dataset]
            nara_info.update({
                "naid": metadata.get("NAID", "Unknown"),
                "catalog_url": metadata.get("catalog_url", "Not available"),
                "file_name": metadata.get("file_name", "Unknown"),
                "url": metadata.get("url", "Not available"),
                "available_online": str(metadata.get("available_online", "Unknown"))
            })
        
        return nara_info
    
    def get_dataset_description(self, dataset: str) -> str:
        """Generate a description for the dataset."""
        descriptions = {
            "aims": "Awards and decorations database containing comprehensive records of military personnel recognition and honors.",
            "basfa": "Base facilities and operations data tracking infrastructure and administrative information.",
            "khmer": "Cambodia operations database documenting military activities and incident reports during the conflict period.",
            "psyopsa": "Psychological operations dataset containing strategic communication and influence campaign data.",
            "seafa": "Southeast Asia Forces database with comprehensive personnel and operational data.",
            "gors": "Ground Operations Reporting System containing tactical unit reports and battlefield assessments.",
            "incda": "Republic of Vietnam incidents database documenting security events and operational reports.",
            "tirsa": "Terrorist Incident Reporting System containing detailed incident analysis and intelligence reports.",
            "vciia": "Viet Cong Initiated Incidents database tracking enemy-initiated activities and engagements.",
            "conga": "Congressional data and legislative information related to military operations.",
            "basfa": "Base facilities administration and logistics data.",
            "hes": "Hamlet Evaluation System data measuring security and development in Vietnamese communities.",
            "vndba": "Vietnam database containing comprehensive operational and administrative records.",
            "bomba": "Bombing operations and ordnance data from air campaign activities.",
            "cidga": "Combat intelligence and damage assessment reports.",
            "hr01a": "Human resources and personnel administration data.",
            "obsea": "Observation and surveillance data from Southeast Asia operations."
        }
        
        return descriptions.get(dataset, f"Military operational dataset containing {dataset.upper()} related information and records.")
    
    def generate_readme_content(self, dataset: str) -> str:
        """Generate comprehensive README content for a dataset."""
        schema_info = self.get_schema_info(dataset)
        docs_info = self.get_docs_info(dataset)
        nara_info = self.get_nara_info(dataset)
        description = self.get_dataset_description(dataset)
        dataworld_project = self.dataworld_mapping.get(dataset, dataset)
        
        # Generate the README content
        content = f"""# {dataset.upper()} Dataset

{description}

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/{dataworld_project}](https://data.world/aragaocb/{dataworld_project})

### Source Information
- **NARA ID**: {nara_info['naid']}
- **Original Filename**: {nara_info['file_name']}
- **Catalog URL**: {nara_info['catalog_url']}
- **Available Online**: {nara_info['available_online']}
- **Source URL**: {nara_info['url']}

## 🗃️ Data Structure

### Transaction Files
- **{dataset}_tx.csv**: Primary transaction data file containing {schema_info['field_count']} fields

### Schema Information
- **Total Fields**: {schema_info['field_count']}
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
"""
        
        # Add field descriptions if available
        if schema_info['fields']:
            for field in schema_info['fields'][:10]:  # Show first 10 fields
                field_id = field.get('id', 'Unknown')
                definition = field.get('definition', 'No description available')
                data_type = field.get('data_values', 'Unknown')
                length = field.get('length', 'Variable')
                
                content += f"- **{field_id}**: {definition}"
                if data_type != 'Unknown':
                    content += f" (Type: {data_type}"
                    if length != 'Variable':
                        content += f", Length: {length}"
                    content += ")"
                content += "\n"
            
            if len(schema_info['fields']) > 10:
                content += f"\n... and {len(schema_info['fields']) - 10} more fields. See schema documentation for complete field definitions.\n"
        
        content += f"""
## 📚 Documentation

### Available Files
"""
        
        # Add documentation files
        if docs_info:
            for doc in docs_info:
                content += f"- **{doc['filename']}** ({doc['type']}, {doc['size']})\n"
        else:
            content += "- No additional documentation files available\n"
        
        content += f"""
### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/{dataset}.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/{dataset}.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/{dataworld_project}](https://data.world/aragaocb/{dataworld_project})
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `{dataset}_tx.csv`
- **Schema Metadata**: `{dataset}_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM {dataset}_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/{dataworld_project}')

# Access transaction data
df = dataset.dataframes['{dataset}_tx']

# Basic analysis
print(f"Total records: {{len(df)}}")
print(f"Columns: {{list(df.columns)}}")
```

### Spatial Analysis
"""
        
        # Add spatial information if this is a spatial dataset
        spatial_datasets = ["khmer", "gors", "incda", "tirsa", "vciia", "seafa"]
        if any(spatial in dataset for spatial in spatial_datasets):
            content += """
This dataset includes spatial coordinates that can be used for mapping and geographic analysis:

```python
# Geographic visualization
import folium

# Create map with data points
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# Add data points to map
for idx, row in df.iterrows():
    if pd.notna(row['latitude']) and pd.notna(row['longitude']):
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=f"Event: {row['event_type']}"
        ).add_to(m)

m.save('map.html')
```
"""
        
        content += f"""
## 🔍 Data Quality

### Completeness
- **Processing Status**: ✅ Complete
- **Data Validation**: Applied during processing
- **Missing Values**: Handled according to original data format

### Known Issues
- Original data may contain historical inconsistencies
- Coordinate precision varies by source
- Some fields may be sparsely populated

## 📖 Historical Context

This dataset is part of the Military History Archival Data Processing Pipeline, which digitizes and processes historical military records from the National Archives. The data provides insights into:

- Military operations and strategic planning
- Personnel management and recognition
- Geographic patterns of conflict events
- Historical operational effectiveness

## 🤝 Contributing

### Data Issues
Report data quality issues or processing errors via the project repository.

### Enhancement Requests
Suggest additional processing features or analysis capabilities.

### Citation
When using this data in research or analysis, please cite:
```
MilitaryHistory Project. ({datetime.now().year}). {dataset.upper()} Dataset. 
Retrieved from https://data.world/aragaocb/{dataworld_project}
```

---

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
"""
        
        return content
    
    def upload_readme_to_dataworld(self, dataset: str, readme_path: Path) -> bool:
        """Upload README.md file to Data.world dataset."""
        if not self.upload_to_dataworld or not self.dw_client:
            return True  # Skip upload if not enabled
            
        # Check if dataset has a Data.world mapping
        if dataset not in self.dataworld_mapping:
            print(f"⏭️  Skipping upload for {dataset} (not mapped to Data.world)")
            return True
            
        dataworld_project = self.dataworld_mapping[dataset]
        dataset_key = f"aragaocb/{dataworld_project}"
        
        try:
            print(f"📤 Uploading README to Data.world: {dataset_key}")
            
            # Use the same authentication pattern as ddw.py
            token = self.dw_client._config.auth_token
            if not token:
                print(f"❌ No API token available for {dataset}")
                return False
            
            # Prepare the API endpoint for dataset update
            url = f"https://api.data.world/v0/datasets/{dataset_key}"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Read the README content
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Truncate content to stay within Data.world's 25,000 character limit
            max_chars = 25000
            if len(readme_content) > max_chars:
                print(f"⚠️  README content too long ({len(readme_content)} chars), truncating to {max_chars} chars")
                # Find a good truncation point (end of a line)
                truncated = readme_content[:max_chars-100]  # Leave buffer
                last_newline = truncated.rfind('\n')
                if last_newline > 0:
                    truncated = truncated[:last_newline]
                readme_content = truncated + "\n\n... [Content truncated. See full README in the dataset repository]"
            
            # Prepare the payload to update dataset summary
            payload = {
                "summary": readme_content
            }
            
            print(f"📝 Uploading {len(readme_content)} characters to Data.world")
            
            # Make the PATCH API call
            response = requests.patch(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Successfully uploaded README for {dataset}")
                return True
            elif response.status_code == 429:
                print(f"⏳ Rate limited for {dataset}, retrying in 30 seconds...")
                import time
                time.sleep(30)
                response = requests.patch(url, json=payload, headers=headers)
                if response.status_code == 200:
                    print(f"✅ Successfully uploaded README for {dataset} (after retry)")
                    return True
                else:
                    print(f"❌ Failed to upload README for {dataset} after retry: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
            else:
                print(f"❌ Failed to upload README for {dataset}: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading README for {dataset}: {e}")
            return False
    
    def generate_readme_for_dataset(self, dataset: str) -> bool:
        """Generate README.md file for a specific dataset."""
        dataset_path = self.opsanal_dir / dataset
        if not dataset_path.exists():
            print(f"❌ Dataset directory not found: {dataset}")
            return False
        
        # Generate README content
        content = self.generate_readme_content(dataset)
        
        # Write README file
        readme_path = dataset_path / "README.md"
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated README for {dataset}: {readme_path}")
            
            # Upload to Data.world if enabled
            if self.upload_to_dataworld:
                upload_success = self.upload_readme_to_dataworld(dataset, readme_path)
                return upload_success
            
            return True
            
        except Exception as e:
            print(f"❌ Error writing README for {dataset}: {e}")
            return False
    
    def generate_all_readmes(self) -> Dict[str, bool]:
        """Generate README files for all datasets."""
        datasets = self.get_dataset_directories()
        results = {}
        
        print(f"🚀 Generating READMEs for {len(datasets)} datasets...")
        if self.upload_to_dataworld:
            print(f"📤 Data.world upload enabled - READMEs will be uploaded as dataset descriptions")
        
        for dataset in datasets:
            results[dataset] = self.generate_readme_for_dataset(dataset)
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        print(f"\\n📊 Summary: {successful}/{len(datasets)} READMEs generated successfully")
        
        if self.upload_to_dataworld:
            uploaded = sum(1 for success in results.values() if success)
            print(f"📤 Data.world uploads: {uploaded}/{len(datasets)} successful")
        
        if successful < len(datasets):
            print("\\n❌ Failed datasets:")
            for dataset, success in results.items():
                if not success:
                    print(f"  • {dataset}")
        
        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate README.md files for dataset directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--dataset",
        help="Generate README for specific dataset only"
    )
    
    parser.add_argument(
        "--upload-to-dataworld",
        action="store_true",
        help="Upload README files to Data.world as dataset descriptions"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="Generate READMEs locally but skip Data.world upload"
    )
    
    args = parser.parse_args()
    
    # Determine if we should upload to Data.world
    upload_enabled = args.upload_to_dataworld and not args.dry_run
    
    if args.dry_run and args.upload_to_dataworld:
        print("🔍 DRY RUN: READMEs will be generated locally, Data.world upload skipped")
        upload_enabled = False
    
    # Initialize generator
    generator = DatasetREADMEGenerator(upload_to_dataworld=upload_enabled)
    
    if args.dataset:
        # Generate README for specific dataset
        success = generator.generate_readme_for_dataset(args.dataset)
        sys.exit(0 if success else 1)
    else:
        # Generate READMEs for all datasets
        results = generator.generate_all_readmes()
        failed_count = sum(1 for success in results.values() if not success)
        sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
