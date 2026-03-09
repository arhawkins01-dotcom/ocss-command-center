# OCSS Command Center - Director Soft Demo Script

**Version:** 1.0.0  
**Last Updated:** February 19, 2026  
**Audience:** Agency Director (business + operational focus)  
**Demo Length:** 20-25 minutes (+ 10 minutes Q&A)

---

## 1) Demo Goal (Read This First)

Use this walkthrough to show the Director that the application can:

1. Ingest reports safely (with duplicate-period controls and auditability)
2. Route work to Support Officers by caseload
3. Support row-level case processing (50+ line reports)
4. Track meaningful KPIs (reports worked + case lines worked/completed)
5. Capture and analyze operational support tickets across leadership roles

---

## 2) Suggested Agenda

1. Executive outcomes and KPI snapshot (3 min)
2. Program Officer ingestion + controls (5 min)
3. Support Officer row-level workflow (7 min)
4. Supervisor oversight and readiness for review (3 min)
5. Director ticket KPI visibility and Q&A (2-7 min)

---

## 3) Pre-Demo Checklist (5 minutes before meeting)

- App is running at `http://localhost:8501`
- Browser tab is open and refreshed
- Role selector visible in sidebar
- At least one uploaded report exists (or plan to upload one live)
- If uploading live, have a sample `.xlsx` or `.csv` ready

Optional confidence check:
- In terminal: `cd /workspaces/ocss-command-center/app && /usr/local/bin/python test_integration.py`

---

## 4) Talk Track + Click Path

## Step A — Open with Leadership Value (Director Role) [~3 min]

**Click path**
1. Sidebar → select **Director**
2. Show **KPIs & Metrics** tab
3. Briefly show **Team Performance** tab
4. Open **🆘 Ticket KPIs** tab

**Say**
- “This dashboard gives a single view of report operations across intake, routing, processing, and support.”
- “The key value is operational visibility: we can see throughput at case-line level, not just file-level.”
- “Ticket analytics are also centralized, so leadership can see issue trends by role, category, and time window.”

**Highlight**
- KPI cards are role-specific and workflow-aware
- Ticket KPI filters include scope, priority, category, establishment, and date windows (including custom range)

---

## Step B — Demonstrate Controlled Ingestion (Program Officer) [~5 min]

**Click path**
1. Sidebar → select **Program Officer**
2. Open **📤 Upload & Processing**
3. Select a caseload
4. Upload sample report file
5. Set metadata:
   - Report Type (e.g., `P-S Report`)
   - Frequency (`Monthly`, `Quarterly`, or `Bi-Annual`)
   - Period year + period value
6. Click **Process Report**

**Say**
- “Ingestion is controlled and auditable. Every successful run creates an ingestion confirmation ID.”
- “Before ingesting, the app scans for duplicate period submissions to prevent accidental re-processing.”
- “If a duplicate is intentional, there is an explicit override checkbox; otherwise, ingest is blocked.”

**Show on screen**
- Ingestion confirmation message with `ING-...` ID
- Duplicate detection warning behavior (if triggered)
- Upload routing audit entries

---

## Step C — Show Row-Level Case Processing (Support Officer) [~7 min]

**Click path**
1. Sidebar → select **Support Officer**
2. Choose name in **Act as Support Officer / Team Lead**
3. Open **📝 My Assigned Reports**
4. Pick a report queue item
5. In row workflow:
   - Filter rows (`Pending / In Progress`, `All`, `Completed`)
   - Select a single case row
   - Edit fields and update `Worker Status`
   - Click **Save Progress** to checkpoint work
6. Repeat for another row (quickly)
7. Attempt submit when pending rows remain (to show guard)
8. Complete remaining row(s) and click **Submit Caseload as Complete**

**Say**
- “Each line is treated as a case. This is critical because reports commonly include 50+ rows.”
- “Workers process one line at a time, save progress, and statuses are tracked at row level.”
- “Submission to supervisor is blocked until all assigned rows are complete, preventing partial handoffs.”

