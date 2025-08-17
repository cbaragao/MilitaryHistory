#!/usr/bin/env python3
"""
Centralized Partitioned Dataset Processor
Efficiently processes large datasets by partitioning them while reusing database connections and loaded data.

This processor optimizes performance by:
- Loading source data once and reusing across all partitions
- Maintaining single database connection throughout processing
- Loading lookup tables once and sharing across partitions
- Processing partitions sequentially with shared resources
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np

# Add parent directory to path for imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp
from ddw import DDW

class PartitionedDatasetProcessor:
    """Efficiently processes dataset partitions with shared resources."""
    
    # Configuration for AIMS partitions
    AIMS_PARTITIONS = [
        {
            'name': 'Early Wars (1911-1945)',
            'sql_file': 'aims_early_wars.sql',
            'output_name': 'aims_early_wars',
            'description': 'Pre-WWII through WWII era military awards (~3,100 records)',
            'date_range': '1911-1945'
        },
        {
            'name': 'Korea Era (1946-1964)',
            'sql_file': 'aims_korea_era.sql',
            'output_name': 'aims_korea_era',
            'description': 'Korean War and post-Korea period (~10,400 records)',
            'date_range': '1946-1964'
        },
        {
            'name': 'Vietnam Era (1965-1975)',
            'sql_file': 'aims_vietnam_era.sql',
            'output_name': 'aims_vietnam_era',
            'description': 'Vietnam War period (~316,800 records)',
            'date_range': '1965-1975'
        },
        {
            'name': 'Post-Vietnam (1976-1989)',
            'sql_file': 'aims_post_vietnam.sql',
            'output_name': 'aims_post_vietnam',
            'description': 'Post-Vietnam peacetime period (~343,500 records)',
            'date_range': '1976-1989'
        },
        {
            'name': 'Gulf War Era (1990-1994)',
            'sql_file': 'aims_gulf_war_era.sql',
            'output_name': 'aims_gulf_war_era',
            'description': 'Gulf War period (~419,800 records)',
            'date_range': '1990-1994'
        }
    ]
    
    def __init__(self, dataset: str, datadotworld_project: str, lat_lon_pairs: list = None):
        """Initialize the partitioned processor."""
        self.dataset = dataset.lower()
        self.datadotworld_project = datadotworld_project
        self.lat_lon_pairs = lat_lon_pairs or []
        
        # Initialize base processor for shared functionality
        self.base_processor = dp.DatasetProcessor(dataset, datadotworld_project, lat_lon_pairs)
        
        # Shared resources (loaded once, used multiple times)
        self.db = None
        self.lookup_tables_loaded = False
        
    def log_message(self, message: str):
        """Print timestamped log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def initialize_shared_resources(self):
        """Load database, source data, and lookup tables once for all partitions."""
        self.log_message("🔧 Initializing shared resources...")
        
        # Create database connection and load source data
        self.log_message("   📦 Loading database and source data...")
        self.db = self.base_processor.processor.create_base_tables()
        
        # Load lookup tables for datasets that have them
        self.log_message("   📚 Loading lookup tables...")
        from nara import Nara
        nara = Nara(self.dataset)
        nara.load_lookup_tables(self.db)
        self.lookup_tables_loaded = True
        
        # Load SQL macros
        self.log_message("   ⚙️  Loading SQL macros...")
        self._load_sql_macros()
        
        self.log_message("✅ Shared resources initialized successfully")
    
    def _load_sql_macros(self):
        """Load SQL macros into the database."""
        current_dir = Path(__file__).resolve().parent
        macros_paths = [
            current_dir / "sql" / "macros.sql",
            current_dir / "sql" / "opsanal" / "macros.sql",
            current_dir / ".." / "sql" / "macros.sql"
        ]
        
        macros_loaded = False
        for path in macros_paths:
            if path.exists():
                self.log_message(f"      Loading SQL macros from {path}")
                with open(path, 'r') as file:
                    macros_sql = file.read()
                    self.db.execute(macros_sql)
                macros_loaded = True
                break
        
        if not macros_loaded:
            self.log_message("      Warning: macros.sql not found, creating required functions inline")
            self.db.execute("""
                CREATE OR REPLACE FUNCTION remove_nan_decimals(input VARCHAR) RETURNS VARCHAR AS
                BEGIN
                    IF input IS NULL THEN
                        RETURN NULL;
                    ELSE
                        -- Replace '.0', '.00', etc. with empty string
                        RETURN REGEXP_REPLACE(input, '\\.0+$', '');
                    END IF;
                END;
            """)
    
    def process_partition(self, sql_file: str, output_name: str, description: str = ""):
        """Process a single partition using shared database connection."""
        if not self.db:
            raise RuntimeError("Shared resources not initialized. Call initialize_shared_resources() first.")
        
        self.log_message(f"🔄 Processing partition: {output_name}")
        if description:
            self.log_message(f"   📝 {description}")
        
        start_time = time.time()
        
        try:
            # Load custom SQL file
            current_dir = os.path.dirname(__file__)
            sql_path = os.path.join(current_dir, "sql/opsanal", sql_file)
            
            if not os.path.exists(sql_path):
                raise FileNotFoundError(f"SQL file not found: {sql_path}")
            
            with open(sql_path, "r") as file:
                query = file.read()
            
            # Execute the partition SQL query
            df = self.db.execute(query).fetchdf()
            
            # Process coordinates if applicable
            df_transformed = self.base_processor.process_utm(df)
            
            # Save transformed data to DuckDB (optional, for debugging)
            self.db.sql(f"DROP TABLE IF EXISTS {output_name}_tx")
            self.db.sql(f"CREATE TABLE {output_name}_tx AS SELECT * FROM df_transformed")
            
            # Upload to data.world with proper null handling
            self._upload_partition(df_transformed, output_name)
            
            # Cleanup CSV files
            self._cleanup_files(output_name)
            
            end_time = time.time()
            duration = end_time - start_time
            record_count = len(df_transformed)
            
            self.log_message(f"✅ Partition {output_name} completed: {record_count:,} records in {duration:.1f}s")
            return True
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self.log_message(f"❌ Partition {output_name} failed after {duration:.1f}s: {str(e)}")
            return False
    
    def _upload_partition(self, df: pd.DataFrame, output_name: str):
        """Upload partition data to data.world with proper null handling."""
        csv_file = f"{output_name}_tx.csv"
        schema_file = f"{output_name}_schema.csv"
        
        # Clean string 'nan' values and convert to actual NaN
        df_clean = df.replace('nan', np.nan).infer_objects(copy=False)
        
        # Save to CSV with proper null handling
        df_clean.to_csv(csv_file, index=False, na_rep='')
        DDW(files=[csv_file], owner_id="aragaocb").upload_to_dataset(self.datadotworld_project)
        
        # Upload schema if it exists
        try:
            schema_exists = self.db.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.dataset}_schema'"
            ).fetchone()
            
            if schema_exists:
                schema_df = self.db.execute(f"SELECT * FROM {self.dataset}_schema").fetchdf()
                schema_df_clean = schema_df.replace('nan', np.nan).infer_objects(copy=False)
                schema_df_clean.to_csv(schema_file, index=False, na_rep='')
                DDW(files=[schema_file], owner_id="aragaocb").upload_to_dataset(self.datadotworld_project)
        except Exception as e:
            self.log_message(f"      Schema upload failed (non-critical): {e}")
    
    def _cleanup_files(self, output_name: str):
        """Clean up temporary CSV files."""
        files_to_clean = [f"{output_name}_tx.csv", f"{output_name}_schema.csv"]
        for file in files_to_clean:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                self.log_message(f"      Warning: Could not clean up {file}: {e}")
    
    def process_all_partitions(self, partitions: list = None):
        """Process all partitions efficiently with shared resources."""
        if partitions is None:
            if self.dataset.lower() == 'aims':
                partitions = self.AIMS_PARTITIONS
            else:
                raise ValueError(f"No default partitions defined for dataset: {self.dataset}")
        
        self.log_message("=" * 80)
        self.log_message("🎯 Partitioned Dataset Processing Started")
        self.log_message(f"   Dataset: {self.dataset.upper()}")
        self.log_message(f"   Partitions: {len(partitions)}")
        self.log_message(f"   Target: data.world project {self.datadotworld_project}")
        self.log_message("=" * 80)
        
        overall_start = time.time()
        
        try:
            # Initialize shared resources once
            self.initialize_shared_resources()
            
            successful = 0
            failed = 0
            total_records = 0
            
            # Process each partition
            for i, partition in enumerate(partitions, 1):
                self.log_message(f"\n📊 Processing partition {i}/{len(partitions)}: {partition['name']}")
                
                success = self.process_partition(
                    partition['sql_file'],
                    partition['output_name'],
                    partition['description']
                )
                
                if success:
                    successful += 1
                    # Get record count from last processed partition
                    try:
                        count_result = self.db.execute(f"SELECT COUNT(*) FROM {partition['output_name']}_tx").fetchone()
                        if count_result:
                            total_records += count_result[0]
                    except:
                        pass
                else:
                    failed += 1
                
                # Brief pause between partitions (but keep DB connection open)
                if i < len(partitions):
                    self.log_message("   ⏸️  Pausing 1 second before next partition...")
                    time.sleep(1)
            
            # Final summary
            overall_end = time.time()
            total_duration = overall_end - overall_start
            
            self.log_message("\n" + "=" * 80)
            self.log_message("🏁 Partitioned Processing Complete")
            self.log_message(f"   Total Duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
            self.log_message(f"   Total Records Processed: {total_records:,}")
            self.log_message(f"   Successful Partitions: {successful}/{len(partitions)}")
            self.log_message(f"   Failed Partitions: {failed}/{len(partitions)}")
            
            if failed > 0:
                self.log_message("   ⚠️  Some partitions failed - check logs above for details")
                return 1
            else:
                self.log_message("   🎉 All partitions processed successfully!")
                self.log_message(f"   📁 Files uploaded to: https://data.world/{self.datadotworld_project}")
                return 0
                
        finally:
            # Clean up shared resources
            if self.db:
                self.log_message("🧹 Cleaning up shared resources...")
                self.db.close()
                self.db = None
    
    def cleanup(self):
        """Clean up resources."""
        if self.db:
            self.db.close()
            self.db = None