import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

datasets = ["incda", "incda_ps1", "incda_ps2", "incda_ps3"]

lat_lon_pairs = [
    ('ILOC_LAT', 'ILOC_LONG')
]

# Process all datasets in a loop
for dataset in datasets:
    print(f"🚀 Processing {dataset}...")
    
    dp.DatasetProcessor(
        dataset=dataset,
        datadotworld_project="aragaocb/republic-of-vietnam-incidents-files-incda",
        lat_lon_pairs=lat_lon_pairs
    ).process()

    print(f"✅ {dataset} processing complete!\n")
