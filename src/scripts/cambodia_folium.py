#!/usr/bin/env python3
"""
Cambodia Choropleth using Folium - often more reliable than Plotly for GeoJSON
"""

import json
import pandas as pd
import folium
from folium import plugins

def create_folium_choropleth():
    """Create Cambodia choropleth using Folium"""
    
    print("🗺️ Creating Cambodia Choropleth with Folium")
    print("=" * 50)
    
    # Event data
    event_data = {
        'Kandal': 6334, 'Takeo': 5131, 'Kampong Cham': 4735, 'Prey Veng': 4450,
        'Siem Reap': 3840, 'Kampong Speu': 3731, 'Kampong Thom': 3198, 
        'Kampong Chhnang': 2939, 'Kampot': 2365, 'Svay Rieng': 2321,
        'Phnom Penh': 1976, 'Tbong Khmum': 1275, 'Pursat': 1272, 'Battambang': 1058,
        'Preah Sihanouk': 680, 'Koh Kong': 306, 'Kep': 285, 'Bantey Meanchey': 146,
        'Oddar Meanchey': 90, 'Preah Vihear': 62, 'Pailin': 52, 'Kratie': 38,
        'Stung Treng': 8, 'Ratanakiri Province': 0, 'Mondulkiri': 0
    }
    
    # Create DataFrame
    df = pd.DataFrame([
        {'province': name, 'events': count}
        for name, count in event_data.items()
    ])
    
    print(f"📊 Data: {len(df)} provinces, {df['events'].sum():,} total events")
    
    # Create base map centered on Cambodia
    m = folium.Map(
        location=[12.8, 104.8],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Read GeoJSON
    geojson_path = '../../maps/geoBoundaries-KHM-ADM1_simplified.geojson'
    
    # Create choropleth
    choropleth = folium.Choropleth(
        geo_data=geojson_path,
        name='Cambodia Provinces',
        data=df,
        columns=['province', 'events'],
        key_on='feature.properties.shapeName',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        line_color='black',
        line_weight=2,
        legend_name='Conflict Events (1970-1975)',
        smooth_factor=0
    ).add_to(m)
    
    # Add tooltips with province names and event counts
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    # Create a feature group for tooltips
    tooltip_layer = folium.FeatureGroup(name='Province Info')
    
    for feature in geojson_data['features']:
        province_name = feature['properties']['shapeName']
        event_count = event_data.get(province_name, 0)
        
        # Create tooltip content
        tooltip_text = f"""
        <b>{province_name}</b><br>
        Events: {event_count:,}<br>
        Rank: #{sorted(event_data.values(), reverse=True).index(event_count) + 1 if event_count > 0 else 'N/A'}
        """
        
        # Add feature with tooltip
        folium.GeoJson(
            feature,
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'transparent',
                'weight': 0,
                'fillOpacity': 0
            },
            tooltip=folium.Tooltip(tooltip_text, sticky=True),
            popup=folium.Popup(f"<h4>{province_name}</h4><p>{event_count:,} conflict events</p>", max_width=300)
        ).add_to(tooltip_layer)
    
    tooltip_layer.add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add title using HTML
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; padding: 10px;">
    <h3>Cambodia Conflict Events by Province</h3>
    <p><b>1970-1975 • 46,292 total events</b></p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save the map to visuals directory
    output_file = '../../visuals/cambodia_folium_choropleth.html'
    m.save(output_file)
    
    print(f"✅ Created Folium choropleth: {output_file}")
    print()
    print("🎯 Folium advantages:")
    print("   ✓ Excellent GeoJSON handling")
    print("   ✓ Built-in choropleth support")
    print("   ✓ Interactive tooltips and popups")
    print("   ✓ Multiple map layers")
    print("   ✓ Zoom and pan controls")
    print("   ✓ Black province borders")
    
    # Print top provinces
    print()
    print("🏆 Top 5 provinces by events:")
    top_5 = df.nlargest(5, 'events')
    for i, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"   {i}. {row['province']}: {row['events']:,} events")
    
    return output_file

if __name__ == '__main__':
    create_folium_choropleth()