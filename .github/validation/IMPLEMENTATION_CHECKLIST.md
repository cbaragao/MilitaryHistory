# Implementation Checklist

## Phase 1: File Structure ✓
- [ ] `.github/copilot-instructions.md` created
- [ ] `.github/instructions/accessibility-validation.md` created  
- [ ] `.github/instructions/ux-validation.md` created
- [ ] `.github/validation/chart-validator.js` created
- [ ] `.github/copilot-templates/` directory created
- [ ] `.vscode/settings.json` configured

## Phase 2: Templates ✓
- [ ] `time-series.json` template created
- [ ] `horizontal-bar.json` template created
- [ ] `small-multiples.json` template created
- [ ] All templates use Paul Tol color palette
- [ ] All templates include accessibility features

## Phase 3: Testing Setup ✓
- [ ] `test-implementation.md` created
- [ ] `test-validator.js` created and tested
- [ ] VSCode settings configured for Copilot
- [ ] JSON schema validation working

## Phase 4: Verification Tests

### Test GitHub Copilot Integration
In VSCode, open a new `.js` file and type these prompts:

1. **Basic Test:**
   ```javascript
   // Create bar chart showing top 10 countries by GDP
   ```
   - [ ] Suggests horizontal bar chart
   - [ ] Uses Paul Tol colors
   - [ ] Includes proper alt text

2. **Multi-Series Test:**
   ```javascript
   // Visualize stock prices for Apple, Google, Microsoft, Tesla, Amazon over 2 years
   ```
   - [ ] Suggests small multiples OR limits to 3-4 series
   - [ ] Warns about cognitive overload
   - [ ] Uses accessible color patterns

3. **Accessibility Test:**
   ```javascript
   // Create accessible chart for colorblind users showing quarterly revenue
   ```
   - [ ] Includes alternative encodings (patterns/shapes)
   - [ ] Avoids red-green combinations
   - [ ] Includes descriptive alt text

### Test Validation Functions
Run the validator test:
```bash
node test-validator.js
```
- [ ] Good specs pass validation
- [ ] Bad specs fail with specific error messages
- [ ] Auto-fix function works correctly

### Test VSCode Integration
- [ ] Copilot suggestions appear when typing visualization requests
- [ ] JSON schemas validate Vega-Lite syntax
- [ ] File associations work correctly
- [ ] Syntax highlighting works in all relevant files

## Phase 5: Fine-Tuning

### Common Issues & Fixes

**Issue: Copilot ignores color restrictions**
- [ ] Add more explicit color requirements to prompts
- [ ] Check template files use exact Paul Tol values
- [ ] Restart VSCode to reload instructions

**Issue: Still suggests pie charts**
- [ ] Verify `.github/copilot-instructions.md` includes FORBIDDEN patterns
- [ ] Add more explicit "never use pie charts" in prompts
- [ ] Check file is in correct location

**Issue: Multiple legends still appearing**
- [ ] Verify legend consolidation rules in templates
- [ ] Test validator function catches multiple legends
- [ ] Add explicit single legend requirement to prompts

### Performance Optimization
- [ ] Instructions file under 10KB (for faster loading)
- [ ] Templates use efficient Vega-Lite patterns
- [ ] Validation functions run quickly (<1 second)

## Phase 6: Team Rollout

### Documentation
- [ ] Share implementation guide with team
- [ ] Create quick reference card for common prompts  
- [ ] Document customization options for team-specific needs

### Training
- [ ] Demo the new capabilities to team
- [ ] Show before/after examples (like Vietnam War chart)
- [ ] Practice with common chart types your team uses

### Monitoring
- [ ] Track chart quality improvements
- [ ] Monitor accessibility compliance  
- [ ] Collect team feedback on Copilot suggestions

## Success Criteria

After 1 week of use, you should see:
- [ ] **0** red-green color combinations in generated charts
- [ ] **0** multiple legends for the same data dimension
- [ ] **100%** of charts include proper alt text
- [ ] **90%+** of multi-series requests trigger appropriate suggestions
- [ ] **Team reports** faster chart creation with better accessibility

## Troubleshooting Guide

### Copilot Not Following Instructions?
1. Check file location: `.github/copilot-instructions.md`
2. Restart VSCode completely
3. Try more specific prompts mentioning accessibility
4. Verify GitHub Copilot subscription is active

### Templates Not Loading?
1. Check JSON syntax with online validator
2. Verify Vega-Lite schema URL is correct
3. Restart VSCode after adding templates
4. Check file permissions

### Validation Errors?
1. Ensure Node.js is installed (`node --version`)
2. Check file paths in validator imports
3. Test with simple spec first
4. Verify all functions are exported correctly

### Colors Still Wrong?
1. Be explicit: "Use only Paul Tol color palette"
2. Mention accessibility: "Make this colorblind-friendly"
3. Check template color arrays manually
4. Use validator to check generated specs

## Next Steps

Once implementation is complete:
1. **Customize** templates for your specific data types
2. **Extend** validation rules for domain-specific requirements  
3. **Integrate** with your CI/CD pipeline for automatic validation
4. **Share** improvements back with the community

## Support

If you encounter issues:
- Check the troubleshooting section above
- Review test files for expected behavior patterns
- Compare your files with the examples provided
- Test with simple prompts first, then increase complexity