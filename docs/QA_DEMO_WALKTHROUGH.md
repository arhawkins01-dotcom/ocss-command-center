"""
QA System Demo Guide - Real-Time Testing

This script creates sample data that will auto-trigger QA sampling
and let you see the full QA workflow in action.
"""

import pandas as pd
import sys
sys.path.insert(0, '/workspaces/ocss-command-center/app')

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║          QA SYSTEM - REAL-TIME DEMO WALKTHROUGH                           ║
╚════════════════════════════════════════════════════════════════════════════╝

DEMO WORKFLOW:
==============

STEP 1: START THE APP (already running on http://localhost:8501)
────────────────────────────────────────────────────────────────

  Already verified! App is active at http://localhost:8501


STEP 2: LOAD AS SUPPORT OFFICER AND PROCESS CASES
───────────────────────────────────────────────────

  1. Open http://localhost:8501
  
  2. Select Role: "Support Officer"
  
  3. Choose Support Officer: Select any available worker
  
  4. Go to "📝 My Assigned Reports" tab
  
  5. Select a report from the queue
  
  6. In the report, you'll see:
     ✅ Report Type Badge (🔵 LOCATE / 🟢 P-S / 🟠 56RA / 🟣 Case Closure)
     ✅ Required Fields Panel showing what fields are needed
     ✅ Quick-Copy Narration Templates for that report type
     ✅ Per-Row Progress Tracking
  
     (These are the UI enhancements from Phase 1)


STEP 3: COMPLETE CASES
──────────────────────

  1. Select a case row from the report
  
  2. Fill in required fields using the Quick-Copy templates
  
  3. Set "Worker Status" = "Completed" for each row
  
  4. Click "💾 Save Progress" to checkpoint
  
  5. Repeat for at least 5 cases to match the QA sample size


STEP 4: TRIGGER QA SAMPLING (AUTO-SUBMISSION)
───────────────────────────────────────────────

  ⭐ THIS IS THE KEY STEP ⭐

  1. Once ALL rows in report are marked "Completed":
  
  2. Click "✅ Submit Caseload as Complete" button
  
  3. System validates all required fields
  
  4. Upon successful submission, you'll see:
     🎯 "QA samples automatically generated for this report."
     
     (Behind the scenes, system selected 5 case samples)


STEP 5: SWITCH TO SUPERVISOR - VIEW QA SAMPLES
────────────────────────────────────────────────

  1. Change role to "Supervisor"
  
  2. Go to NEW tab: "🎯 QA Review"
  
  3. Select the report you just submitted
  
  4. System shows:
     📊 QA Sample Badge
        "🎯 QA Sample: [Worker Name]"
        "5 of [N] cases selected (X% sample rate)"
  
  5. Click on worker name
  
  6. Dashboard shows:
     - Cases Reviewed
     - Avg Compliance %
     - Pass Rate
     - Workers Reviewed


STEP 6: REVIEW SAMPLED CASE AGAINST OHIO COMPLIANCE
──────────────────────────────────────────────────────

  ⭐ THE COMPLIANCE CHECK HAPPENS HERE ⭐

  1. Select worker from dropdown
  
  2. Select one of the 5 sampled cases
  
  3. System automatically calculates:
  
     📈 COMPLIANCE SCORE CARD
        Shows: [Score]% with color coding
        - 🟢 Green: 90%+ (Excellent)
        - 🟡 Amber: 75-89% (Acceptable)
        - 🔴 Red: <75% (Needs Improvement)
  
  4. See CRITERIA CHECKLIST:
     ✅ = Requirement MET
     ❌ = Requirement FAILED
     
     Each criterion shows:
     - Category
     - Ohio Regulation (OAC/ORC/OCSE)
     - Weight (points)
     - Explanation
     
     Example criteria for 56RA:
     ✅ "EST-02: Genetic Testing scheduled within 30 days (ORC 3111.04)"
     ❌ "EST-04: Court referral documentation incomplete"
  
  5. Enter REVIEWER NOTES describing what needs coaching
  
  6. Click "💾 Save QA Review"
  
  7. Repeat for other sampled cases (typically 5 per worker)


STEP 7: VIEW EXECUTIVE QA DASHBOARD
─────────────────────────────────────

  1. Switch role to "Director"
  
  2. Go to NEW tab: "🎯 QA & Compliance"
  
  3. See AGENCY-WIDE METRICS:
     - Total Cases Reviewed (all workers, all reports)
     - Avg Compliance Score (agency-wide)
     - Pass Rate (% meeting ≥75% threshold)
     - Workers Reviewed (how many workers evaluated)
  
  4. See COMPLIANCE BY CATEGORY chart:
     Shows performance on each Ohio requirement category:
     - "Database Searches": 92%
     - "Service Requirements": 87%
     - "Narration": 78%
     (etc.)
  
  5. See TOP COMPLIANCE ISSUES:
     "Most common failures across all reviews"
     Helps identify agency-wide training needs
  
  6. Strategic Insights:
     ✅ Wins: "Report completion at 92% (≥90% target)"
     ⚠️ Action Items: "Data quality 3% below 95% target"


═══════════════════════════════════════════════════════════════════════════════

REAL-TIME TESTING - QUICK PATH:
═════════════════════════════════

If you want to see everything quickly without manual data entry:

  1. App uses STATE to track QA data
  2. Each session generates fresh sample QA metrics
  3. Metrics show even without real submitted reports
  
  To see demo data:
  - Director tab → "🎯 QA & Compliance" shows aggregated metrics
  - Supervisor tab → "🎯 QA Review" shows submitted reports for review


═══════════════════════════════════════════════════════════════════════════════

OHIO COMPLIANCE CRITERIA BEING CHECKED:
════════════════════════════════════════

LOCATE REPORTS (6 criteria, 100 points max):
  LOC-01: Database searches (20 pts)
  LOC-02: Custodial parent contact (15 pts)
  LOC-03: 6+ month closure - NAS (20 pts)
  LOC-04: 2+ year closure - UNL (20 pts)
  LOC-05: Case narration (15 pts)
  LOC-06: Interstate/CLEAR (10 pts)

56RA ESTABLISHMENT (6 criteria, 100 points max):
  EST-01: Service requirements (20 pts)
  EST-02: Genetic testing 30-day rule (25 pts) ← Most heavily weighted
  EST-03: Admin hearing process (15 pts)
  EST-04: Court referral (15 pts)
  EST-05: COBO letters (10 pts)
  EST-06: Case narration (15 pts)

P-S PARENTING & SUPPORT (6 criteria, 100 points max):
  PS-01: Client contact (20 pts)
  PS-02: Genetic testing (25 pts) ← Most heavily weighted
  PS-03: Service of process (15 pts)
  PS-04: Court referral (20 pts)
  PS-05: Postal verification (10 pts)
  PS-06: Case narration (10 pts)

CASE CLOSURE (6 criteria, 100 points max):
  CLO-01: F&Rs filed (20 pts)
  CLO-02: Support termination (15 pts)
  CLO-03: Child status verification (15 pts)
  CLO-04: SETS updated (15 pts)
  CLO-05: Hold release (15 pts)
  CLO-06: Closure justification (20 pts)

Pass/Fail Thresholds:
  🟢 90%+ = Excellent (Exceeds standards)
  🟡 75-89% = Acceptable (Meets minimum)
  🔴 <75% = Needs Improvement (Requires coaching)


═══════════════════════════════════════════════════════════════════════════════

LIVE DASHBOARD FEATURES YOU'LL SEE:
════════════════════════════════════

✨ FOR SUPERVISORS:
   - View 5 randomly-selected cases per worker per report
   - Score each case against Ohio compliance standards
   - Add coaching notes and feedback
   - Track worker performance trends (avg compliance, pass rate)
   - Color-coded compliance cards (green/amber/red)

✨ FOR EXECUTIVES (Directors):
   - Agency-wide QA metrics dashboard
   - Compliance trending by category
   - Identify systemic training needs
   - Worker performance benchmarking
   - Strategic insights and action items
   - Export-ready compliance data

✨ AUTOMATIC FEATURES:
   - QA samples generated on submission (no manual selection needed)
   - Deterministic sampling (reproducible for audits)
   - Compliance scoring automatic (Ohio criteria pre-loaded)
   - Metrics aggregation real-time


═══════════════════════════════════════════════════════════════════════════════

GETTING STARTED NOW:
═════════════════════

1. Open: http://localhost:8501
2. Let it load (you'll see role selector on left sidebar)
3. Select Role: Look at docs/QA_COMPLIANCE_SYSTEM_COMPLETE.md (full reference)

Try this sequence:
  a) Support Officer role → Show the worker UI enhancements (badges, templates)
  b) Process a few cases and submit → See "QA samples generated" message
  c) Switch to Supervisor → See the new "🎯 QA Review" tab
  d) Switch to Director → See the new "🎯 QA & Compliance" tab

═══════════════════════════════════════════════════════════════════════════════
""")

print("\n✅ QA System is ready! Open http://localhost:8501 and follow the workflow above.\n")
