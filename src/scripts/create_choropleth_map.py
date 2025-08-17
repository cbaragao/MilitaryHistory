#!/usr/bin/env python3
"""
Cambodia Choropleth Map Generator using Folium
Clean implementation for creating choropleth maps from conflict event data
"""

import json
import pandas as pd
import folium
from folium import plugins

def create_cambodia_choropleth():
    """Create Cambodia choropleth map showing conflict events by province"""
    
    print("🗺️ Creating Cambodia Conflict Events Choropleth Map")
    print("=" * 60)
    
    # Event data for each province (from spatial analysis)
    event_data = {
        'Kandal': 6334, 'Takeo': 5131, 'Kampong Cham': 4735, 'Prey Veng': 4450,
        'Siem Reap': 3840, 'Kampong Speu': 3731, 'Kampong Thom': 3198, 
        'Kampong Chhnang': 2939, 'Kampot': 2365, 'Svay Rieng': 2321,
        'Phnom Penh': 1976, 'Tbong Khmum': 1275, 'Pursat': 1272, 'Battambang': 1058,
        'Preah Sihanouk': 680, 'Koh Kong': 306, 'Kep': 285, 'Bantey Meanchey': 146,
        'Oddar Meanchey': 90, 'Preah Vihear': 62, 'Pailin': 52, 'Kratie': 38,
        'Stung Treng': 8, 'Ratanakiri Province': 0, 'Mondulkiri': 0
    }
    
    # Create DataFrame for choropleth data
    df = pd.DataFrame([
        {'province': name, 'events': count}
        for name, count in event_data.items()
    ])
    
    print(f"📊 Dataset: {len(df)} provinces, {df['events'].sum():,} total events")
    print(f"📊 Range: {df['events'].min()} to {df['events'].max():,} events")
    
    # Create base map centered on Cambodia
    map_center = [12.8, 104.8]  # Cambodia center coordinates
    m = folium.Map(
        location=map_center,
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Path to GeoJSON file with province boundaries
    geojson_path = '../../maps/geoBoundaries-KHM-ADM1_simplified.geojson'
    
    # Create choropleth layer
    choropleth = folium.Choropleth(
        geo_data=geojson_path,
        name='Cambodia Provinces',
        data=df,
        columns=['province', 'events'],
        key_on='feature.properties.shapeName',  # Match GeoJSON property
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        line_color='black',
        line_weight=2,
        legend_name='Conflict Events (1970-1975)',
        smooth_factor=0
    ).add_to(m)
    
    # Load GeoJSON for adding interactive features
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    # Create interactive tooltip layer
    tooltip_layer = folium.FeatureGroup(name='Province Details')
    
    for feature in geojson_data['features']:
        province_name = feature['properties']['shapeName']
        event_count = event_data.get(province_name, 0)
        
        # Calculate rank
        sorted_counts = sorted(event_data.values(), reverse=True)
        rank = sorted_counts.index(event_count) + 1 if event_count > 0 else 'N/A'
        
        # Create rich tooltip content
        tooltip_text = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <b style="font-size: 14px;">{province_name}</b><br>
            <b>Events:</b> {event_count:,}<br>
            <b>Rank:</b> #{rank}<br>
            <b>% of Total:</b> {(event_count/df['events'].sum()*100):.1f}%
        </div>
        """
        
        # Create popup content
        popup_text = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0; color: #2c3e50;">{province_name}</h4>
            <hr style="margin: 5px 0;">
            <p><b>Conflict Events:</b> {event_count:,}</p>
            <p><b>Provincial Rank:</b> #{rank} of 25</p>
            <p><b>Percentage:</b> {(event_count/df['events'].sum()*100):.1f}% of total</p>
        </div>
        """
        
        # Add invisible feature for tooltips (doesn't interfere with choropleth)
        folium.GeoJson(
            feature,
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'transparent',
                'weight': 0,
                'fillOpacity': 0
            },
            tooltip=folium.Tooltip(tooltip_text, sticky=True),
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(tooltip_layer)
    
    tooltip_layer.add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add title and subtitle
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 450px; height: 100px; 
                background-color: white; border: 2px solid #2c3e50; z-index: 9999; 
                font-family: Arial, sans-serif; border-radius: 5px; padding: 15px;">
        <h3 style="margin: 0; color: #2c3e50; font-size: 18px;">
            Cambodia Conflict Events by Province
        </h3>
        <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;">
            <b>1970-1975 • 46,292 total events across 25 provinces</b>
        </p>
        <p style="margin: 0; font-size: 12px; color: #95a5a6;">
            Click provinces for details • Hover for quick stats
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save the final map to visuals directory
    output_file = '../../visuals/cambodia_choropleth_map.html'
    m.save(output_file)
    
    print(f"✅ Created choropleth map: {output_file}")
    print()
    print("🎯 Map features:")
    print("   ✓ Province-level conflict event data")
    print("   ✓ Interactive tooltips with statistics")
    print("   ✓ Clickable popups with detailed information")
    print("   ✓ Color-coded intensity (light to dark)")
    print("   ✓ Black province boundaries for clarity")
    print("   ✓ Zoom and pan controls")
    print("   ✓ Layer control for toggling features")
    
    # Print summary statistics
    print()
    print("📊 Top 5 provinces by conflict events:")
    top_5 = df.nlargest(5, 'events')
    for i, (_, row) in enumerate(top_5.iterrows(), 1):
        pct = (row['events']/df['events'].sum()*100)
        print(f"   {i}. {row['province']:<20}: {row['events']:>5,} events ({pct:.1f}%)")
    
    return output_file

if __name__ == '__main__':
    output_file = create_cambodia_choropleth()
    print(f"\n🎉 Successfully created: {output_file}")
    print("📖 Open this file in your web browser to view the interactive map")