import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Import the datasetprocessor module directly
from datasetprocessor import DatasetProcessor

DatasetProcessor(
    dataset="vciia",
    datadotworld_project='aragaocb/viet-cong-initiated-incidents-vciia'
).process()
