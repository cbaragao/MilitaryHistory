#!/usr/bin/env python3
"""
PSYOPSA Master Processing Script
Processes all three PSYOPSA tables: Fixed Set, Periodic Set 1, and Periodic Set 2
"""

import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

def main():
    """Process all PSYOPSA datasets"""
    
    print("🎯 PSYOPSA - Psychological Operation System Files")
    print("=" * 60)
    print("Processing Vietnam War psychological operations data (1970-1973)")
    print()
    
    # List of PSYOPSA datasets (fixed set + two periodic sets)
    datasets = [
        "psyopsa",      # Fixed Set - District baseline data
        "psyopsa_ps1",  # Periodic Set 1 - Operations activities
        "psyopsa_ps2"   # Periodic Set 2 - Radio/TV programming
    ]
    
    # No coordinate transformation needed for PSYOPSA
    lat_lon_pairs = []
    
    # Data.world project for PSYOPSA
    datadotworld_project = "aragaocb/psyopsa"
    
    print("📋 Processing order:")
    for i, dataset in enumerate(datasets, 1):
        print(f"   {i}. {dataset}")
    print()
    
    # Process each dataset
    success_count = 0
    for i, dataset in enumerate(datasets, 1):
        print(f"🚀 Processing {dataset} ({i}/{len(datasets)})...")
        
        try:
            processor = dp.DatasetProcessor(
                dataset=dataset,
                datadotworld_project=datadotworld_project,
                lat_lon_pairs=lat_lon_pairs
            )
            processor.process()
            
            print(f"✅ {dataset} processing complete!")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {dataset}: {str(e)}")
            
        print()
    
    # Summary
    print("📊 PSYOPSA Processing Summary")
    print("=" * 40)
    print(f"✅ Successfully processed: {success_count}/{len(datasets)} datasets")
    
    if success_count == len(datasets):
        print("🎉 All PSYOPSA datasets processed successfully!")
        print()
        print("📈 Data available at:")
        print(f"   https://data.world/{datadotworld_project}")
        print()
        print("📋 Dataset breakdown:")
        print("   • psyopsa: District baseline (population, security scores)")
        print("   • psyopsa_ps1: Operations activities (leaflets, broadcasts)")
        print("   • psyopsa_ps2: Radio/TV programming details")
    else:
        print("⚠️  Some datasets failed to process. Check error messages above.")
    
    return success_count == len(datasets)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)