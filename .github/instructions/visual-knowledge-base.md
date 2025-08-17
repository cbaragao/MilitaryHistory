---
priority: 2
description: "Visual knowledge base referencing proven accessible examples"
applyTo: "**/*.{js,ts,json}"
---

# Visual Knowledge Base

## Purpose

This knowledge base catalogs proven, accessible visualizations from `/visuals/` directory. Use these as references and inspiration for new visualizations that maintain accessibility excellence.

## How to Use This Knowledge Base

**When creating new visualizations:**
1. **Identify similar data patterns** in your new request
2. **Reference appropriate example** from catalog below
3. **Adapt proven techniques** to your new data
4. **Maintain accessibility standards** from the examples

## Catalog of Proven Examples

### 1. Heat Map Analysis
**File**: `1968_search_and_destroy_gors.json`
**Use for**: Time-based pattern analysis, intensity mapping, categorical distributions

**Key Features**:
- **Heat map with ordinal binning** for clear intensity levels
- **CVD-safe color scheme**: Single-hue progression (`#f7fbff` to `#4477AA`)
- **Clear categorical axes** with proper sorting
- **Comprehensive alt text** with tactical insights
- **Professional styling** with consistent typography

**Accessibility Patterns**:
```json
{
  "mark": {
    "type": "rect", 
    "stroke": "white",
    "strokeWidth": 2
  },
  "encoding": {
    "color": {
      "scale": {"scheme": "blues", "range": ["#f7fbff", "#4477AA"]},
      "legend": {"gradientLength": 300}
    },
    "opacity": {
      "condition": {"test": "datum.mission_count > 0", "value": 1},
      "value": 0.1
    }
  }
}
```

**Reusable Techniques**:
- Binning continuous data for categorical display
- Using opacity to handle missing/zero values
- White stroke borders for clear cell definition

### 2. Multi-Panel Dashboard  
**File**: `conga_firing_missions.json`
**Use for**: Complex datasets requiring multiple view types, geographic + statistical analysis

**Key Features**:
- **Geographic visualization** with proportional symbols
- **Horizontal bar chart** for rankings (accessibility best practice)
- **Scatterplot analysis** with size encoding
- **Coordinated color schemes** across panels
- **Independent scale resolution** between charts

**Accessibility Patterns**:
```json
{
  "vconcat": [...],
  "resolve": {
    "scale": {
      "color": "independent",
      "size": "independent"  
    }
  },
  "encoding": {
    "color": {
      "scale": {"range": ["#4477AA", "#CC6677", "#66CCEE"]},
      "legend": {"orient": "right"}
    }
  }
}
```

**Reusable Techniques**:
- Multi-panel layouts with `vconcat`
- Consistent color palette across panels
- Right-oriented legends for dashboard layout
- Geographic + statistical view combinations

### 3. Multi-Line Time Series
**File**: `vietnam-air-missions-updated.json`  
**Use for**: Temporal trends with multiple data series, comparative analysis over time

**Key Features**:
- **CVD-safe color palette** with stroke patterns
- **Point markers** with white outlines for clarity
- **Proper temporal axis** formatting
- **Amy Cesal alt text** formula implementation
- **Comprehensive tooltips** with formatting

**Accessibility Patterns**:
```json
{
  "mark": {
    "type": "line",
    "point": {
      "filled": true,
      "stroke": "white", 
      "strokeWidth": 2
    },
    "strokeWidth": 3
  },
  "encoding": {
    "color": {
      "scale": {"range": ["#4477AA", "#CC6677", "#AA3377", "#66CCEE"]},
      "legend": {"symbolStrokeWidth": 2, "symbolStrokeColor": "white"}
    },
    "strokeDash": {
      "scale": {"range": [[1,0], [5,5], [10,5], [15,5,5,5]]},
      "legend": null
    }
  }
}
```

**Reusable Techniques**:
- Stroke patterns as color alternatives
- Point markers with contrast borders
- Legend styling for accessibility
- Temporal axis with year formatting

## Common Accessibility Patterns Across All Examples

### Color Safety
```json
{
  "color": {
    "scale": {
      "range": ["#4477AA", "#CC6677", "#66CCEE", "#AA3377", "#BBBBBB"]
    }
  }
}
```

### Alternative Encodings
```json
{
  "strokeDash": {
    "scale": {"range": [[1,0], [5,5], [10,5], [15,5,5,5]]},
    "legend": null
  }
}
```

### Professional Styling
```json
{
  "config": {
    "view": {"stroke": null},
    "axis": {
      "labelFont": "Arial",
      "titleFont": "Arial", 
      "gridColor": "#E5E5E5"
    },
    "title": {
      "font": "Arial",
      "fontWeight": "bold"
    }
  }
}
```

## Data Processing Patterns

### Temporal Data Handling
```json
{
  "transform": [
    {
      "calculate": "datetime(split(datum.year_month, '-')[0], split(datum.year_month, '-')[1] - 1, 1)",
      "as": "date"
    }
  ]
}
```

### Ranking and Filtering
```json
{
  "transform": [
    {
      "window": [{"op": "rank", "as": "rank"}],
      "sort": [{"field": "value", "order": "descending"}]
    },
    {"filter": "datum.rank <= 10"}
  ]
}
```

### Binning for Categories
```json
{
  "transform": [
    {
      "calculate": "datum.mission_count > 200 ? '200+' : datum.mission_count >= 150 ? '150-199' : ...",
      "as": "intensity_bin"
    }
  ]
}
```

## Usage Guidelines

### When to Reference Each Example

**Use Heat Map Pattern for**:
- Time-of-day analysis
- Geographic distribution grids
- Intensity/frequency analysis
- Matrix-style data

**Use Dashboard Pattern for**:
- Complex datasets with multiple dimensions
- Geographic + statistical combinations
- Executive summary views
- Multi-aspect analysis

**Use Time Series Pattern for**:
- Temporal trends (primary use case)
- Comparative analysis over time
- Mission/activity tracking
- Multi-country/multi-unit comparisons

### Adaptation Guidelines

1. **Keep accessibility features** - never remove stroke patterns, colors, or alt text
2. **Adapt data transforms** - modify calculations for your specific data structure
3. **Maintain styling consistency** - use the same fonts, colors, spacing
4. **Update content appropriately** - change titles, labels, tooltips for your data

## Quality Standards from Examples

**Every visualization should have**:
- Insight-focused titles with context
- Amy Cesal formula alt text descriptions
- CVD-safe color combinations
- Alternative encodings (patterns/shapes)
- Professional typography and styling
- Comprehensive tooltips
- Proper axis labeling and formatting

**Reference these examples when Copilot needs guidance on**:
- Complex data transformations
- Multi-panel layouts
- Accessibility implementation
- Professional styling standards
- Tooltip and interaction design