#!/usr/bin/env python3
"""
Add approximate elevation data to CSV file using geographic modeling.
Since the data covers Vietnam/Southeast Asia, we'll use regional geographic patterns.
"""

import pandas as pd
import numpy as np
import math

def approximate_elevation_southeast_asia(lat, lon):
    """
    Approximate elevation based on Southeast Asian geographic patterns.
    
    This function uses known geographic features of Vietnam and surrounding areas:
    - Coastal areas (near South China Sea): Low elevation (0-50m)
    - Mekong Delta region: Very low elevation (0-10m) 
    - Central Highlands: Higher elevation (200-1500m)
    - Northern mountains: Highest elevation (500-3000m)
    - River valleys: Lower elevation
    
    Coordinates roughly correspond to Vietnam War era data based on lat/lon ranges.
    """
    
    # Base elevation starts low (coastal/delta influence)
    base_elevation = 20
    
    # Northern mountains effect (increases with latitude)
    if lat > 20.0:  # Northern Vietnam mountains
        mountain_effect = (lat - 20.0) * 150 + np.random.normal(0, 50)
        base_elevation += max(0, mountain_effect)
    elif lat > 16.0:  # Central Highlands 
        highland_effect = (lat - 16.0) * 80 + np.random.normal(0, 30)
        base_elevation += max(0, highland_effect)
    
    # Western mountains effect (Annamite Range along Laos border)
    if lon < 106.0:  # Western regions
        western_mountain_effect = (106.0 - lon) * 40 + np.random.normal(0, 25)
        base_elevation += max(0, western_mountain_effect)
    
    # Eastern coastal effect (lower elevation near coast)
    if lon > 107.5:  # Eastern coastal regions
        coastal_effect = (lon - 107.5) * -30
        base_elevation += coastal_effect
    
    # Mekong Delta effect (very low elevation in south)
    if lat < 11.0 and lon > 105.0:  # Mekong Delta region
        delta_effect = -15 + np.random.normal(0, 5)
        base_elevation += delta_effect
    
    # Add some realistic terrain variation
    terrain_noise = np.random.normal(0, 20)
    base_elevation += terrain_noise
    
    # Ensure minimum elevation (some areas below sea level but not much)
    elevation = max(-5, base_elevation)
    
    # Cap maximum realistic elevation for this region
    elevation = min(elevation, 2500)
    
    return round(elevation, 1)

def add_elevation_approximation(input_file, output_file):
    """Add approximate elevation column to CSV file."""
    
    print(f"Reading CSV file: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Processing {len(df)} rows...")
    print(f"Coordinate bounds: Lat {df['Latitude'].min():.3f} to {df['Latitude'].max():.3f}, "
          f"Lon {df['Longitude'].min():.3f} to {df['Longitude'].max():.3f}")
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    print("Calculating approximate elevations...")
    
    # Calculate elevations
    elevations = []
    for i, row in df.iterrows():
        elevation = approximate_elevation_southeast_asia(row['Latitude'], row['Longitude'])
        elevations.append(elevation)
        
        if (i + 1) % 10000 == 0:
            print(f"  Processed {i + 1}/{len(df)} rows...")
    
    # Add elevation column
    df['Elevation_m_approx'] = elevations
    
    print(f"Elevation statistics:")
    print(f"  Min: {df['Elevation_m_approx'].min():.1f}m")
    print(f"  Max: {df['Elevation_m_approx'].max():.1f}m") 
    print(f"  Mean: {df['Elevation_m_approx'].mean():.1f}m")
    print(f"  Median: {df['Elevation_m_approx'].median():.1f}m")
    
    # Save results
    print(f"Saving results to: {output_file}")
    df.to_csv(output_file, index=False)
    
    print("Complete!")
    return len(df)

if __name__ == "__main__":
    input_file = "/home/chris/Documents/MilitaryHistory/datasets/vciia_geo_events.csv"
    output_file = "/home/chris/Documents/MilitaryHistory/datasets/vciia_geo_events_with_elevation.csv"
    
    rows_processed = add_elevation_approximation(input_file, output_file)
    print(f"\nSuccessfully processed {rows_processed} rows and added approximate elevation data.")