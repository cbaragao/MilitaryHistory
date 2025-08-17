#!/usr/bin/env python3
"""
AIMS Korea Era (1946-1964) Data Processing Script
Processes Korean War and post-Korea era military awards data.

This script uses the centralized PartitionedDatasetProcessor for efficient processing.
For better performance when processing multiple partitions, use the master script: aims.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from partitioned_processor import PartitionedDatasetProcessor

if __name__ == "__main__":
    # Create processor and initialize shared resources
    processor = PartitionedDatasetProcessor(
        dataset="aims",
        datadotworld_project="aragaocb/aimsawards",
        lat_lon_pairs=[]  # No geographic coordinates in AIMS data
    )
    
    try:
        # Initialize shared resources (DB connection, source data, lookup tables)
        processor.initialize_shared_resources()
        
        # Process this specific partition
        success = processor.process_partition(
            sql_file="aims_korea_era.sql",
            output_name="aims_korea_era",
            description="Korean War and post-Korea period (~10,400 records)"
        )
        
        processor.log_message("🏁 Korea Era partition processing complete")
        if success:
            processor.log_message("   📁 File uploaded to: https://data.world/aragaocb/aimsawards")
            exit_code = 0
        else:
            processor.log_message("   ❌ Processing failed - check logs above")
            exit_code = 1
            
    except Exception as e:
        processor.log_message(f"❌ Fatal error: {str(e)}")
        exit_code = 1
    finally:
        # Clean up resources
        processor.cleanup()
    
    sys.exit(exit_code)