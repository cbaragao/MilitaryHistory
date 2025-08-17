#!/usr/bin/env python3
"""
PSYOPSA Periodic Set 1 Processing Script
Processes psychological operations activities (leaflets, loudspeakers, publications)
"""

import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

def main():
    """Process PSYOPSA Periodic Set 1"""
    
    print("🎯 PSYOPSA Periodic Set 1 - Operations Activities")
    print("=" * 50)
    
    # No coordinate transformation needed
    lat_lon_pairs = []
    
    # Process the dataset
    processor = dp.DatasetProcessor(
        dataset="psyopsa_ps1",
        datadotworld_project="aragaocb/psyopsa",
        lat_lon_pairs=lat_lon_pairs
    )
    
    processor.process()
    
    print("✅ PSYOPSA Periodic Set 1 processing complete!")

if __name__ == "__main__":
    main()