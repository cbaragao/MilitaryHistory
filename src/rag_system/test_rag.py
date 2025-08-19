#!/usr/bin/env python3
"""
Simple test script for the RAG system that avoids import issues
"""
import sys
import os

# Add paths to avoid import issues
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rag_system_path = os.path.join(project_root, 'src', 'rag_system')
src_path = os.path.join(project_root, 'src')

sys.path.insert(0, rag_system_path)
sys.path.insert(0, src_path)

# Now import directly from local modules
try:
    # Import components directly
    from military_viz_rag import MilitaryVizRAG
    from vega_generator import VegaLiteGenerator
    from folium_generator import FoliumMapGenerator
    from query_processor import QueryProcessor
    
    print("✅ All RAG system components imported successfully!")
    
    # Test basic initialization
    db_path = "/home/chris/Documents/MilitaryHistory/src/ddb/opsanal.db"
    if os.path.exists(db_path):
        print(f"✅ Database found at: {db_path}")
        
        # Try to create RAG system instance
        rag = MilitaryVizRAG(db_path)
        print("✅ MilitaryVizRAG initialized successfully!")
        
        # Test query processing
        processor = QueryProcessor(rag)
        test_query = "Show hostile incidents over time from HOSTA table"
        result = processor.process_natural_language(test_query)
        print(f"✅ Query processed: {test_query}")
        print(f"   Result keys: {list(result.keys())}")
        print(f"   Detected table: {result.get('table_name', 'None')}")
        print(f"   Visualization type: {result.get('visualization_type', 'None')}")
        print(f"   Generated SQL: {result.get('sql_query', 'None')[:100]}...")
        
        # Execute the SQL query to get data
        if 'sql_query' in result and result['sql_query']:
            print(f"🔍 Executing SQL: {result['sql_query'][:100]}...")
            
            # Get database connection
            import duckdb
            con = duckdb.connect(db_path)
            
            try:
                # Execute the query
                data = con.execute(result['sql_query']).df()
                print(f"✅ Data retrieved: {data.shape[0]} rows, {data.shape[1]} columns")
                
                if not data.empty:
                    # Create output directory first
                    output_dir = os.path.join(project_root, 'visuals')
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Generate visualization based on type
                    viz_type = result.get('visualization_type', 'line_chart')
                    print(f"📊 Creating {viz_type} visualization...")
                    
                    if viz_type in ['line_chart', 'bar_chart', 'scatter_plot', 'heatmap']:
                        # Generate Vega-Lite specification
                        vega_gen = VegaLiteGenerator()
                        context = {
                            'title': f"HOSTA Incidents Analysis",
                            'query': test_query,
                            'viz_type': viz_type
                        }
                        vega_spec = vega_gen.generate_spec(data, viz_type, context)
                        
                        # Save Vega-Lite spec
                        spec_path = os.path.join(output_dir, 'rag_test_hosta_incidents.json')
                        with open(spec_path, 'w') as f:
                            import json
                            json.dump(vega_spec, f, indent=2)
                        
                        print(f"✅ Vega-Lite specification saved to: {spec_path}")
                        
                        # Create HTML file for viewing
                        html_path = os.path.join(output_dir, 'rag_test_hosta_incidents.html')
                        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>RAG Test - HOSTA Incidents</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
</head>
<body>
    <div id="vis"></div>
    <script type="text/javascript">
        var spec = {json.dumps(vega_spec, indent=2)};
        vegaEmbed('#vis', spec);
    </script>
</body>
</html>"""
                        
                        with open(html_path, 'w') as f:
                            f.write(html_content)
                        
                        print(f"✅ HTML visualization saved to: {html_path}")
                        
                    elif viz_type == 'folium_map':
                        # Check if data has geographic columns
                        geo_cols = [col for col in data.columns if col.lower() in ['latitude', 'longitude', 'lat', 'lon']]
                        if len(geo_cols) >= 2:
                            folium_gen = FoliumMapGenerator()
                            context = {
                                'title': f"HOSTA Incidents Map",
                                'query': test_query
                            }
                            map_obj = folium_gen.generate_map(data, 'density_map', context)
                            
                            # Save map
                            map_path = os.path.join(output_dir, 'rag_test_hosta_map.html')
                            map_obj.save(map_path)
                            print(f"✅ Folium map saved to: {map_path}")
                        else:
                            print("⚠️  No geographic columns found for map visualization")
                            
                else:
                    print("⚠️  No data returned from query")
                    
            except Exception as e:
                print(f"❌ Error executing query: {e}")
            finally:
                con.close()
                
        else:
            print("⚠️  No SQL query generated")
        
    else:
        print(f"❌ Database not found at: {db_path}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()