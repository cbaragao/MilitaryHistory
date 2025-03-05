from pyproj import Transformer
import pandas as pd

class TransformCoordinates:
    """Converts EPSG:4131 to WGS84 (EPSG:4326)."""

    def __init__(self):
        self.transformer = Transformer.from_crs("EPSG:4131", "EPSG:4326", always_xy=True)

    def convert_to_wgs84(self, lon, lat):
        """Convert EPSG:4131 to WGS84 and print input types for debugging."""
        
        print(f"🚀 Converting to WGS84: lat={lat} (type={type(lat)}), lon={lon} (type={type(lon)})")

        # Ensure inputs are single numbers (not lists or NaN)
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            print(f"❌ Skipping invalid conversion: lat={lat}, lon={lon}")
            return None, None  # Return None if values are invalid

        # Perform coordinate transformation
        try:
            return self.transformer.transform(lon, lat)
        except Exception as e:
            print(f"⚠️ WGS84 conversion failed for lat={lat}, lon={lon}: {e}")
            return None, None


    def transform_coordinates(self, df: pd.DataFrame, lat_column: str, lon_column: str)-> pd.DataFrame:
        """Convert lat/lon columns to WGS 1984 format and print debugging info."""
        
        print(f"Before WGS 1984 Conversion ({lat_column}, {lon_column}):")
        print(df[[lat_column, lon_column]].dropna().head())

        def safe_convert(row):
            lat, lon = row[lat_column], row[lon_column]

            # Convert lists to single values
            if isinstance(lat, list): lat = lat[0]
            if isinstance(lon, list): lon = lon[0]

            print(f"✅ Passing lat={lat}, lon={lon} to WGS84 conversion")

            if pd.notna(lat) and pd.notna(lon) and isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                return pd.Series(self.convert_to_wgs84(lon, lat))
            return pd.Series([None, None])

        df[[f"{lat_column}_wgs84", f"{lon_column}_wgs84"]] = df.apply(safe_convert, axis=1)

        print(f"After WGS 1984 Conversion ({lat_column}_wgs84, {lon_column}_wgs84):")
        print(df[[f"{lat_column}_wgs84", f"{lon_column}_wgs84"]].dropna().head())

        return df



