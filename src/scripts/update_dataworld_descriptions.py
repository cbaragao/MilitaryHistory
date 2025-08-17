#!/usr/bin/env python3
"""
Data.world Column Description Updater
=====================================
Dynamically updates column descriptions in Data.world datasets using schema 
information from JSON files in the opsanal directory structure.

Usage:
    python update_dataworld_descriptions.py [dataset_name] [--dry-run]
    
Examples:
    python update_dataworld_descriptions.py psyopsa --dry-run
    python update_dataworld_descriptions.py aims 
    python update_dataworld_descriptions.py --all
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from common import Common
from dataworld_updater import DataWorldColumnUpdater


class DataWorldDescriptionUpdater:
    """Updates Data.world dataset column descriptions using local schema files."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.owner_id = "aragaocb"  # Default owner ID
        self.project_root = Path(__file__).parent.parent.parent
        self.dw_updater = DataWorldColumnUpdater(self.owner_id)
        
    def get_available_datasets(self) -> List[str]:
        """Get list of datasets that have processing scripts."""
        scripts_dir = Path(__file__).parent
        dataset_scripts = []
        
        for script_file in scripts_dir.glob("*.py"):
            # Skip utility scripts and this script itself
            if script_file.name in ["__init__.py", "update_dataworld_descriptions.py", 
                                  "cambodia_folium.py", "create_choropleth_map.py"]:
                continue
            
            dataset_name = script_file.stem
            # Check if corresponding opsanal directory exists
            opsanal_dir = self.project_root / "opsanal" / dataset_name
            if opsanal_dir.exists():
                dataset_scripts.append(dataset_name)
                
        return sorted(dataset_scripts)
    
    def load_schema_data(self, dataset: str) -> Optional[List[Dict]]:
        """Load schema data for a dataset from JSON files."""
        try:
            # Try to load schema directly from JSON file
            schema_path = self.project_root / "opsanal" / dataset / "schema" / "schema.json"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    schema_json = json.load(f)
                    if isinstance(schema_json, dict) and 'data' in schema_json:
                        return schema_json['data']
                    elif isinstance(schema_json, list):
                        return schema_json
            
            # Fallback: try to use Common class
            common = Common(dataset=dataset)
            schema_df = common.get_json_data("schema", "schema")
            
            if not schema_df.empty:
                return schema_df.to_dict('records')
            else:
                print(f"Warning: No valid schema data found for {dataset}")
                return None
                
        except Exception as e:
            print(f"Error loading schema for {dataset}: {e}")
            return None
    
    def extract_column_descriptions(self, schema_data: List[Dict]) -> Dict[str, str]:
        """Extract column ID to description mapping from schema data."""
        descriptions = {}
        
        for field in schema_data:
            if field.get("field_group") == "FIELD":
                column_id = field.get("id", "").strip()
                # Build comprehensive description from available fields
                description_parts = []
                
                # Primary description
                if field.get("definition"):
                    description_parts.append(field["definition"])
                elif field.get("title"):
                    description_parts.append(field["title"])
                
                # Add data type information
                if field.get("data_values"):
                    description_parts.append(f"Data type: {field['data_values']}")
                
                # Add length information for fixed-width fields
                if field.get("length"):
                    description_parts.append(f"Length: {field['length']} characters")
                
                # Join all parts
                if description_parts:
                    descriptions[column_id.lower()] = ". ".join(description_parts)
                    
        return descriptions
    
    def query_dataworld_datasets(self) -> List[str]:
        """Query Data.world to get all datasets for the owner."""
        try:
            # Use the API client to get user's datasets
            datasets = self.dw_updater.api_client.get_user(self.owner_id).get('datasets', [])
            dataset_names = [ds.get('id', '').replace(f'{self.owner_id}/', '') for ds in datasets if ds.get('id')]
            return [name for name in dataset_names if name]  # Filter out empty names
        except Exception as e:
            print(f"Warning: Could not query Data.world datasets: {e}")
            return []
    
    def fuzzy_match_dataset(self, local_dataset: str, dataworld_datasets: List[str]) -> Optional[str]:
        """Find the best matching Data.world dataset name using fuzzy matching."""
        if not dataworld_datasets:
            return None
            
        best_match = None
        best_score = 0.0
        
        for dw_dataset in dataworld_datasets:
            # Calculate similarity score
            score = SequenceMatcher(None, local_dataset.lower(), dw_dataset.lower()).ratio()
            
            # Boost score if local dataset name is contained in Data.world name
            if local_dataset.lower() in dw_dataset.lower():
                score += 0.3
                
            # Boost score if they start with the same letters
            if dw_dataset.lower().startswith(local_dataset.lower()[:3]):
                score += 0.2
                
            if score > best_score and score > 0.4:  # Minimum threshold
                best_score = score
                best_match = dw_dataset
        
        return best_match
    
    def auto_discover_dataset_mapping(self) -> Dict[str, str]:
        """Automatically discover dataset name mapping by querying Data.world."""
        print("🔍 Auto-discovering Data.world dataset mappings...")
        
        # Get local datasets
        local_datasets = self.get_available_datasets()
        
        # Query Data.world for actual datasets
        dataworld_datasets = self.query_dataworld_datasets()
        
        if not dataworld_datasets:
            print("⚠️  Could not retrieve Data.world datasets, using fallback mapping")
            return self.get_dataset_project_mapping()
        
        print(f"📊 Found {len(dataworld_datasets)} datasets on Data.world")
        print(f"📁 Found {len(local_datasets)} local datasets")
        
        # Create mapping using fuzzy matching
        auto_mapping = {}
        for local_dataset in local_datasets:
            match = self.fuzzy_match_dataset(local_dataset, dataworld_datasets)
            if match:
                auto_mapping[local_dataset] = match
                print(f"  ✅ {local_dataset} → {match}")
            else:
                # Try exact name as fallback
                auto_mapping[local_dataset] = local_dataset
                print(f"  ⚠️  {local_dataset} → {local_dataset} (no match found)")
        
        return auto_mapping
    
    def get_dataset_project_mapping(self) -> Dict[str, str]:
        """Map dataset names to their Data.world project names from individual processing scripts."""
        # Extracted from datadotworld_project variables in each script
        mapping = {
            "psyopsa": "psyopsa",  # psyopsa.py: "aragaocb/psyopsa"
            "khmer": "khmer",      # khmer.py: "aragaocb/khmer"
            "aims": "aimsawards",  # aims.py: "aragaocb/aimsawards"
            "seafa": "southeast-asia-forces-seafa",  # seafa.py: "aragaocb/southeast-asia-forces-seafa"
            "gors": "ground-operations-reporting-system-gors",  # gors.py: "aragaocb/ground-operations-reporting-system-gors"
            "incda": "republic-of-vietnam-incidents-files-incda",  # incda.py: "aragaocb/republic-of-vietnam-incidents-files-incda"
            "tirsa": "terrorist-incident-reporting-system-tirsa",  # tirsa.py: "aragaocb/terrorist-incident-reporting-system-tirsa"
            "vciia": "viet-cong-initiated-incidents-vciia",  # vciia.py: "aragaocb/viet-cong-initiated-incidents-vciia"
            "basfa": "basfa",      # basfa.py: "aragaocb/basfa"
            "conga": "conga",      # conga.py: "aragaocb/conga"
            "hes": "hes",          # No script found, using fallback
        }
        return mapping
    
    def get_dataworld_dataset_info(self, project_name: str) -> Optional[Dict]:
        """Get dataset information from Data.world."""
        try:
            dataset_key = f"{self.owner_id}/{project_name}"
            dataset_info = self.api_client.get_dataset(dataset_key)
            return dataset_info
        except Exception as e:
            print(f"Error getting dataset info for {project_name}: {e}")
            return None
    
    def update_dataset_descriptions(self, dataset: str) -> bool:
        """Update column descriptions for a specific dataset."""
        print(f"\n🔄 Processing {dataset}...")
        
        # Load schema data
        schema_data = self.load_schema_data(dataset)
        if not schema_data:
            print(f"❌ No schema data found for {dataset}")
            return False
        
        # Extract column descriptions
        descriptions = self.extract_column_descriptions(schema_data)
        if not descriptions:
            print(f"❌ No column descriptions found for {dataset}")
            return False
        
        print(f"📋 Found {len(descriptions)} column descriptions")
        
        # Get Data.world project name
        project_mapping = self.get_dataset_project_mapping()
        project_name = project_mapping.get(dataset, dataset)
        
        # Get dataset info from Data.world
        if self.dry_run:
            print("🔍 DRY RUN - Column descriptions that would be updated:")
            for col_id, description in descriptions.items():
                print(f"  • {col_id}: {description[:100]}{'...' if len(description) > 100 else ''}")
            
            # Show preview of what would be updated
            self.dw_updater.preview_updates(project_name, descriptions)
            return True
        
        # Actually update the descriptions
        print(f"🚀 Updating Data.world dataset: {self.owner_id}/{project_name}")
        success = self.dw_updater.bulk_update_dataset(project_name, descriptions)
        
        if success:
            print(f"✅ Successfully updated all files in {project_name}")
        else:
            print(f"⚠️  Some updates failed for {project_name}")
            
        return success
    
    def update_all_datasets(self) -> None:
        """Update descriptions for all available datasets."""
        datasets = self.get_available_datasets()
        print(f"🎯 Found {len(datasets)} datasets to process")
        
        successful_updates = 0
        for dataset in datasets:
            if self.update_dataset_descriptions(dataset):
                successful_updates += 1
        
        print(f"\n📊 Summary: {successful_updates}/{len(datasets)} datasets updated successfully")


