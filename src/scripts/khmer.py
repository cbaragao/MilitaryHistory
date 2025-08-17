import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

dp.DatasetProcessor(
    dataset="khmer",
    datadotworld_project="aragaocb/khmer",
    lat_lon_pairs=[("LATLONG_LAT", "LATLONG_LONG")]
).process()