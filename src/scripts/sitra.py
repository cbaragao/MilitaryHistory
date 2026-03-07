#!/usr/bin/env python3
"""
SITRA Master Processing Script
Significant Incident Tracking and Reporting - RG-218 (Joint Chiefs of Staff)

Processes 4 SITRA files covering 1966-1973. Run each dataset individually
to avoid singleton conflicts:

    python src/scripts/sitra_66_68.py
    python src/scripts/sitra_69.py
    python src/scripts/sitra_70.py
    python src/scripts/sitra_71_73.py

Or run all via subprocess (recommended):
    python src/scripts/sitra.py
"""

import os
import sys
import subprocess

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    datasets = [
        "sitra_66_68",
        "sitra_69",
        "sitra_70",
        "sitra_71_73",
    ]

    success_count = 0
    for dataset in datasets:
        print(f"Processing {dataset}...")
        script = os.path.join(scripts_dir, f"{dataset}.py")
        result = subprocess.run([sys.executable, script])
        if result.returncode == 0:
            print(f"{dataset} complete!")
            success_count += 1
        else:
            print(f"Error processing {dataset} (exit code {result.returncode})")
        print()

    print(f"Done: {success_count}/{len(datasets)} datasets processed successfully.")
    return success_count == len(datasets)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
