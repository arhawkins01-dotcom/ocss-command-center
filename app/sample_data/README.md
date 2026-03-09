# Sample Data for OCSS Command Center

## Overview

Sample demonstration data files for testing the OCSS Command Center with realistic child support case data.

---

## Demo Reports by Type

### 1. **LOCATE Reports** (`sample_locate_report.csv/.xlsx`)

Locating/finding non-custodial parents (NCPs) for establishment of support.

**Key Fields:**
- Case Number, NCP/CP Names
- Current Location (Address, City, State, ZIP)
- Locate Status (LOCATED, PARTIALLY LOCATED, IN PROGRESS)
- Locate Method (Employment Search, DMV, Federal Match, Social Media, etc.)
- Employment Information & Verification Status
- Phone Number  
- Review Comments & QA Flags

**Sample Data Scenarios:**
- 8 successfully located cases
- 1 case partially located (awaiting address)
- 1 inactive case with previous location
- Range of locate methods and success rates

**Compliance References:**
- ORC 3125.25 (Locating Non-Custodial Parents)
- OAC 5101:12-1-50 (Location Services)
- OCSE AT-08-01 (Locate Service Performance)

---

### 2. **56RA/56 Support Enforcement Reports** (`sample_56ra_report.csv/.xlsx`)

Support order enforcement and collection tracking.

**Key Fields:**
- Case Number, NCP/CP Names, Child Info
- Support Order Amount & Collection Frequency
- Monthly Collection Target vs Actual Collections
- Collection Rate & Year-to-Date Results
- Last Payment Date & Payment Method
- Enforcement Action Status (None, Payment Plan, Wage Withholding, Levy, etc.)
- Arrears Amount & Compliance Status
- Court Order Details

**Sample Data Scenarios:**
- 3 cases with 100% compliance
- 5 cases under 75% compliance (various enforcement actions)
- 1 case with contempt filing
- 1 inactive case with warrant issued
- Multiple enforcement methods (wage withholding, bank levy, payment plans)

**Compliance References:**
- ORC 3119.05 (Support Order Enforcement)
- ORC 3119.26 (Wage Withholding)
- OAC 5101:12-45-03 (Support Collection)
- OCSE AT-06-02 (Support Order Enforcement)

---

### 3. **P-S/PS Paternity/Support Establishment** (`sample_ps_report.csv/.xlsx`)

Paternity testing and support order establishment proceedings.

**Key Fields:**
- Case Number, Child/Mother/Alleged Father Names
- Paternity Status (ESTABLISHED, PENDING, CONTESTED)
- Genetic Testing Status & Lab Results
- Paternity Test Results (% Probability or Exclusion)
- Support Order Amount & Date
- Order Type (Court Ordered, Agreed, Voluntary Acknowledgment, Contested)
- Legal Action & Court Order Status
- Financial Obligation Agreement

**Sample Data Scenarios:**
- 6 established paternity cases
- 1 pending case awaiting genetic test return
- 2 contested cases with court hearings scheduled
- 1 case excluded by genetic testing
- Range: Voluntary acknowledgments through court-ordered actions

**Compliance References:**
- ORC 3111.04 (Paternity Establishment)
- ORC 3119.04 (Support Order Establishment)
- OAC 5101:12-1-30 (Paternity Establishment)
- OCSE PIQ-06-02 (Paternity Establishment Performance)

---

## Using Sample Data

### Option 1: CSV Files
Upload directly to the OCSS Command Center via the "Report Intake Portal" → "Upload Establishment Report"

### Option 2: Excel Files
Pre-formatted with proper columns; recommended for better data integrity

### To Generate Excel Files
```bash
python app/sample_data/create_excel_samples.py
```

---

## Data Dictionary

### Common Fields (All Report Types)

| Field | Type | Description |
|-------|------|-------------|
| Case Number | String | Unique identifier (format: C-[TYPE]-[XXX]) |
| Status | String | ACTIVE, PENDING, INACTIVE, CONTESTED |
| QA Flag | Y/N | Marked for quality assurance review |
| Review Date | Date | Last QA review date |
| Reviewer Name | String | Person who conducted QA review |

