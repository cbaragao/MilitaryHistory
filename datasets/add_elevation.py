#!/usr/bin/env python3
"""
Add elevation data to CSV file using offline elevation approximation.
Uses the 'elevation' package which downloads SRTM data locally for offline use.
"""

import pandas as pd
import elevation
import os
from pathlib import Path

def add_elevation_to_csv(input_file, output_file):
    """
    Add elevation column to CSV file using offline SRTM data.
    
    The elevation package downloads SRTM (Shuttle Radar Topography Mission) data
    which provides ~30m resolution elevation data globally. This is downloaded
    once and cached locally, making it suitable for processing large datasets
    without API rate limits or costs.
    """
    
    print(f"Reading CSV file: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Processing {len(df)} rows...")
    print(f"Coordinate bounds: Lat {df['Latitude'].min():.3f} to {df['Latitude'].max():.3f}, "
          f"Lon {df['Longitude'].min():.3f} to {df['Longitude'].max():.3f}")
    
    # Prepare coordinate bounds for SRTM data download
    bounds = [
        df['Longitude'].min() - 0.1,  # West
        df['Latitude'].min() - 0.1,   # South  
        df['Longitude'].max() + 0.1,  # East
        df['Latitude'].max() + 0.1    # North
    ]
    
    print("Downloading SRTM elevation data (this may take a few minutes for the first run)...")
    
    # Create a temporary DEM file for the region
    dem_path = 'temp_dem.tif'
    
    # Download and cache SRTM data for the bounding box
    elevation.clip(bounds=bounds, output=dem_path, product='SRTM1')
    
    print("Adding elevation values...")
    
    # Process coordinates in batches for memory efficiency
    batch_size = 1000
    elevations = []
    
    for i in range(0, len(df), batch_size):
        batch_end = min(i + batch_size, len(df))
        batch_coords = df.iloc[i:batch_end]
        
        # Create coordinate pairs for elevation lookup
        coords = list(zip(batch_coords['Longitude'], batch_coords['Latitude']))
        
        # Get elevation values for this batch
        batch_elevations = elevation.elevation(coords, dem_path)
        elevations.extend(batch_elevations)
        
        if (i // batch_size + 1) % 10 == 0:
            print(f"  Processed {batch_end}/{len(df)} rows...")
    
    # Add elevation column to dataframe
    df['Elevation_m'] = elevations
    
    print(f"Elevation statistics:")
    print(f"  Min: {df['Elevation_m'].min():.1f}m")
    print(f"  Max: {df['Elevation_m'].max():.1f}m") 
    print(f"  Mean: {df['Elevation_m'].mean():.1f}m")
    print(f"  Median: {df['Elevation_m'].median():.1f}m")
    
    # Save the result
    print(f"Saving results to: {output_file}")
    df.to_csv(output_file, index=False)
    
    # Cleanup temporary DEM file
    if os.path.exists(dem_path):
        os.remove(dem_path)
    
    print("Complete!")
    return len(df)

if __name__ == "__main__":
    input_file = "/home/chris/Documents/MilitaryHistory/datasets/vciia_geo_events.csv"
    output_file = "/home/chris/Documents/MilitaryHistory/datasets/vciia_geo_events_with_elevation.csv"
    
    rows_processed = add_elevation_to_csv(input_file, output_file)
    print(f"\nSuccessfully processed {rows_processed} rows and added elevation data.")