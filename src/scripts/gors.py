import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



import datasetprocessor as dp

# List of GORS datasets
datasets = [
    "gors_67", "gors_68", "gors_69", "gors_70", "gors_71_72",
    "gors_ps1_67", "gors_ps1_68", "gors_ps1_69", "gors_ps1_70", "gors_ps1_71_72",
    "gors_ps2_67", "gors_ps2_68", "gors_ps2_69", "gors_ps2_70", "gors_ps2_71_72",
    "gors_ps3_67", "gors_ps3_68", "gors_ps3_69", "gors_ps3_70", "gors_ps3_71_72",
    "gors_ps4_67", "gors_ps4_68", "gors_ps4_69", "gors_ps4_70", "gors_ps4_71_72",
    "gors_ps5_67", "gors_ps5_68", "gors_ps5_69", "gors_ps5_70", "gors_ps5_71_72",
    "gors_ps6_67", "gors_ps6_68", "gors_ps6_69", "gors_ps6_70", "gors_ps6_71_72",
    "gors_ps7_67", "gors_ps7_68", "gors_ps7_69", "gors_ps7_70", "gors_ps7_71_72"
]

# UTM to Lat/Lon columns
lat_lon_pairs = [("UTM_lat", "UTM_lon")]

# Process all datasets in a loop
for dataset in datasets:
    print(f"🚀 Processing {dataset}...")
    
    dp.DatasetProcessor(
        dataset=dataset,
        datadotworld_project="aragaocb/ground-operations-reporting-system-gors",
        lat_lon_pairs=lat_lon_pairs
    ).process()

    print(f"✅ {dataset} processing complete!\n")
