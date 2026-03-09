# QA System Testing - Fix for "Not Assigned as Supervisor" Message

## Problem
You selected "Supervisor" role but the app shows:
> "You are not assigned as a supervisor for any unit. QA review is available to unit supervisors."

## Solution: Use Auto-Created Demo Supervisors

When the app initializes, it automatically creates demo units with supervisors. Here's how to use them:

---

## QUICK FIX - 3 Steps

### Step 1: Switch Back to Support Officer
- Change role back to **"Support Officer"**
- Note the **Unit name** (e.g., "Establish Unit 1")

### Step 2: Process and Submit a Report
- Select any support officer (e.g., "Establish Unit 1 Support Officer 1")
- Process some cases and mark them "Completed"
- Click **"✅ Submit Caseload as Complete"**
- Confirm you see: "🎯 QA samples automatically generated"

### Step 3: Switch to the Correct Supervisor
- Change role to **"Supervisor"**
- In the "Act as Supervisor" dropdown, look for a name matching your unit
- **Pattern:** `[Unit Name] Supervisor`
  - Example: "Establish Unit 1 Supervisor"
  - Or: "Locate Unit 1 Supervisor"
- Select that supervisor name
- Now the "🎯 QA Review" tab should work!

---

## Where to Find Supervisor Names

### In the Sidebar:
1. Change to **"Supervisor"** role
2. Look at the "Act as Supervisor / Team Lead" dropdown
3. You'll see auto-created names like:
   - "Establish Unit 1 Supervisor"
   - "Establish Unit 2 Supervisor"
   - "Locate Unit 1 Supervisor"
   - "Parenting Unit 1 Supervisor"
   - etc.

### Naming Pattern:
```
[Department] Unit [Number] Supervisor

Examples:
- "Establish Unit 1 Supervisor"    (Establishment department)
- "Locate Unit 2 Supervisor"       (Locate department)
- "Parenting Unit 1 Supervisor"    (Parenting/Support department)
```

---

## Full QA Testing Workflow

### 1️⃣ Process Cases (Support Officer)

```
Role: Support Officer
Unit: Establish Unit 1
Worker: Establish Unit 1 Support Officer 1
```

- Go to "📝 My Assigned Reports"
- Process at least 5 cases (mark as "Completed")
- Submit: Click "✅ Submit Caseload as Complete"
- ✅ See: "🎯 QA samples automatically generated"

### 2️⃣ Review QA Samples (Supervisor)

```
Role: Supervisor
Supervisor: Establish Unit 1 Supervisor
```

- Go to new tab: "🎯 QA Review"
- Select the report you just submitted
- Select worker "Establish Unit 1 Support Officer 1"
- You'll see: "🎯 QA Sample: Establish Unit 1 Support Officer 1"
- "5 of [N] cases selected (X% sample rate)"

### 3️⃣ Review Individual Cases Against Ohio Compliance

- Select one sampled case
- System shows:
  - **Compliance Score** (auto-calculated)
  - **Criteria Checklist** (Ohio OAC/ORC/OCSE requirements)
  - **✅ Passed** / **❌ Failed** marks for each criterion
- Add reviewer notes
- Click "💾 Save QA Review"
- Repeat for other sampled cases

### 4️⃣ View Executive Dashboard (Director)

```
Role: Director
```

