#!/usr/bin/env python3
"""
AIMS Gulf War Era (1990-1994) Data Processing Script
Processes Gulf War period military awards data.

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
            sql_file="aims_gulf_war_era.sql",
            output_name="aims_gulf_war_era",
            description="Gulf War period (~419,800 records)"
        )
        
        processor.log_message("🏁 Gulf War Era partition processing complete")
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