def main():
    parser = argparse.ArgumentParser(
        description="Update Data.world column descriptions from schema JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s psyopsa --dry-run          # Preview updates for PSYOPSA dataset
  %(prog)s aims                       # Update AIMS dataset descriptions  
  %(prog)s --all                      # Update all available datasets
  %(prog)s --list                     # List available datasets
        """
    )
    
    parser.add_argument(
        "dataset", 
        nargs="?", 
        help="Dataset name to update (e.g., psyopsa, aims, conga)"
    )
    
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Update all available datasets"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Preview changes without actually updating Data.world"
    )
    
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List all available datasets and exit"
    )
    
    args = parser.parse_args()
    
    updater = DataWorldDescriptionUpdater(dry_run=args.dry_run)
    
    # List available datasets
    if args.list:
        datasets = updater.get_available_datasets()
        print("📋 Available datasets:")
        for dataset in datasets:
            print(f"  • {dataset}")
        return
    
    # Update all datasets
    if args.all:
        updater.update_all_datasets()
        return
    
    # Update specific dataset
    if args.dataset:
        success = updater.update_dataset_descriptions(args.dataset)
        sys.exit(0 if success else 1)
    
    # No action specified
    parser.print_help()
    print(f"\n💡 Tip: Use --list to see available datasets")


if __name__ == "__main__":
    main()
