# OCSS Command Center - User Manual

**Version 1.0.0**  
**Last Updated: February 21, 2026**

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Role-Specific Guides](#role-specific-guides)
   - [Director](#director)
   - [Program Officer](#program-officer)
   - [Supervisor](#supervisor)
   - [Support Officer](#support-officer)
   - [IT Administrator](#it-administrator)
4. [Common Tasks](#common-tasks)
5. [Troubleshooting](#troubleshooting)
6. [Support & Contact](#support--contact)

---

## System Overview

The OCSS Command Center is a centralized dashboard for managing establishment reports, caseloads, and team assignments. The system provides role-based views to support different workflows across your organization.

### Key Features

- **Role-Based Access**: Each user sees relevant features for their role
- **Caseload Management**: Track and assign work by caseload (181000 series)
- **Report Processing**: Upload, review, edit, and export establishment reports
- **Ingestion Controls**: Ingestion confirmation ID, period metadata, and duplicate-period scanning
- **Team Coordination**: Supervisors manage units and assign work to team members
- **Audit Trail**: Upload routing, assignment changes, and ticket actions are logged in-session
- **Escalation Alerts**: Time-based alerts for overdue/unacknowledged work (with acknowledgements)
- **Leadership Exports**: Senior leadership can download Word/Excel briefing packs from live application data
- **Help Ticket Center**: All roles can submit; leadership and IT roles can analyze ticket KPIs

### System Requirements

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Network access to the OCSS Command Center server
- Your assigned username/credentials (when authentication is enabled)

### Important Notes

- **Mixed Persistence Model**:
   - **Organizational configuration persists across app restarts** (Users, Units, Assignments, Current User (for audit), and Alert Acknowledgements)
   - **Report data is session-based** (uploaded report content and row-level edits)
   - Use **Leadership Exports** (Excel/Word) for periodic snapshots when needed

---

## Getting Started

### Accessing the System

1. Open your web browser
2. Navigate to: `http://[your-server-address]:8501`
3. The dashboard will load automatically

### Signing In (Optional)

Most deployments use the sidebar role selector (no sign-in). Some environments (management demo or IT-managed SSO gateway) may enable a sign-in screen.

- If you see a **Sign in** screen, complete sign-in (or choose **Continue without signing in** when available).
- When signed in, your **role is locked** to your authenticated identity and the sidebar role radio will not appear.

### Selecting Your Role

On the left sidebar, use the **"Select Your Role"** radio buttons to choose your role:
- Director
- Program Officer
- Supervisor
- Support Officer
- IT Administrator

The main content area will update to show features relevant to your role.

**Note**: If authentication is enabled and you are signed in, role selection is handled automatically.

---

## Role-Specific Guides

### Director

**Purpose**: Executive oversight, strategic planning, and performance monitoring.

#### Dashboard Features

**📊 KPIs & Metrics Tab**
- **Alerts (Escalation)**: A compact expander shows aging/unacknowledged work relevant to your leadership title (see Unit Role below)
- View organizational performance metrics:
  - Report Completion Rate
  - On-Time Submissions
  - Data Quality Score
  - CQI Alignments
- Review monthly submission trends
- Identify strategic wins and action items

**👥 Caseload Management Tab**
- Overview of all active caseloads
- Regional distribution metrics
- Completion status by region
- **Leadership Exports (Excel/Word)**: Download an executive packet from live application data (caseload status, alerts, assignments, audit)

**Leadership Titles (Unit Role)**
The sidebar role remains **Director**, but leadership titles are captured under **Unit Role** in User Management:
- Director (one allowed)
- Deputy Director
- Department Manager
- Senior Administrative Officer

Alerts and export views adapt based on Unit Role.

**📋 Team Performance Tab**
- Individual worker performance comparison (dynamically updated)
- Real-time team efficiency metrics and quality scores
- **Note**: This tab now aggregates data directly from Support Officer work queues.

**🆘 Ticket KPIs Tab**
- Organization-level ticket analytics
- Filter support by scope, priority, category, establishment, and date window
- Custom date range with automatic start/end correction

#### Quick Actions

- Monitor high-level trends
- Identify teams needing support
- Export reports for executive briefings

---

### Program Officer

**Purpose**: Upload establishment reports and manage caseload data.

#### Dashboard Features

**📤 Upload & Processing Tab**

1. **Select Caseload**: Choose the target caseload (181000, 181001, 181002, etc.)
2. **Upload File**: Click "Browse files" and select an Excel (.xlsx) or CSV file
3. **Review Preview**: The system displays:
   - File name and size
   - Number of rows and columns
   - Data preview (first 5 rows)
4. **Set Ingestion Metadata**:
   - Report Type (for example: P-S Report)
   - Frequency (Monthly / Quarterly / Bi-Annual)
   - Period Year and Period Value
   - **Due-Date Clock**: For monthly 56RA / P-S / Locate sources, the app calculates a due date automatically based on the monthly schedule (see below). The clock starts at upload time.
5. **Process Report**: Click **"Process Report"**
6. **Review Confirmation**:
   - Ingestion ID (`ING-...`) is displayed on success
   - Duplicate-period scanning runs automatically before ingest
   - **Note**: Any non-critical processing warnings are now grouped in a collapsible "⚠️ Warnings" section to keep your view clean. Click to expand and review them.

7. **(Optional) Rename processed report display names**:
   - Update the **"Rename to"** field for one or more processed items
   - Click **"✏️ Update"** to apply a single rename
   - Or click **"✏️ Update All Names"** to apply all edits in one step

**📊 Caseload Overview Tab**
- View all active caseloads
- See upload statistics by caseload
- Monitor report status

**📋 Report Status Tab**
- Track reports in progress
- View completion status
- Export summary data

**🆘 Ticket KPIs Tab**
- Program Officer ticket KPI analytics with the same filters used by leadership roles

#### Best Practices

- **File Format**: Use standardized Excel templates for consistent data structure
- **Naming Convention**: Name files clearly (e.g., `ENV_Report_Q1_2026.xlsx`)
- **Data Validation**: Review the preview before uploading to catch errors early
- **Regular Uploads**: Upload reports as soon as they're prepared to keep work flowing

#### Monthly Report Distribution Schedule (Current)

For monthly processing cycles, the QA due-date clock is based on the report source and month:

| Month | Primary Report (QA) | Secondary Report (QA) |
|---|---|---|
| January | 56RA (3 days) | P-S (2 days) |
| February | Locate (3 days) | P-S (2 days) |
| March | P-S (5 days) |  |
| April | 56RA (3 days) | P-S (2 days) |
| May | Locate (3 days) | P-S (2 days) |
| June | P-S (5 days) |  |
| July | 56RA (3 days) | P-S (2 days) |
| August | Locate (3 days) | P-S (2 days) |
| September | P-S (5 days) |  |
| October | 56RA (3 days) | P-S (2 days) |
| November | Locate (3 days) | P-S (2 days) |
| December | P-S (5 days) |  |

If a report source cannot be detected or the frequency is not Monthly, the app uses a default due window.

---

### Supervisor

**Purpose**: Manage your unit, assign caseloads to team members, and monitor team performance.

**Who Uses This Role**: Supervisors use this role to manage their unit. Worker Self-Pull is available only to senior leadership (Director/Program Officer) and Support Officer **Team Leads**.

#### Dashboard Features

**👥 My Team & Assignments Tab**

1. **Select Your Unit**: Choose your supervisor name from the dropdown
2. **View Team**: See all team leads and support officers in your unit
3. **View Assignments**: See which caseloads are assigned to each team member

**Reassign Reports Within Unit**:
- **From Worker**: Select the current assignee
- **To Worker**: Select the new assignee
- **Caseload to Move**: Choose the caseload
- Click **"🔄 Move Caseload"** to reassign

**Worker Self-Pull (Claim a Caseload)**:

This feature allows eligible users to claim caseloads for themselves.

**Access**:
- **Allowed**: Director, Program Officer, and Support Officer **Team Leads**
- **Not allowed**: Regular Support Officers (non-Team Leads)

1. **Worker Action**:
   - Select **Supervisor** role in the sidebar
   - Choose your supervisor's name from the dropdown
   - Scroll to the **Worker Self-Pull** section
   - Enter your name in "Simulate Current Worker"
   - Select yourself in "Pull As" (must match exactly)
   - Choose a caseload from "Caseload to Claim"
   - The system shows if the caseload is available or who currently owns it
   - Click **"🧷 Pull Caseload to Self"**

2. **Availability Hints**:
   - Green info box: Caseload already assigned to you
   - Orange warning: Caseload assigned to someone else (pull blocked)
   - No message: Caseload is available for claiming

3. **Self-Only Rule**: Workers can only pull caseloads for themselves, not for others

**📈 Team Performance Analytics Tab**
- Team average metrics (completion, quality, efficiency)
- Individual worker performance comparison
- Progress tracking

**🆘 Ticket KPIs Tab**
- Supervisor-accessible ticket KPI analytics and trend filters

#### Supervisor Best Practices

- **Balance Workload**: Distribute caseloads evenly across team members
- **Monitor Progress**: Check team performance metrics weekly
- **Support Struggling Workers**: Reassign if someone is overloaded
- **Encourage Self-Pull (when applicable)**: Team Leads can claim new work when they have capacity
- **Audit Trail**: All assignments are logged; you can review changes in IT Admin view

#### Alerts & Exports

- **Alerts (Escalation)**: A compact expander highlights:
   - Items aging **3–5 days** without acknowledgement (Supervisor tier)
   - **Unassigned** caseload work items (always visible to leadership)
- **Leadership Exports (Excel/Word)**: Supervisors can download a unit-scoped packet for briefings and workload reviews

---

### Support Officer

**Purpose**: Process assigned reports for your caseloads and provide technical support.

#### Dashboard Features

**Act as Support Officer / Team Lead**

**Important**: If authentication is enabled, your role is locked after sign-in. If you are *not* signed in, you must manually select your name from the dropdown to see your work (this simulates login).

1. Find the "Act as Support Officer / Team Lead" dropdown at the top
2. Select your name from the list
3. The dashboard will update to show only caseloads assigned to you

**Caseload Metrics**
- **Assigned Caseloads**: Number of caseloads you're responsible for
- **Reports Worked**: Assigned reports with active row-level work
- **Case Lines Worked**: Row-level cases worked for assigned reports
- **Case Lines Completed**: Row-level cases completed for assigned reports

**📊 Caseload Dashboard Tab**

View and process reports by caseload:

1. **Select a Caseload**: Choose from your assigned caseloads
2. **View Reports**: Each report shows:
   - Report ID and date
   - File name
   - Key data fields
3. **Edit Report Data**:
   - Click inside the expandable report card
   - Use the form to update field values
   - Click **"💾 Update Report"** to save changes
4. **Action Buttons**:
   - **📥 Download CSV**: Export report data
   - **✅ Approve**: Mark report as approved
   - **💾 Save**: Save progress
   - **📤 Submit**: Submit for review

**📝 My Assigned Reports Tab**
- View report queue for your assigned caseloads
- Process one case line at a time (row-level workflow)
- **How to complete this report (checklist)**: Review the in-dashboard checklist (includes sample narration templates you can copy/paste)
- **Save Progress**: Click **"💾 Save Progress"** periodically to checkpoint your work (the UI shows your last saved timestamp)
- **Conditional Submit**: The **"✅ Submit Caseload"** button checks your work. It will only allow submission if *all* your assigned rows are marked `Completed`. If rows are `Pending` or `In Progress`, you'll see a warning.
- **Report-type guardrails**: The app enforces report-specific dropdowns and required fields (see the 56RA / P-S / Locate sections below)
- View KPI Tracker and Throughput (7-day / 30-day) summaries

#### Alerts for Support Officers

- The app shows a lightweight warning when you have **unfinished and/or unsaved work**.
- The **Alerts (Escalation)** expander is also available. Worker alerts focus on the **1–3 day** window before escalation moves upward.
- Clicking **💾 Save Progress** also acknowledges the report to reduce repeated alerts.

**🆘 Support Tickets Tab**
- View and manage support requests related to your caseloads

**📚 Knowledge Base Tab**
- Access documentation and guides
- Search for solutions to common issues

#### Support Officer Best Practices

- **Select Yourself**: Always choose your name in the dropdown to see your work
- **Process Row-by-Row**: Treat each report line as a separate case item
- **Review Data Carefully**: Update row status and review fields before moving on
- **Use CSV Export**: Download data for offline analysis or archiving
- **Update Status**: Use `Worker Status` (`Not Started`, `In Progress`, `Completed`) per case line
- **Ask for Help**: Use Support Tickets if you encounter data issues

---

### IT Administrator

**Purpose**: System configuration, user management, unit setup, and audit monitoring.

#### Dashboard Features

**🖥️ System Status Tab**
- Server health metrics
- Database status
- Active user count
- Configuration paths
- **Alerts (Operational View)**: IT Admin sees a compact read-only view focused on overdue and unassigned items

**👥 User & Caseload Management Tab**

**Current User (for audit)**:
- Enter your name so audit entries record who made changes

**Organization Metrics**:
- Total users, assigned reports, completion rates

**Add/Remove Users**:

User management is session-based but **functional** for demos and internal workflows.

1. Enter new user name
2. Select role (Director, Program Officer, Supervisor, Support Officer, IT Administrator)
3. Select department (or custom)
4. If adding a **Director** role user, choose a **Unit Role**:
   - **Director** (only one allowed)
   - **Deputy Director**
   - **Department Manager**
   - **Senior Administrative Officer**
5. Click **"➕ Add User"**

**Unit Role column**:
- For **Support Officers**, Unit Role identifies **Team Lead** vs regular Support Officer
- For **Director** role users, Unit Role identifies leadership level (Director/Deputy Director/Department Manager/Senior Administrative Officer)

**Bulk Caseload Assignment** (future feature):
- Assign multiple reports to a user at once

**🏷️ Unit Management**:

Create and manage organizational units:

1. **Select Unit**: Choose "(New Unit)" or an existing unit
2. **New Unit Name**: Enter a name if creating new (case-insensitive duplicates are blocked)
3. **Supervisor Name**: Enter the supervisor's name
4. **Team Lead / Support Officer**: Add team members
5. **Caseload to Assign**: Select a caseload and assignee
6. Click **"➕ Create/Update Unit"**

**Validation & Deduplication**:
- System prevents duplicate unit names (case-insensitive)
- Prevents adding duplicate personnel to same unit
- Blocks assigning same caseload to multiple people
- Shows clear error messages

**Current Units**:
- Quick view of all units with supervisor and team lists

**🗑️ Remove Caseload Assignment**:

1. **Select Unit**: Choose the unit
2. **Select Assignee**: Choose the person
3. **Select Caseload**: Choose the caseload to remove
4. Click **"🗑️ Remove Assignment"**
5. **Confirmation Modal Appears**:
   - Review the removal details
   - Click **"Confirm Remove"** to proceed (logs audit entry)
   - Or click **"Cancel"** to abort

**🛠️ Maintenance & Logs Tab**

**Recent System Activity**:
- View server logs and audit entries
- See assignment/removal actions with timestamps
- Filter by event type

**Maintenance Tools**:
- Run system diagnostics
- Generate audit reports
- Backup database

**🆘 Ticket KPIs Tab**
- IT ticket KPI analytics with shared filters
- Ticket log maintenance entries and IT verification tracking

#### IT Administrator Best Practices

- **Set Current User**: Always enter your name for audit accountability
- **Unit Structure**: Create units matching your org chart (e.g., "OCSS North", "OCSS South")
- **Assignment Review**: Check Current Units regularly to verify accurate assignments
- **Audit Log**: Review Recent System Activity weekly to monitor changes
- **Backup Data**: Export audit logs and configuration periodically
- **Deduplication**: System blocks duplicates automatically; no manual cleanup needed
- **Confirmation Modals**: Always review before confirming removals

---

## Common Tasks

### How to Upload a Report (Program Officer)

1. Select **Program Officer** role
2. Go to **📤 Upload & Processing** tab
3. Select target caseload (e.g., 181000)
4. Click **"Browse files"**
5. Select Excel or CSV file
6. Review preview
7. Select report metadata (type, frequency, period year/value)
8. Click **"Process Report"**
9. Confirm ingestion success and capture the displayed ingestion ID

### How to Claim a Caseload (Worker Self-Pull)

**Note**: Worker Self-Pull is restricted to **Director / Program Officer** and **Support Officer Team Leads**. It is accessed through the **Supervisor** role.

1. Select **Supervisor** role in the sidebar
2. Choose your supervisor's name in the dropdown
3. Go to **👥 My Team & Assignments** tab
4. Scroll to the **Worker Self-Pull (Claim a Caseload)** section
5. In **Worker Self-Pull** section:
   - Enter your name in "Simulate Current Worker"
   - Select yourself in "Pull As" (both fields must match exactly)
   - Choose a caseload from "Caseload to Claim"
   - Review the availability hint (if any):
     - Green info box = already yours
     - Orange warning = assigned to someone else
     - No message = available to claim
6. Click **"🧷 Pull Caseload to Self"**
7. System confirms claim or shows error if not available

### How to View Caseload Work Status (Real-Time) (Leadership)

1. Select **Director** or **Program Officer** role
2. Go to **👥 Caseload Management**
3. Review the **Caseload Work Status (Real-Time)** table
4. Use it to see assigned vs unassigned caseloads and overall status: **Pending / Finished / Completed / Unassigned**

### How to Use Alerts (Escalation) and Acknowledge

1. Open your role workspace
2. Find **Alerts (Escalation)** (available for all roles)
3. Review the top items (unassigned and/or aging work)
4. Select a report in **Acknowledge report** and click **Acknowledge**

Escalation ladder (time since upload):
- Support Officer: 1–3 days
- Supervisor: 3–5 days
- Program Officer: 5+ days
- Department Manager: 1–10 days *only when Support Officer + Supervisor have not acknowledged*
- Director/Deputy Director: 10+ days (last)

### How to Export Leadership Reports (Excel / Word)

1. Director: go to **👥 Caseload Management**
2. Program Officer: go to **👥 Caseload Management**
3. Supervisor: go to **👥 Team Caseload** (after selecting your supervisor)
4. Open **Leadership Exports (Excel / Word)** and download:
   - Excel packet with multiple sheets
   - Word packet suitable for briefings

### How to Process a Report (Support Officer)

1. Select **Support Officer** role
2. Choose your name in "Act as Support Officer / Team Lead"
3. Go to **📝 My Assigned Reports** tab
4. Select a report from your queue
5. Choose a case-row filter and select one case row
6. Update editable row fields (including `Worker Status`)
7. Edits are applied immediately to the session
8. Click **"💾 Save Progress"** to checkpoint your work
9. Repeat until all assigned rows are marked `Completed`
10. Click **"✅ Submit Caseload as Complete"** to finalize and send to supervisor

#### Completion Checklist (What “Done” Means)

Use this checklist to ensure your caseload is ready to submit:

1. In **📝 My Assigned Reports**, set the filter to **Pending / In Progress**
2. Open each remaining case row assigned to you
3. Review/update the editable fields required for your report type
4. Set **Worker Status** for that row:
   - **Not Started**: you have not begun work on the row
   - **In Progress**: you have started but are not finished
   - **Completed**: row is fully reviewed and ready for supervisor
5. Click **💾 Save Progress** regularly (recommended after every few rows)
6. Before submitting, switch the filter to **All** and verify there are **no** assigned rows left in **Not Started** or **In Progress**
7. Click **✅ Submit Caseload as Complete**

**Important:** The app will block submission if any of your assigned rows are not marked **Completed**. This is intentional to prevent partial or inconsistent submissions.

---

## 56RA Report Spreadsheet Instructions (Support Officer)

### Background / Rationale (Summary)

56RA helps identify cases where OCSS can still meet Service of Process (SOP) and move the case forward (establish an order, provide customer service, or close when appropriate). Data captured on the worksheet supports analysis of outcomes, success, bottlenecks, and process gaps.

### Step-by-step

1. Save the spreadsheet to your P: drive or Desktop.
2. Filter the **Caseload** column to show only your caseload(s).
3. Review **every** case on your caseload.
4. Take real action (do not only narrate that action is needed): schedule GT, prep ADS, refer to court, close case, etc.
5. Complete these fields for each case:
   - **Date Report was Processed** (in the app: **Date Action Taken**)
   - **Action Taken/Status** (drop-down)
   - **Case Narrated**
   - **Comment** (as needed; required if Action Taken/Status = OTHER)
6. Narrate every case (when applicable include status, action taken, and next steps/follow-up needed).
7. Email the completed spreadsheet to your Supervisor and Establishment PO3 at each deadline.

### 56RA Action Taken/Status values

- Scheduled GT
- Pending GTU
- Prepped ADS
- Pending AHU
- Referred to Court
- Pending Court
- Sent Contact Letter
- Sent COBO Letter(s)
- Sent Postal Verification
- Closed Case
- NCP Unlocatable
- Order Already Established
- Case Already Closed
- OTHER (must explain in Comment)

### Reminders

- If a case was sanctioned previously and nothing is pending, re-process the necessary action.
- If a client missed a second GT appointment and it has been over 14 days, take the next appropriate steps.
- Contact your supervisor with questions.

---

## Paternity-Support Mode (P-S) Work List Instructions (Support Officer)

### Goal (Summary)

Process every case on the work list to meet SOP requirements, provide customer service, establish orders, close cases when appropriate, and reduce caseload size.

### Step-by-step

1. Save the worksheet to your P: drive or Desktop.
2. Work your assigned unit/caseload cases and meet the monthly deadlines.
3. Document actions in **Action Taken/Status** (drop-down).
4. Narrations must begin with **P-S Report.**
5. Avoid unnecessary appointments; contact clients via phone, web portal, etc.
6. Complete all actions and follow up (no “to be scheduled” narrations).
7. Email the completed report to your Supervisor and Emily at each deadline.

### P-S Action Taken/Status values

- GT
- ADS
- COURT REFERRAL
- CONTACT LETTER
- POSTAL
- CLOSED CASE
- PHYSICAL CUSTODY
- NCP UNLOCATABLE
- PENDING-GTU
- PENDING-AHU
- PENDING-COURT
- OTHER (must explain in Comment)

### Key rules

- No “no action” narrations unless an action is pending.
- If sanctioned previously and nothing is pending, process the necessary action again.

---

## Locate Report Spreadsheet Instructions (Support Officer)

### Purpose (Summary)

The Locate report identifies cases where OCSS can still meet locate-effort requirements to move cases forward (establish an order, provide customer service, or close cases when appropriate). Information collected supports analysis of outcomes, division success, bottlenecks, process gaps, and resource needs.

### Step-by-step

1. Save the spreadsheet to your Desktop or P: drive.
2. Filter the **Caseload** column to only your caseload(s).
3. Review **each** case on the spreadsheet.
4. Clear the NCP in all relevant databases (BMV, SVES, court dockets, ODRC, Work Number, etc.).
   - If there is an indication the NCP may be out of state, request a **CLEAR** search.
5. Clear all received information on **ILSU**.
   - Ensure the **Data received** column is blank.
   - Consider **NAS** / **UNL** closures if criteria are met.
6. Attempt contact with CP/CTR and/or PPF/NCP (if available) via phone, JFS7711, web portal, etc.
   - Narrate what you requested and the deadline (if applicable).
   - If the client provides address information, take the next appropriate action.
7. If applicable, close the case using the appropriate closure code:
   - **UNL**: locate 2+ years with SSN
   - **NAS**: locate 6+ months with no SSN
8. If the NCP is located, process the next appropriate action within **5 business days** (SOP clock starts when CIP1 is updated with a valid address).
   - Review OnBase for any required documents (do not delay unless necessary documents are missing).
9. Narrate every case that appears on the spreadsheet.

### Narration patterns (examples)

- **UNL Locate Report:** searched databases (BMV/SVES/dockets/etc.)—no information located. Contacted CP; no information. Case has been in locate 2+ years with SSN; case closed.
- **NAS Locate Report:** searched databases—no information located. No response to record update from CP. Case has been in locate 6+ months without SSN; case closed.

### Reminders

- Do not close a case solely because an action is needed; complete the action and follow up.
- Do not send unnecessary postals to delay taking an action; verify older addresses using locate sources.

### How to Reassign Work (Supervisor)

1. Select **Supervisor** role
2. Choose your name
3. Go to **👥 My Team & Assignments** tab
4. In **Reassign Reports Within Unit**:
   - From Worker: Current assignee
   - To Worker: New assignee
   - Caseload to move: The caseload
5. Click **"🔄 Move Caseload"**
6. Confirm success message

### How to Create a Unit (IT Administrator)

1. Select **IT Administrator** role
2. Go to **👥 User & Caseload Management** tab
3. Enter your name in "Current User (for audit)"
4. In **Unit Management**:
   - Select "(New Unit)"
   - Enter "New Unit Name" (e.g., "OCSS Central")
   - Enter "Supervisor Name"
   - Enter "Team Lead Name" (optional)
   - Enter "Support Officer Name"
   - Select "Caseload to Assign"
5. Click **"➕ Create/Update Unit"**
6. Review "Current Units" list

### How to Remove an Assignment (IT Administrator)

1. Select **IT Administrator** role
2. Go to **👥 User & Caseload Management** tab
3. In **Remove Caseload Assignment**:
   - Select Unit
   - Select Assignee
   - Select Caseload
4. Click **"🗑️ Remove Assignment"**
5. **Confirmation modal appears**:
   - Review details
   - Click **"Confirm Remove"** to proceed
   - Audit entry is recorded
6. Check **Maintenance & Logs** tab to see audit entry

---

## Troubleshooting

### I don't see my caseloads (Support Officer)

**Solution**: Make sure you've selected your name in the "Act as Support Officer / Team Lead" dropdown. Only caseloads assigned to you in your unit will appear.

### Upload failed or preview looks wrong (Program Officer)

**Potential Causes**:
- File format issue (must be .xlsx or .csv)
- Corrupted or empty file
- Special characters in file name

**Solution**: 
- Verify file format
- Open file in Excel to confirm data is present
- Rename file to remove special characters
- Try re-uploading

### Duplicate-period ingestion was blocked

**Reason**: A report with matching type/frequency/period/caseload (or matching content hash) already exists in the session registry.

**Solution**:
1. Verify report metadata is correct
2. Confirm whether this upload is intentional
3. If intentional, enable **"Allow ingestion even if duplicate period report is detected"** before processing

### I can't pull a caseload (Worker Self-Pull)

**Possible Reasons**:
- You do not have permission (only Director/Program Officer and Support Officer Team Leads can self-pull)
- Caseload already assigned to someone else (check availability hint)
- "Simulate Current Worker" doesn't match "Pull As" (must be identical, including capitalization)
- You're not in the worker list for this unit
- You haven't selected the Supervisor role in the sidebar
- You haven't selected your supervisor in the dropdown

**Solution**:
1. Verify you're in the **Supervisor** role (check sidebar)
2. Confirm your supervisor is selected in the dropdown
3. If you are not a Team Lead, ask your supervisor to assign/reassign the caseload to you (self-pull is restricted)
4. Check the availability hint (orange warning shows current owner and unit)
5. Ensure both "Simulate Current Worker" and "Pull As" have your exact name
6. If caseload is held by someone else, ask a supervisor to reassign it using the reassignment features

### Unit creation says "already exists"

**Reason**: System prevents duplicate unit names (case-insensitive).

**Solution**: 
- Select the existing unit from the dropdown to update it instead
- Or choose a different name for the new unit

### Can't remove an assignment

**Possible Reasons**:
- Caseload already removed
- Unit doesn't exist
- Person has no assignments

**Solution**:
- Refresh the page and try again
- Check "Current Units" list to verify structure
- Verify assignee and caseload in the dropdown match

### Report data not saving (Support Officer)

**Possible Causes**:
- Forgot to click the **"💾 Update Report"** button inside the form
- Session expired or server restarted
- Browser was closed before data was saved

**Solution**:
1. Ensure you clicked **"💾 Update Report"** inside the form (not just editing fields)
2. Look for the success message (green checkmark: "✓ Report data updated!")
3. **Important**: Session-based storage means data resets if:
   - Server restarts
   - Browser session ends
   - You clear browser cache
4. **Best Practice**: Always **📥 Download CSV** after making important edits to create a backup

### I cannot submit report to supervisor

**Reason**: At least one row assigned to you is not `Completed`.

**Solution**:
1. In **My Assigned Reports**, filter to **Pending / In Progress**
2. Complete and save each remaining row
3. Submit once all assigned rows are completed

### Page won't load

**Solution**:
- Check network connection
- Verify server is running (ask IT)
- Try refreshing the page (Ctrl+R or Cmd+R)
- Clear browser cache
- Try a different browser

---

## Support & Contact

### For Technical Issues
- Contact your IT Administrator
- Email: it-support@ocss.agency.gov
- Phone: (555) 100-2000

### For Workflow/Process Questions
- Contact your Supervisor
- Refer to this User Manual
- Check the Knowledge Base (Support Officer dashboard)

### For System Enhancement Requests
- Submit via IT Administrator
- Include detailed description and use case
- Priority requests should go through your Director

---

## Appendix: Keyboard Shortcuts & Tips

- **Ctrl+R / Cmd+R**: Refresh page
- **F11**: Full-screen mode
- **Ctrl+F / Cmd+F**: Search within page (useful for finding specific reports)

### Browser Tips

- **Bookmark the dashboard** for quick access
- **Use tabs** to compare data across roles (if you have multiple role permissions)
- **Export CSV files regularly** to maintain offline backups
- **Clear cache** weekly to ensure you see latest updates

---

**End of User Manual**  
For additional support or to report issues with this documentation, contact your IT Administrator.
