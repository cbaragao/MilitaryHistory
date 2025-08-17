// Chart Validation Functions for GitHub Copilot
// Use these functions to validate generated Vega-Lite specifications

const APPROVED_PALETTE = ["#4477AA", "#CC6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"];

const FORBIDDEN_COMBINATIONS = [
  // Red-Green issues
  ['#EE6677', '#228833'], ['#CC6677', '#228833'], ['#FF0000', '#00FF00'],
  // Blue-Yellow issues  
  ['#4477AA', '#CCBB44'], ['#4477AA', '#DDDD77'],
  // Blue-Purple issues
  ['#4477AA', '#AA3377'],
  // Age-related issues
  ['#4477AA', '#666666']
];

/**
 * Main validation function for any Vega-Lite specification
 */
function validateVegaLiteSpec(spec) {
  const results = {
    valid: true,
    errors: [],
    warnings: [],
    suggestions: []
  };

  // UX Validations
  const uxValidation = validateUX(spec);
  if (!uxValidation.valid) {
    results.valid = false;
    results.errors.push(...uxValidation.errors);
  }
  results.warnings.push(...uxValidation.warnings);

  // Accessibility Validations  
  const a11yValidation = validateAccessibility(spec);
  if (!a11yValidation.valid) {
    results.valid = false;
    results.errors.push(...a11yValidation.errors);
  }

  // Color Validations
  const colorValidation = validateColors(spec);
  if (!colorValidation.valid) {
    results.valid = false;
    results.errors.push(...colorValidation.errors);
  }

  return results;
}

/**
 * UX-focused validation
 */
