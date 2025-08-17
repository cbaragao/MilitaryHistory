import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

dp.DatasetProcessor(
    dataset="conga",
    datadotworld_project="aragaocb/conga",
    lat_lon_pairs=[("COARD_lat", "COARD_lon")]
).process()
