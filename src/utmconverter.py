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



    def process_utm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scans DataFrame for UTM columns and converts them to lat/lon."""
        for column in df.columns:
            if 'utm' in column.lower():
                print(f"Processing {column} for UTM conversion")
                print(df[column].dropna().head())  # Print sample UTM values before conversion

                lat_col, lon_col = f"{column}_lat", f"{column}_lon"
                df[lat_col] = None
                df[lon_col] = None

                for index, utm_value in df[column].items():
                    if pd.notna(utm_value) and isinstance(utm_value, str):
                        result = self.convert_utm(utm_value)
                        if result:
                            df.at[index, lat_col] = result[1][0]
                            df.at[index, lon_col] = result[1][1]
                        else:
                            print(f"⚠️ Failed to convert {column} value: {utm_value}")

                print(f"Completed conversion for {column}:")
                print(df[[lat_col, lon_col]].dropna().head())  # Print converted values

        return df  # ✅ Now contains _lat and _lon columns for each UTM column

