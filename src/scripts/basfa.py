import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

dp.DatasetProcessor(
    dataset="basfa",
    datadotworld_project="aragaocb/basfa",
    lat_lon_pairs=[
        ("UTMC_lat", "UTMC_lon"),
        ("UTM1_lat", "UTM1_lon"),
        ("UTM2_lat", "UTM2_lon"),
        ("UTM3_lat", "UTM3_lon"),
        ("UTM4_lat", "UTM4_lon"),
        ("UTM5_lat", "UTM5_lon"),
        ("UTM6_lat", "UTM6_lon"),
        ("UTM7_lat", "UTM7_lon"),
        ("UTM8_lat", "UTM8_lon"),
        ("UTM9_lat", "UTM9_lon"),
    ],
).process()
