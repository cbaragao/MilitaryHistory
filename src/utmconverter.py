import pandas as pd
import mgrs


class UTMConverter:
    """Handles conversion of UTM coordinates to lat/lon using MGRS."""

    def __init__(self):
        self.mgrs_converter = mgrs.MGRS()
        self.ranges = ['48Q', '49Q', '48P', '49P']

    def convert_utm(self, utm: str):
        """Attempts to convert a UTM coordinate to lat/lon by trying different MGRS prefixes."""
        
        m = mgrs.MGRS()
        ranges = ['48Q', '49Q', '48P', '49P']

        def find_first_valid_mgrs():
            """Try each prefix until one works."""
            for prefix in ranges:
                full_mgrs = prefix + utm
                try:
                    print(f"🔄 Testing MGRS: {full_mgrs}")  # Debug print
                    val = m.toLatLon(full_mgrs)
                    print(f"✅ Converted {full_mgrs} -> {val}")  # Debug print
                    return (full_mgrs, val)
                except Exception as e:
                    print(f"❌ Failed to convert {full_mgrs}: {e}")  # Debug print
                    continue
            return None

        result = find_first_valid_mgrs()

        if result:
            return result
        else:
            print(f"⚠️ No valid conversion found for UTM: {utm}")
            return None



    def convert_mgrs_direct(self, mgrs_coord: str):
        """Convert MGRS coordinate directly without prefix guessing."""
        try:
            m = mgrs.MGRS()
            print(f"🔄 Converting MGRS: {mgrs_coord}")
            val = m.toLatLon(mgrs_coord)
            print(f"✅ Converted {mgrs_coord} -> {val}")
            return val
        except Exception as e:
            print(f"❌ Failed to convert MGRS {mgrs_coord}: {e}")
            return None

    def process_coordinate_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Process a specific coordinate column (UTM/MGRS)."""
        print(f"Processing {column} for coordinate conversion")
        
        # Show sample values
        sample_values = df[column].dropna().head(10)
        print("Sample coordinate values:")
        for i, val in enumerate(sample_values):
            print(f"  {i+1}: '{val}' (length: {len(val)})")

        lat_col, lon_col = f"{column}_lat", f"{column}_lon"
        df[lat_col] = None
        df[lon_col] = None

        for index, coord_value in df[column].items():
            if pd.notna(coord_value) and isinstance(coord_value, str) and coord_value.strip():
                coord_value = coord_value.strip()
                
                # For coordinates with letters, try both direct MGRS and prefix guessing
                if any(c.isalpha() for c in coord_value):
                    # First try as complete MGRS coordinate
                    result = self.convert_mgrs_direct(coord_value)
                    if result:
                        df.at[index, lat_col] = result[0]
                        df.at[index, lon_col] = result[1]
                    else:
                        # If direct MGRS fails, try as partial coordinate with prefix guessing
                        print(f"Direct MGRS failed, trying with prefixes for: {coord_value}")
                        result = self.convert_utm(coord_value)
                        if result:
                            df.at[index, lat_col] = result[1][0]
                            df.at[index, lon_col] = result[1][1]
                        else:
                            print(f"⚠️ Failed both MGRS and UTM conversion for: {coord_value}")
                else:
                    # Try as UTM with prefix guessing
                    result = self.convert_utm(coord_value)
                    if result:
                        df.at[index, lat_col] = result[1][0]
                        df.at[index, lon_col] = result[1][1]
                    else:
                        print(f"⚠️ Failed UTM conversion for: {coord_value}")

        # Show conversion results
        converted_count = df[[lat_col, lon_col]].dropna().shape[0]
        print(f"Completed conversion for {column}: {converted_count} coordinates converted")
        if converted_count > 0:
            print(df[[column, lat_col, lon_col]].dropna().head())

        return df

    def process_utm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scans DataFrame for UTM/MGRS columns and converts them to lat/lon."""
        # Check for UTM columns
        for column in df.columns:
            if 'utm' in column.lower():
                df = self.process_coordinate_column(df, column)
        
        # Check for MGRS/coordinate columns (like COARD)
        for column in df.columns:
            if any(keyword in column.lower() for keyword in ['coord', 'mgrs', 'grid']) and '_lat' not in column and '_lon' not in column:
                df = self.process_coordinate_column(df, column)

        return df  # ✅ Now contains _lat and _lon columns for each coordinate column