**Show on screen**
- `Worker Status` values: `Not Started`, `In Progress`, `Completed`
- Save confirmation on row updates
- Guard message if not all rows are completed

---

## Step D — Director Oversight (Caseload Management) [~3 min]

**Click path**
1. Sidebar → select **Director**
2. Open **👥 Caseload Management** tab
3. Scroll to **Workload Distribution by Worker** chart (show real-time data)
4. Scroll to **Reassign Caseloads Between Workers**
5. Select a "From Worker", "To Worker", and "Caseload"
6. Click **Execute Reassignment**

**Say**
- "I can see the exact workload of every support officer in real-time."
- "If a worker is overloaded, I can instantly move a caseload to another team member."
- "This updates their dashboards immediately—no emails or spreadsheets required."

---

## Step E — Show KPI Integrity (Support Officer KPIs) [~3 min]

**Click path**
1. Stay in **Support Officer → My Assigned Reports**
2. Scroll to KPI sections:
   - Support Officer KPI Tracker table
   - Throughput table
   - 7-day throughput bar chart

**Say**
- “KPI logic is tied to row-level work, not just report counts.”
- “We track both report-level effort and case-line effort for a truer workload picture.”

**Call out KPI definitions**
- **Reports Worked**: reports with active row progress
- **Case Lines Worked**: lines touched (`In Progress`/`Completed` or timestamped)
- **Case Lines Completed**: lines marked `Completed`
- **Throughput 7d / 30d**: activity based on `Last Updated`

---

## Step E — Show Leadership Issue Governance (Director/IT Ticket KPIs) [~3 min]

**Click path**
1. Sidebar → select **Director** and open **🆘 Ticket KPIs**
2. Change filters (Scope, Priority, Date Window)
3. Choose **Custom Range** and show effective filter summary
4. (Optional) Switch to **IT Administrator → 🆘 Ticket KPIs** to show maintenance log and IT verification

**Say**
- “All roles can submit help tickets, but leadership and IT can analyze patterns and service quality.”
- “The filter summary makes KPI context explicit, so numbers are always interpretable.”
- “IT can maintain and verify ticket actions, providing accountability.”

---

## 5) Director-Focused Close (1 minute)

**Say**
- “This gives us controlled intake, worker-level execution, and leadership-level visibility in one workflow.”
- “Operationally, we now have fewer blind spots: every ingestion, case row, and ticket can be tracked and reviewed.”
- “The next phase would be persistence and enterprise authentication, but the process model is already in place and demo-ready.”

---

## 6) Q&A Prep (Likely Questions)

### Q1: “How do we prevent duplicate monthly reports?”
**Answer:** Ingestion runs duplicate-period scanning using metadata (type/frequency/period/caseload) and content hash checks. Non-intentional duplicates are blocked by default.

### Q2: “Can one report with 50+ lines be worked safely?”
**Answer:** Yes. Each line is treated as a separate case row with its own status and last-updated tracking. Workers save row by row.

### Q3: “How do you ensure KPI accuracy?”
**Answer:** KPI calculations are derived from the same row-level dataset used in processing, so reports worked and case lines worked/completed stay consistent.

### Q4: “Can leadership monitor operational issues?”
**Answer:** Yes. Ticket KPI tabs for Director, Program Officer, Supervisor, and IT provide filtered analytics and trend visibility.

### Q5: “What’s needed before broad rollout?”
**Answer:** Add durable persistence and authentication/authorization (planned next phase), then proceed with pilot rollout.

---

## 7) Backup Plan (If live upload fails)

If sample upload is unavailable during demo:
- Use existing queued reports in Support Officer tab
- Demonstrate row-level workflow and KPI tracking anyway
- Emphasize ingestion controls conceptually using existing audit entries and metadata already shown in UI

---

## 8) 30-Second Summary for the Director

“Today you saw end-to-end control: reports are ingested with duplicate safeguards, routed by caseload, processed row by row as real case work, and tracked with practical KPIs. Leadership can also monitor support issues through filtered ticket analytics. The application already supports the operating model for a soft launch.”