function validateUX(spec) {
  const errors = [];
  const warnings = [];

  // Check for multiple legends
  const legendCount = countLegends(spec);
  if (legendCount > 1) {
    errors.push("Multiple legends detected. Use only one legend per chart.");
  }

  // Check for cognitive overload
  const seriesCount = estimateSeriesCount(spec);
  if (seriesCount > 4 && !hasFaceting(spec)) {
    warnings.push(`${seriesCount} data series detected. Consider using small multiples (faceting) for better clarity.`);
  }

  // Check for proper alt text
  if (!spec.description || !followsCesalFormula(spec.description)) {
    errors.push("Missing or improper alt text. Use Amy Cesal formula: 'Chart type of data type where key insight'");
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Accessibility validation
 */
function validateAccessibility(spec) {
  const errors = [];

  // Check for required alt text
  if (!spec.description) {
    errors.push("Missing description field required for screen readers");
  }

  // Check for color alternatives
  if (hasMultipleCategories(spec) && !hasAlternativeEncodings(spec)) {
    errors.push("Multiple categories detected but no alternative encodings (patterns/shapes) provided");
  }

  // Check for keyboard navigation
  if (!spec.view?.keyboard) {
    errors.push("Missing keyboard navigation support. Add 'view: {keyboard: true}'");
  }

  // Check contrast
  if (!hasProperContrast(spec)) {
    errors.push("Insufficient contrast. Add white stroke borders to marks");
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Color validation for all types of color blindness
 */
function validateColors(spec) {
  const errors = [];
  const colors = extractColors(spec);

  if (!colors || colors.length === 0) return { valid: true, errors: [] };

  // Check against approved palette
  const unapprovedColors = colors.filter(color => !APPROVED_PALETTE.includes(color));
  if (unapprovedColors.length > 0) {
    errors.push(`Unapproved colors detected: ${unapprovedColors.join(', ')}. Use only approved Paul Tol palette.`);
  }

  // Check for forbidden combinations
  const hasForbiddenCombo = FORBIDDEN_COMBINATIONS.some(combo =>
    combo.every(color => colors.includes(color))
  );
  
  if (hasForbiddenCombo) {
    errors.push("Forbidden color combination detected (red-green, blue-yellow, or blue-purple)");
  }

  // Check for too many colors
  if (colors.length > 4) {
    errors.push(`Too many colors (${colors.length}). Maximum 4 colors recommended for cognitive clarity.`);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Helper functions
 */
function countLegends(spec) {
  let count = 0;
  const encoding = spec.encoding || {};
  
  if (encoding.color?.legend !== null && encoding.color?.legend !== false) count++;
  if (encoding.shape?.legend !== null && encoding.shape?.legend !== false) count++;
  if (encoding.strokeDash?.legend !== null && encoding.strokeDash?.legend !== false) count++;
  if (encoding.size?.legend !== null && encoding.size?.legend !== false) count++;
  
  return count;
}

function estimateSeriesCount(spec) {
  if (spec.encoding?.color?.field) {
    // Estimate based on color encoding
    return spec.encoding.color.scale?.range?.length || 4;
  }
  return 1;
}

function hasFaceting(spec) {
  return !!(spec.facet || spec.repeat);
}

function followsCesalFormula(description) {
  // Basic check for Cesal formula: should contain chart type + "where"
  const lowerDesc = description.toLowerCase();
  const hasChartType = ['chart', 'plot', 'graph'].some(type => lowerDesc.includes(type));
  const hasWhere = lowerDesc.includes('where');
  return hasChartType && hasWhere;
}

function hasMultipleCategories(spec) {
  // Check if categorical encoding has multiple values
  const colorField = spec.encoding?.color?.field;
  const shapeField = spec.encoding?.shape?.field;
  return !!(colorField || shapeField);
}

function hasAlternativeEncodings(spec) {
  const encoding = spec.encoding || {};
  const hasColor = !!encoding.color?.field;
  const hasShape = !!encoding.shape?.field;
  const hasStrokeDash = !!encoding.strokeDash?.field;
  
  // If has color categories, should also have shape or pattern
  if (hasColor) {
    return hasShape || hasStrokeDash;
  }
  return true;
}

function hasProperContrast(spec) {
  const mark = spec.mark;
  if (typeof mark === 'object') {
    return !!(mark.stroke && mark.strokeWidth);
  }
  return false;
}

function extractColors(spec) {
  const colors = [];
  const encoding = spec.encoding || {};
  
  if (encoding.color?.scale?.range) {
    colors.push(...encoding.color.scale.range);
  }
  
  if (typeof spec.mark === 'object' && spec.mark.color) {
    colors.push(spec.mark.color);
  }
  
  return [...new Set(colors)]; // Remove duplicates
}

/**
 * Auto-fix function to correct common issues
 */
function autoFixSpec(spec) {
  let fixed = { ...spec };

  // Fix color palette
  if (fixed.encoding?.color?.scale?.range) {
    const colorCount = fixed.encoding.color.scale.range.length;
    fixed.encoding.color.scale.range = APPROVED_PALETTE.slice(0, colorCount);
  }

  // Fix multiple legends
  fixed = consolidateLegends(fixed);

  // Add contrast borders
  if (typeof fixed.mark === 'object') {
    fixed.mark = {
      ...fixed.mark,
      stroke: fixed.mark.stroke || "white",
      strokeWidth: fixed.mark.strokeWidth || 2
    };
  }

  // Add keyboard navigation
  fixed.view = {
    ...fixed.view,
    keyboard: true
  };

  return fixed;
}

function consolidateLegends(spec) {
  const fixed = { ...spec };
  const encoding = fixed.encoding || {};

  // Keep color legend, remove others
  if (encoding.color?.field) {
    if (encoding.shape) {
      encoding.shape = { ...encoding.shape, legend: null };
    }
    if (encoding.strokeDash) {
      encoding.strokeDash = { ...encoding.strokeDash, legend: null };
    }
  }

  return fixed;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    validateVegaLiteSpec,
    autoFixSpec,
    APPROVED_PALETTE,
    FORBIDDEN_COMBINATIONS
  };
}