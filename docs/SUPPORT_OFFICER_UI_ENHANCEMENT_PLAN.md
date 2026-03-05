# Support Officer Processing UI Enhancement Plan

## Overview
Enhance the Support Officer "My Assigned Reports" tab to provide seamless, intuitive processing for three distinct report types with different field requirements.

## Report Types and Their Processing Requirements

### 1. **LOCATE Reports**
**Purpose:** Locate absent parents  
**Required Fields for Completion:**
- Date Case Reviewed
- Results of Review  
- Case Narrated = Yes
- Comment (required for certain outcomes: closed/UNL/NAS/OTHER)

**Common Actions:**
- Cleared BMV/SVES/dockets  
- Contacted CP (custodial parent)
- Closed UNL (2+ years with SSN)
- Closed NAS (6+ months no SSN)

### 2. **P-S Reports**
**Purpose:** Parenting and Support  
**Required Fields for Completion:**
- Action Taken/Status
- Case Narrated = Yes  
- Comment (required if Action = OTHER)

**Common Actions:**
- GT (Genetic Testing)
- ADS (Affidavit of Domestic Service)
- Court Referral
- Contact Letter
- Postal Verification

### 3. **56RA Reports**  
**Purpose:** Establish support orders
**Required Fields for Completion:**
- Date Report was Processed (Date Action Taken)
- Action Taken/Status
- Case Narrated = Yes
- Comment (required if Action = OTHER)

**Common Actions:**
- Scheduled GT
- Pending GTU (GT Unit)
- Prepped ADS
- Pending AHU (Admin Hearing Unit)  
- Referred to Court
- Sent COBO Letter

### 4. **Case Closure Workflow**
**Purpose:** Review cases for potential closure  
**Required Fields for Completion:**
- All Y/N fields (7 questions)
- Initials
- Comments (required if closure NOT proposed)

## UI Enhancement Features

### A. Report Type Detection & Display
✅ Automatically detect report type from data
✅ Display prominent badge/alert with report type
✅ Use color coding:
   - LOCATE: Blue 🔵
   - P-S: Green 🟢  
   - 56RA: Orange 🟠
   - Case Closure: Purple 🟣

### B. Dynamic Required Fields Panel  
✅ Show collapsible panel "Required for This Report Type"
✅ List only relevant fields for current report
✅ Check mark progress as fields are filled
✅ Real-time validation feedback

### C. Improved Column Configuration
✅ Prioritize workflow fields in left columns
✅ Group related fields together
✅ Use clear column headers with tooltips
✅ Disable non-editable fields with visual distinction

### D. Real-Time Validation & Feedback
✅ Inline validation messages per field
✅ Visual indicators (✓ / ⚠️) next to fields  
✅ Prevent "Completed" status if required fields missing
✅ Clear explanation of what's missing

### E. Processing Guidance Enhancements
✅ Contextual help based on report type
✅ Common narration templates visible  
✅ Sample scenarios for each action type
✅ Quick reference guide always accessible

### F. Progress Tracking Improvements
✅ Per-row completion percentage  
✅ Visual progress bar for overall caseload
✅ "Next row" indicator to guide workflow  
✅ Time estimates based on remaining rows

## Implementation Approach

1. **Enhance Report Type Detection** (lines 9290-9310)
   - Add visual badge rendering function
   - Create report-specific color schemes

2. **Create Dynamic Requirements Panel** (after line 9315)
   - Build component that reads report_source
   - Display contextual checklist
   - Show field completion status

3. **Improve Data Editor Configuration** (lines 9420-9530)
   - Optimize column_config with better labels
   - Add help text to dropdowns
   - Implement conditional formatting

4. **Add Real-Time Validation** (lines 9620-9680)
   - Check fields as user edits
   - Display inline warnings
   - Guide user to missing requirements

5. **Enhance Guidance Panel** (lines 9530-9600)
   - Make context-sensitive
   - Add visual examples  
   - Include quick-copy text templates

## Success Metrics

✅ Workers can instantly identify report type  
✅ Required fields are always clear
✅ Validation happens before attempted completion
✅ Processing time per row decreases  
✅ Error rate decreases (incomplete submissions)
✅ Worker satisfaction increases

## Testing Checklist

- [ ] Test with sample LOCATE report
- [ ] Test with sample P-S report  
- [ ] Test with sample 56RA report
- [ ] Test with Case Closure workflow
- [ ] Verify validation prevents invalid completions
- [ ] Confirm all templates are accurate
- [ ] Test with multiple simultaneous reports
- [ ] Validate session state persistence

## Rollout Plan

1. **Phase 1:** Visual indicators and required fields panel
2. **Phase 2:** Real-time validation  
3. **Phase 3:** Enhanced guidance and templates
4. **Phase 4:** Progress tracking improvements
5. **Phase 5:** User feedback and iteration
