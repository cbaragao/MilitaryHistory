#!/usr/bin/env python3
"""
Simple spatial preprocessing for Khmer events with Cambodia provinces.
"""

import duckdb
import sys

def main():
    print("🚀 Starting spatial preprocessing...")
    
    try:
        # Initialize DuckDB with spatial extension
        conn = duckdb.connect()
        print("📊 Installing spatial extension...")
        conn.execute("INSTALL spatial")
        conn.execute("LOAD spatial")
        print("✅ Spatial extension loaded")
        
        # Test loading the boundaries
        print("🗺️  Loading Cambodia boundaries...")
        result = conn.execute("""
            SELECT COUNT(*) as province_count
            FROM ST_Read('../maps/geoBoundaries-KHM-ADM1_simplified.geojson')
        """).fetchone()
        print(f"✅ Found {result[0]} provinces")
        
        # Test loading the events
        print("📍 Loading Khmer events...")
        result = conn.execute("""
            SELECT COUNT(*) as event_count
            FROM read_csv('khmer-locations.csv')
            WHERE latlong_lat_wgs84 IS NOT NULL 
            AND latlong_long_wgs84 IS NOT NULL
        """).fetchone()
        print(f"✅ Found {result[0]} events")
        
        # Create tables
        print("🔧 Creating provinces table...")
        conn.execute("""
            CREATE TABLE provinces AS 
            SELECT 
                shapeName as province_name,
                shapeID as province_id,
                geom
            FROM ST_Read('../maps/geoBoundaries-KHM-ADM1_simplified.geojson')
        """)
        
        print("🔧 Creating events table...")
        conn.execute("""
            CREATE TABLE events AS
            SELECT 
                itemno,
                latlong_lat_wgs84 as longitude,
                latlong_long_wgs84 as latitude,
                ST_Point(latlong_lat_wgs84, latlong_long_wgs84) as geom
            FROM read_csv('khmer-locations.csv')
            WHERE latlong_lat_wgs84 IS NOT NULL 
            AND latlong_long_wgs84 IS NOT NULL
            AND latlong_lat_wgs84 BETWEEN 102 AND 108
            AND latlong_long_wgs84 BETWEEN 10 AND 15
        """)
        
        # Simple count first
        print("📊 Testing spatial join...")
        result = conn.execute("""
            SELECT COUNT(*) as total_events FROM events
        """).fetchone()
        print(f"✅ Events in table: {result[0]}")
        
        result = conn.execute("""
            SELECT COUNT(*) as total_provinces FROM provinces
        """).fetchone()
        print(f"✅ Provinces in table: {result[0]}")
        
        # Try spatial join
        print("🔗 Performing spatial join...")
        result = conn.execute("""
            SELECT 
                p.province_name,
                COUNT(e.itemno) as event_count
            FROM provinces p
            LEFT JOIN events e ON ST_Within(e.geom, p.geom)
            GROUP BY p.province_name
            ORDER BY event_count DESC
            LIMIT 10
        """).fetchall()
        
        print("📈 Top 10 provinces by event count:")
        for province, count in result:
            print(f"  {province}: {count or 0} events")
            
        conn.close()
        print("✅ Processing complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
