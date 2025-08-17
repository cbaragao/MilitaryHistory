#!/usr/bin/env python3
"""
Spatial preprocessing script for Khmer events with Cambodia administrative boundaries.
This script uses DuckDB to perform spatial joins and create province-level aggregations.
"""

import duckdb
import requests
import json
import csv
from pathlib import Path

def download_cambodia_boundaries():
    """Download Cambodia ADM1 administrative boundaries if not already present."""
    geojson_path = Path("../maps/geoBoundaries-KHM-ADM1_simplified.geojson")
    
    if geojson_path.exists():
        print(f"✓ Using existing boundaries: {geojson_path}")
        return str(geojson_path)
    
    print("📥 Downloading Cambodia administrative boundaries...")
    url = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/KHM/ADM1/geoBoundaries-KHM-ADM1_simplified.geojson"
    
    response = requests.get(url)
    response.raise_for_status()
    
    # Ensure maps directory exists
    geojson_path.parent.mkdir(exist_ok=True)
    
    with open(geojson_path, 'w') as f:
        f.write(response.text)
    
    print(f"✓ Downloaded boundaries to: {geojson_path}")
    return str(geojson_path)

def create_province_aggregation():
    """Create spatially aggregated province-level event counts."""
    
    # Initialize DuckDB with spatial extension
    conn = duckdb.connect()
    conn.execute("INSTALL spatial")
    conn.execute("LOAD spatial")
    
    print("🗺️  Loading Cambodia administrative boundaries...")
    geojson_path = download_cambodia_boundaries()
    
    # Load administrative boundaries
    conn.execute(f"""
    CREATE TABLE provinces AS 
    SELECT 
        shapeName as province_name,
        shapeID as province_id,
        geom
    FROM ST_Read('{geojson_path}')
    """)
    
    print("📍 Loading Khmer event locations...")
    
    # Load Khmer locations with proper coordinate handling
    # Note: Based on our analysis, latlong_lat_wgs84 contains longitude, latlong_long_wgs84 contains latitude
    conn.execute("""
    CREATE TABLE events AS
    SELECT 
        itemno,
        latlong_lat_wgs84 as longitude,  -- This field actually contains longitude values
        latlong_long_wgs84 as latitude,  -- This field actually contains latitude values
        ST_Point(latlong_lat_wgs84, latlong_long_wgs84) as geom
    FROM read_csv('khmer-locations.csv')
    WHERE latlong_lat_wgs84 IS NOT NULL 
    AND latlong_long_wgs84 IS NOT NULL
    AND latlong_lat_wgs84 BETWEEN 102 AND 108  -- Longitude range for Cambodia
    AND latlong_long_wgs84 BETWEEN 10 AND 15   -- Latitude range for Cambodia
    """)
    
    print("🔗 Performing spatial join...")
    
    # Spatial join and aggregation
    result = conn.execute("""
    SELECT 
        p.province_name,
        p.province_id,
        COUNT(e.itemno) as event_count,
        AVG(e.longitude) as avg_longitude,
        AVG(e.latitude) as avg_latitude
    FROM provinces p
    LEFT JOIN events e ON ST_Within(e.geom, p.geom)
    GROUP BY p.province_name, p.province_id
    ORDER BY event_count DESC
    """).fetchall()
    
    print("📊 Provincial event summary:")
    total_events = 0
    for row in result:
        province, province_id, count, avg_lon, avg_lat = row
        total_events += count if count else 0
        print(f"  {province}: {count or 0} events")
    
    print(f"\n📈 Total events spatially joined: {total_events}")
    
    # Export results
    output_path = "khmer-events-by-province.csv"
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['province_name', 'province_id', 'event_count', 'avg_longitude', 'avg_latitude'])
        writer.writerows(result)
    
    print(f"✅ Results exported to: {output_path}")
    
    # Also create a summary for verification
    conn.execute("""
    SELECT 
        COUNT(*) as total_events_in_csv,
        COUNT(CASE WHEN latitude BETWEEN 10 AND 15 
                   AND longitude BETWEEN 102 AND 108 THEN 1 END) as events_in_cambodia_bounds
    FROM events
    """)
    
    summary = conn.fetchone()
    print(f"📋 Data validation:")
    print(f"  Total events in CSV: {summary[0]}")
    print(f"  Events within Cambodia bounds: {summary[1]}")
    
    conn.close()
    return output_path

if __name__ == "__main__":
    print("🚀 Starting spatial preprocessing for Khmer events...")
    output_file = create_province_aggregation()
    print(f"🎯 Preprocessing complete! Use {output_file} for choropleth visualization.")
