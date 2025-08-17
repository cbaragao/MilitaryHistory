"""
Data.world API Helper for Column Metadata Updates
================================================
Helper functions for updating column descriptions and metadata in Data.world datasets.
"""

import datadotworld as dw
import requests
import json
from typing import Dict, List, Optional


class DataWorldColumnUpdater:
    """Helper class for updating Data.world column metadata via API."""
    
    def __init__(self, owner_id: str = "aragaocb"):
        self.owner_id = owner_id
        self.api_client = dw.api_client()
        
    def get_dataset_schema(self, project_name: str) -> Optional[Dict]:
        """Get the current schema/structure of a Data.world dataset."""
        try:
            dataset_key = f"{self.owner_id}/{project_name}"
            
            # Get dataset files and their schemas
            dataset_info = self.api_client.get_dataset(dataset_key)
            
            # Find CSV files that end with _tx.csv (transaction files)
            tx_files = []
            for file_info in dataset_info.get('files', []):
                file_name = file_info.get('name', '')
                if file_name.endswith('_tx.csv'):
                    tx_files.append(file_info)
            
            return {
                'dataset_key': dataset_key,
                'tx_files': tx_files,
                'total_files': len(dataset_info.get('files', []))
            }
            
        except Exception as e:
            print(f"Error getting dataset schema: {e}")
            return None
    
    def update_file_schema(self, dataset_key: str, file_name: str, 
                          column_descriptions: Dict[str, str]) -> bool:
        """Update column descriptions for a specific _tx.csv file in a Data.world dataset."""
        try:
            # Only process _tx.csv files
            if not file_name.endswith('_tx.csv'):
                print(f"⏭️  Skipping {file_name} (not a transaction file)")
                return False
                
            print(f"🎯 Processing transaction file: {file_name}")
            
            # Parse dataset key to get owner and dataset ID
            if '/' not in dataset_key:
                print(f"❌ Invalid dataset key format: {dataset_key}")
                return False
            
            owner, dataset_id = dataset_key.split('/', 1)
            
            # Use the filename without .csv extension as table ID (Data.world format)
            table_id = file_name.replace('.csv', '')
            
            print(f"📊 Dataset: {dataset_key}")
            print(f"📋 Table ID: {table_id}")
            print(f"🔧 Column descriptions to apply: {len(column_descriptions)}")
            
            # Try to update the table schema using the Data.world API
            try:
                # Use the requests library to make a direct API call
                import requests
                
                # Get the API token from the client
                token = self.api_client._config.auth_token
                if not token:
                    print(f"❌ No API token available")
                    return False
                
                # Prepare the API endpoint - use query.data.world as per documentation
                url = f"https://query.data.world/tables/{owner}/{dataset_id}/{table_id}/schema"
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                # First, get the current schema to preserve existing structure
                print(f"🔍 Getting current schema structure...")
                response = requests.get(url, headers=headers)
                if response.status_code == 429:
                    print(f"⏳ Rate limited, waiting 30 seconds...")
                    import time
                    time.sleep(30)
                    response = requests.get(url, headers=headers)
                
                if response.status_code != 200:
                    print(f"❌ Could not retrieve current schema: {response.status_code}")
                    return False
                
                current_schema = response.json()
                existing_fields = current_schema.get('fields', [])
                
                # Update existing fields with descriptions
                updated_fields = []
                for field in existing_fields:
                    field_name = field.get('name', '')
                    if field_name in column_descriptions:
                        # Clean up the description
                        clean_description = column_descriptions[field_name]
                        if '. Data type:' in clean_description:
                            clean_description = clean_description.split('. Data type:')[0]
                        
                        # Limit description length
                        if len(clean_description) > 200:
                            clean_description = clean_description[:197] + "..."
                        
                        # Add description to existing field structure
                        updated_field = field.copy()
                        updated_field['description'] = clean_description
                        updated_fields.append(updated_field)
                    else:
                        # Keep field as-is if no description available
                        updated_fields.append(field)
                
                payload = {"fields": updated_fields}
                
                print(f"🌐 Attempting API call to update {table_id} schema...")
                print(f"📝 Updating {len([f for f in updated_fields if 'description' in f])} column descriptions")
                
                # Make the API call
                response = requests.patch(url, json=payload, headers=headers)
                
                # Handle rate limiting
                if response.status_code == 429:
                    print(f"⏳ Rate limited, waiting 30 seconds before retry...")
                    import time
                    time.sleep(30)
                    response = requests.patch(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    print(f"✅ Successfully updated schema for {file_name}")
                    return True
                else:
                    print(f"❌ API call failed with status {response.status_code}")
                    print(f"📄 Response: {response.text}")
                    
                    # Fall back to showing what would be updated
                    print(f"📝 Column descriptions that were attempted:")
                    for col_name, description in column_descriptions.items():
                        print(f"  ✅ {col_name}: {description[:60]}{'...' if len(description) > 60 else ''}")
                    
                    return False
                    
            except Exception as api_error:
                print(f"❌ API error: {api_error}")
                
                # Fall back to displaying the information
                print(f"📝 Column descriptions ready for {file_name}:")
                for col_name, description in column_descriptions.items():
                    print(f"  ✅ {col_name}: {description[:60]}{'...' if len(description) > 60 else ''}")
                
                print(f"⚠️  Schema extraction successful, API update failed")
                return False
                
        except Exception as e:
            print(f"❌ Error processing transaction file schema: {e}")
            return False
    
    def _get_api_token(self) -> str:
        """Get the Data.world API token from configuration."""
        # Use the same authentication method as ddw.py
        # The datadotworld library handles authentication automatically
        return "authenticated"  # Placeholder - actual token handled by dw.api_client()
    
    def _update_schema_descriptions(self, schema: Dict, 
                                  descriptions: Dict[str, str]) -> Dict:
        """Update schema with new column descriptions."""
        updated_schema = schema.copy()
        
        # Update field descriptions
        if 'fields' in updated_schema:
            for field in updated_schema['fields']:
                field_name = field.get('name', '').lower()
                if field_name in descriptions:
                    field['description'] = descriptions[field_name]
        
        return updated_schema
    
    def preview_updates(self, project_name: str, 
                       descriptions: Dict[str, str]) -> None:
        """Preview what column descriptions would be updated for _tx.csv files."""
        print(f"\n🔍 Preview for {self.owner_id}/{project_name}:")
        
        schema_info = self.get_dataset_schema(project_name)
        if not schema_info:
            print("❌ Could not retrieve dataset schema")
            return
        
        tx_files = schema_info.get('tx_files', [])
        total_files = schema_info.get('total_files', 0)
        
        print(f"📁 Found {len(tx_files)} transaction files (_tx.csv) out of {total_files} total files")
        
        if not tx_files:
            print("❌ No _tx.csv files found in dataset")
            return
        
        for file_info in tx_files:
            file_name = file_info.get('name', 'Unknown')
            print(f"\n📄 {file_name}")
            
            # Show which columns would be updated
            matching_descriptions = 0
            for col_name, description in list(descriptions.items())[:5]:  # Show first 5
                matching_descriptions += 1
                print(f"  • {col_name}: {description[:80]}{'...' if len(description) > 80 else ''}")
            
            if len(descriptions) > 5:
                print(f"  ... and {len(descriptions) - 5} more columns")
            
            if matching_descriptions == 0:
                print("  No matching column descriptions found")
    
    def bulk_update_dataset(self, project_name: str, 
                           descriptions: Dict[str, str]) -> bool:
        """Update column descriptions for _tx.csv files in a dataset."""
        schema_info = self.get_dataset_schema(project_name)
        if not schema_info:
            return False
        
        dataset_key = schema_info['dataset_key']
        tx_files = schema_info.get('tx_files', [])
        
        if not tx_files:
            print("❌ No _tx.csv files found in dataset")
            return False
        
        print(f"🎯 Focusing on {len(tx_files)} transaction files (_tx.csv)")
        success_count = 0
        
        for file_info in tx_files:
            file_name = file_info.get('name', '')
            print(f"\n📄 Updating {file_name}...")
            
            if self.update_file_schema(dataset_key, file_name, descriptions):
                success_count += 1
        
        print(f"\n✅ Updated {success_count}/{len(tx_files)} transaction files successfully")
        
        return success_count == len(tx_files)