- Go to new tab: "🎯 QA & Compliance"
- See:
  - **Total cases reviewed** (aggregated from all supervisors' reviews)
  - **Avg Compliance Score** (agency-wide)
  - **Pass Rate** (% of cases ≥75%)
  - **Compliance by Category** (chart of Ohio criteria performance)
  - **Top Issues** (most common failures)
  - **Strategic Insights** (wins and action items)

---

## Troubleshooting

### Message: "No QA reviews completed yet"
**In Director's QA & Compliance tab**
- ✅ **Normal** - means no supervisor has reviewed any cases yet
- **Solution:** Complete more QA reviews as a supervisor first

### Message: "No reports with QA samples available yet"
**In Supervisor's QA Review tab**
- ✅ **Normal** - means no submitted reports yet
- **Solution:** 
  1. Switch to Support Officer
  2. Process cases and submit a report
  3. Come back to Supervisor view

### Can't find Supervisor role dropdown
- **Make sure you're using Supervisor role** (not Support Officer)
- Check "Act as Supervisor / Team Lead" dropdown on left sidebar
- It might be below the report selector

### Supervisor dropdown shows "(Select)"
- This means no supervisors have been created yet
- **Solution:** Reload the page (⌘R or Ctrl+R)
- Wait for app to initialize demo data

---

## What You'll See - Real Examples

### QA Sample Badge (Supervisor View)
```
┌────────────────────────────────────────┐
│ 🎯 QA Sample: Establish Unit 1 Support │
│             Officer 1                   │
│                                        │
│ 5 of 25 cases selected (20% sample     │
│ rate)                                   │
└────────────────────────────────────────┘
```

### Compliance Score Card
```
┌────────────────────────────────────────┐
│ ✅                                      │
│ 87%                                     │
│ Acceptable                              │
│ Score: 87 / 100 points                 │
└────────────────────────────────────────┘
```

### Criteria Checklist (56RA Example)
```
✅ EST-01: Service Requirements
   Requirement: Proper service (ADS, personal, certified mail)
   Regulation: Ohio OAC 5101:12-45-03(C)
   Weight: 20 points
   ✓ Passed: Found 'ADS' in Action Taken

❌ EST-02: Genetic Testing
   Requirement: GT scheduled within 30 days of PCR filing
   Regulation: Ohio ORC 3111.04(A)(1)
   Weight: 25 points
   ✗ Failed: GT not found in Action Taken field
```

---

## Demo Unit Names (Based on Department)

### Establishment Department
- "Establish Unit 1 Supervisor"
- "Establish Unit 2 Supervisor"
- "Establish Unit 3 Supervisor"
- "Establish Unit 4 Supervisor"
- "Establish Unit 5 Supervisor"

### Locate Department
- "Locate Unit 1 Supervisor"
- "Locate Unit 2 Supervisor"
- "Locate Unit 3 Supervisor"
- "Locate Unit 4 Supervisor"
- "Locate Unit 5 Supervisor"

### Parenting/Support Department
- "Parenting Unit 1 Supervisor"
- "Parenting Unit 2 Supervisor"
- "Parenting Unit 3 Supervisor"
- "Parenting Unit 4 Supervisor"
- "Parenting Unit 5 Supervisor"

---

## Quick Testing Checklist

- [ ] **Step 1:** Select Support Officer role
- [ ] **Step 2:** Process 5+ cases using Quick-Copy templates (Phase 1 UI)
- [ ] **Step 3:** Mark all cases "Completed"
- [ ] **Step 4:** Click "Submit Caseload as Complete"
- [ ] **Step 5:** Confirm "🎯 QA samples automatically generated" message
- [ ] **Step 6:** Switch to Supervisor role
- [ ] **Step 7:** Select "[Unit] Supervisor" from dropdown
- [ ] **Step 8:** See "🎯 QA Review" tab (NEW!)
- [ ] **Step 9:** Select report with QA samples
- [ ] **Step 10:** Select worker and review sampled case
- [ ] **Step 11:** See compliance score and criteria checklist
- [ ] **Step 12:** Add reviewer notes and save
- [ ] **Step 13:** Switch to Director role
- [ ] **Step 14:** See "🎯 QA & Compliance" tab (NEW!)
- [ ] **Step 15:** View agency-wide metrics and compliance trends ✅

---

## Next Steps

Once you've successfully tested the workflow:

1. ✅ Supervisor QA Review tab shows cases
2. ✅ Compliance scoring works (color-coded cards)
3. ✅ Director sees aggregated metrics

Then you can:
- Review the [QA_COMPLIANCE_SYSTEM_COMPLETE.md](QA_COMPLIANCE_SYSTEM_COMPLETE.md) documentation
- Check the [Ohio compliance criteria](QA_COMPLIANCE_SYSTEM_COMPLETE.md#ohio-compliance-criteria) reference
- See [future enhancements](QA_COMPLIANCE_SYSTEM_COMPLETE.md#future-enhancements-phase-2) planned for Phase 2

---

**Still stuck?** Try these troubleshooting steps:

1. **Reload page**: ⌘R (Mac) or Ctrl+R (Windows)
2. **Check browser console**: F12 → Console for any errors
3. **Verify app is running**: http://localhost:8501 should load
4. **Try different unit**: Some units might not have demo cases yet

**Questions?** See [QA_DEMO_WALKTHROUGH.md](QA_DEMO_WALKTHROUGH.md) for detailed step-by-step guide.
