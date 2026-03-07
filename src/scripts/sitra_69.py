#!/usr/bin/env python3
"""SITRA 1969 Processing Script"""

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import datasetprocessor as dp

def main():
    processor = dp.DatasetProcessor(
        dataset="sitra_69",
        datadotworld_project="aragaocb/sitra",
        lat_lon_pairs=[]
    )
    processor.process()
    print("sitra_69 processing complete!")

if __name__ == "__main__":
    main()
