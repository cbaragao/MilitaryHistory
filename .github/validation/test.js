// Create an accessible bar chart showing top 5 countries by population, avoiding red-green colors

const chartSpec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Top 5 Countries by Population (2023)",
    "subtitle": "Population in billions - China and India lead with over 1.4 billion each",
    "fontSize": 16,
    "fontWeight": "bold",
    "anchor": "start",
    "color": "#333333",
    "font": "Arial, sans-serif"
  },
  "description": "Horizontal bar chart of population by country where China leads with 1.425 billion people, followed closely by India at 1.428 billion, showing the demographic dominance of these two nations",
  "width": 600,
  "height": 300,
  "data": {
    "values": [
      {"country": "China", "population": 1.425, "rank": 1},
      {"country": "India", "population": 1.428, "rank": 2},
      {"country": "United States", "population": 0.339, "rank": 3},
      {"country": "Indonesia", "population": 0.277, "rank": 4},
      {"country": "Pakistan", "population": 0.240, "rank": 5}
    ]
  },
  "mark": {
    "type": "bar",
    "color": "#4477AA",
    "stroke": "#FFFFFF",
    "strokeWidth": 1,
    "cornerRadiusEnd": 3
  },
  "encoding": {
    "y": {
      "field": "country",
      "type": "nominal",
      "sort": {"field": "population", "order": "descending"},
      "axis": {
        "title": null,
        "labelFont": "Arial, sans-serif",
        "labelFontSize": 12,
        "labelColor": "#333333",
        "domain": false,
        "ticks": false
      }
    },
    "x": {
      "field": "population",
      "type": "quantitative",
      "scale": {"domain": [0, 1.5]},
      "axis": {
        "title": "Population (Billions)",
        "titleFont": "Arial, sans-serif",
        "titleFontSize": 12,
        "titleColor": "#333333",
        "labelFont": "Arial, sans-serif",
        "labelFontSize": 11,
        "labelColor": "#666666",
        "grid": true,
        "gridColor": "#E0E0E0",
        "gridOpacity": 0.5,
        "domain": true,
        "domainColor": "#333333"
      }
    },
    "tooltip": [
      {"field": "country", "type": "nominal", "title": "Country"},
      {"field": "population", "type": "quantitative", "title": "Population (Billions)", "format": ".3f"},
      {"field": "rank", "type": "ordinal", "title": "Global Rank"}
    ]
  },
  "config": {
    "view": {"stroke": null},
    "axis": {
      "labelFont": "Arial, sans-serif",
      "titleFont": "Arial, sans-serif"
    }
  }
};

// Export the chart specification
export default chartSpec;