### LOCATE-Specific
- Locate Status: LOCATED, PARTIALLY LOCATED, IN PROGRESS
- Locate Method: Employment Search, DMV, Federal Match, etc.
- Employment Verified: Yes/No

### 56RA-Specific  
- Collection Rate: Percentage of ordered amount collected
- Enforcement Action: None, Payment Plan, Wage Withholding, Levy, Contempt, etc.
- Arrears Amount: Total unpaid support

### P-S-Specific
- Paternity Status: ESTABLISHED, PENDING, CONTESTED
- Genetic Testing: COMPLETED, IN PROGRESS, REQUESTED
- Test Results: % Probability (99.9%+) or EXCLUSION

---

## QA Test Cases

The sample data includes intentional scenarios for QA testing:

✅ **LOCATE Report:**
- Flag: Case C-LOCATE-003 (partial locate - address pending)
- Flag: Case C-LOCATE-006 (multi-agency search ongoing)
- Flag: Case C-LOCATE-009 (inactive with unknown employment)

✅ **56RA Report:**
- Flag: Case C-56RA-002 (67% compliance - payment plan established)
- Flag: Case C-56RA-003 (75% compliance - new withholding order)
- Flag: Case C-56RA-005 (67% compliance - arrears enforcement)
- Flag: Case C-56RA-007 (67% compliance - bank levy initiated)
- Flag: Case C-56RA-009 (0% compliance - contempt filing)
- Flag: Case C-56RA-010 (50% compliance - escalation recommended)

✅ **P-S Report:**
- Flag: Case C-PS-002 (pending - awaiting response)
- Flag: Case C-PS-003 (contested - excluded by genetics)
- Flag: Case C-PS-006 (pending - testing kit mailed)
- Flag: Case C-PS-009 (contested - hearing pending)

---

## Ohio Compliance Criteria

These sample reports map to the 24 Ohio compliance criteria implemented in the QA system:

**LOCATE (6 criteria):**
1. Timely locate initiation
2. Method appropriateness
3. Information accuracy
4. Employment verification
5. Address validation
6. Documentation completeness

**56RA (6 criteria):**
1. Order amount calculation
2. Collection rate (target: 60%+)
3. Enforcement action timeliness
4. Payment recording
5. Arrears management
6. Compliance documentation

**P-S (6 criteria):**
1. Genetic testing timeliness
2. Paternity establishment
3. Order calculation accuracy
4. Support amount appropriateness
5. Court order documentation
6. Case closure timeliness

**CASE_CLOSURE (6 criteria):**
1. Closure reason appropriateness
2. Final payment confirmation
3. Arrears resolution
4. Case file completeness
5. Closure documentation
6. Closure timing

---

## Test Workflow

1. **Upload Sample Report**
   - Go to: Program Officer → Report Intake Portal
   - Upload: `sample_locate_report.xlsx` (or CSV)
   - Select: Caseload 181000 Downtown Establishment

2. **View in Support Officer Dashboard**
   - Support Officer → My Assigned Reports
   - See the uploaded report data

3. **QA Review (Supervisor)**
   - Supervisor → QA Review tab
   - See auto-sampled cases (5 per worker per report type)
   - Review against 24 Ohio compliance criteria
   - Mark passed/failed per criterion

4. **Director Dashboard**
   - Director → QA & Compliance tab
   - View agency-wide compliance metrics
   - See trends by report type
   - Identify low-performing workers

---

## Notes for Test Data

- **Personal Information**: All names are randomized; no real individuals
- **Financial Data**: Amounts realistic for Ohio child support orders
- **Dates**: All relative to current date for realistic scenarios
- **Status Distributions**: 70-80% success cases, 20-30% QA flag cases

---

## Regenerating Sample Data

To update or modify sample data:

1. Edit CSV files directly in Excel or text editor
2. Run: `python create_excel_samples.py` to regenerate XLSXfiles
3. Commit to git: `git add sample_*.csv *.xlsx && git commit`

---

**Created**: March 6, 2026  
**OCSS Command Center v1.4.0+**  
**Ohio Child Support Services**
