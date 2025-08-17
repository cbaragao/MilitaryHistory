# Testing Your Copilot Implementation

## Quick Test Commands

### Test 1: Basic Chart Generation
**In any `.js` or `.md` file, type:**
```
// Create a horizontal bar chart showing top 5 countries by population
```
**Expected:** Copilot should suggest using the horizontal bar template with Paul Tol colors.

### Test 2: Multi-Series Data
**Type:**
```
// Visualize quarterly sales data for 6 different product lines over 3 years
```
**Expected:** Copilot should suggest small multiples (faceting) instead of overlapping lines.

### Test 3: Color Validation  
**Type:**
```javascript
const badColors = ["#FF0000", "#00FF00"]; // This should trigger validation
```
**Expected:** Copilot should warn about red-green combination.

### Test 4: Accessibility Check
**Type:**
```
// Create accessible time series chart with proper alt text
```
**Expected:** Should include Amy Cesal formula alt text and alternative encodings.

## Validation Tests

### Test Your Validator Function
Create `test-validator.js`:

```javascript
const { validateVegaLiteSpec } = require('./.github/validation/chart-validator.js');

// Test 1: Good specification
const goodSpec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "Bar chart of sales data where Q4 shows highest revenue",
  "mark": {
    "type": "bar",
    "stroke": "white",
    "strokeWidth": 2
  },
  "encoding": {
    "x": {"field": "quarter", "type": "nominal"},
    "y": {"field": "sales", "type": "quantitative"},
    "color": {
      "field": "quarter",
      "scale": {"range": ["#4477AA", "#CC6677", "#228833", "#CCBB44"]}
    }
  },
  "view": {"keyboard": true}
};

console.log("Good spec validation:", validateVegaLiteSpec(goodSpec));

// Test 2: Bad specification (multiple issues)
const badSpec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "mark": "bar",
  "encoding": {
    "x": {"field": "quarter", "type": "nominal"},
    "y": {"field": "sales", "type": "quantitative"},
    "color": {
      "field": "quarter",
      "scale": {"range": ["#FF0000", "#00FF00"]}, // Red-green issue
      "legend": {"title": "Quarter"}
    },
    "shape": {
      "field": "quarter", 
      "legend": {"title": "Quarter"} // Duplicate legend
    }
  }
};

console.log("Bad spec validation:", validateVegaLiteSpec(badSpec));
```

Run: `node test-validator.js`

## Copilot Prompt Testing

### Test Prompts (Use in VSCode)

1. **Simple Request:**
   ```
   Create a Vega-Lite bar chart showing company revenues
   ```

2. **Complex Request:**
   ```
   I need to visualize monthly website traffic for 8 different pages over 2 years
   ```

3. **Accessibility-Focused:**
   ```
   Generate accessible line chart for screenreader users showing temperature trends
   ```

4. **Color-Specific:**
   ```
   Create chart with red and green colors for comparison
   ```

## Expected Behaviors

### ✅ What Should Happen:
- Copilot suggests templates from `.github/copilot-templates/`
- Colors automatically use Paul Tol palette
- Multi-series data triggers small multiples suggestion
- Alt text follows Amy Cesal formula
- Single legend maximum
- Red-green combinations avoided

### ❌ What Should NOT Happen:
- Pie charts suggested
- More than 4 colors in single chart
- Multiple legends for same data
- Red-green color combinations
- Missing alt text
- Color-only data distinction

## Troubleshooting

### If Copilot Ignores Instructions:
1. Check file is in correct location (`.github/copilot-instructions.md`)
2. Restart VSCode
3. Try more specific prompts
4. Check GitHub Copilot settings are enabled

### If Validation Fails:
1. Ensure Node.js is installed
2. Check file paths in validator
3. Verify JSON syntax in templates

### If Colors Still Wrong:
1. Be more explicit in prompts: "Use Paul Tol color palette"
2. Check template files use correct color arrays
3. Manually specify colors in requests

## Success Metrics

Track these over a week of use:
- [ ] 0 red-green combinations generated
- [ ] 0 multiple legends for same dimension  
- [ ] All charts include proper alt text
- [ ] Complex data triggers small multiples suggestion
- [ ] Horizontal bars suggested for rankings