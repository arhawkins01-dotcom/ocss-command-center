# OCSS Command Center - IT Demo Script

**Version 1.0.0**  
**Last Updated: February 18, 2026**  
**Target Audience**: IT Staff, System Administrators, Technical Leadership

---

## Demo Overview

**Duration**: 25-35 minutes (20-30 minutes for core features + 5 minutes for Q&A)  
**Objective**: Walk IT staff through all major features, demonstrate role-based workflows, validate system functionality, and clarify session storage limitations.

**Important Context for Attendees**:
- This is a **proof-of-concept** with session-based storage
- Data does NOT persist across server restarts
- Each browser session has independent state
- Phase 2 will add database persistence and authentication

**Prerequisites**:
- OCSS Command Center running on server (port 8501)
- Network access to server from demo machine
- Sample data loaded (default units: OCSS North, OCSS South)
- Projector or screen sharing for group demo

---

## Demo Setup

### Before You Begin

1. **Start the Streamlit Server**:
   ```bash
   cd /workspaces/ocss-command-center
   streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
   ```

2. **Open Browser**:
   - Navigate to: `http://localhost:8501` (local)
   - Or: `http://[server-ip]:8501` (network)

3. **Verify Sample Data**:
   - Units: OCSS North, OCSS South
   - Caseloads: 181000, 181001, 181002
   - Personnel: Sarah Johnson, Michael Chen, Jessica Brown, etc.

4. **Prepare Sample Files** (optional):
   - Create a simple Excel file: `test_report.xlsx` with columns like "Student Count", "Staff Count", "Status"
   - Or use CSV: `test_report.csv`

---

## Demo Script

### Part 1: System Overview (3 minutes)

**[Show Dashboard with Director View]**

**Script**:
> "Welcome to the OCSS Command Center. This is a centralized dashboard for managing establishment reports and caseloads across our organization. The system is built on Streamlit, runs on Python, and provides role-based views for five user types."

**[Point to Left Sidebar]**

> "Each user selects their role here in the sidebar. The main content area updates automatically to show relevant features. Let's walk through each role."

**Key Points**:
- Role-based access control (currently UI-based; authentication coming in Phase 2)
- **Session-based data storage** (in-memory; resets on server restart or browser session end)
- Database integration planned for Phase 2 for persistent storage
- Streamlit framework (easy to deploy, Python-based)
- **Important**: All demo actions are session-only; recommend exporting CSV backups of important data

---

### Part 2: Director View (3 minutes)

**[Select "Director" Role]**

**Script**:
> "The Director view provides executive oversight. Let's look at the three tabs."

**Tab 1: KPIs & Metrics**

**[Show metrics cards]**

> "Here we have organization-wide KPIs:
> - Report Completion Rate: 89.3%
> - On-Time Submissions: 94%
> - Data Quality Score: 96.7%
> - CQI Alignments: 34
>
> The bar chart shows monthly submission trends. Directors can quickly identify performance patterns."

**Tab 2: Caseload Management**

**[Switch to tab 2]**

> "This shows how caseloads are distributed by region, completion status, and priority. Directors can spot regions that need attention."

**Tab 3: Team Performance**

**[Switch to tab 3]**

> "This compares individual worker performance with metrics like completion percentage, average time per report, and quality scores."

**Demo Action**: ✅ Show all three tabs  
**Expected Outcome**: Metrics display correctly; no errors

---

### Part 3: Program Officer View (5 minutes)

**[Select "Program Officer" Role]**

**Script**:
> "Program Officers are responsible for uploading establishment reports to specific caseloads."

**Tab 1: Upload Reports**

**[Show upload interface]**

**Demo Action 1: Upload a Sample File**

1. **Select Caseload**: Choose `181000`
2. **Click "Browse files"**: Upload `test_report.xlsx` or paste sample data
3. **Preview**: Show the data preview (first 5 rows, column count)
4. **Upload**: Click **"📤 Upload to Caseload"**

**Script**:
> "The system parses Excel and CSV files, shows a preview, and stores the report in the selected caseload. Each report gets a unique ID, timestamp, and is tagged with the uploader."

**[Show Recent Uploads section]**

> "Recent uploads appear here with report ID, caseload, and status."

**Tab 2: Caseload Overview**

**[Switch to tab 2]**

> "This gives Program Officers a bird's-eye view of all caseloads, how many reports each has, and status summaries."

**Expected Outcome**: 
- ✅ File uploads successfully
- ✅ Preview shows correct data
- ✅ Recent uploads list updates
- ✅ No errors in console

---

### Part 4: Supervisor View (7 minutes)

**[Select "Supervisor" Role]**

**Script**:
> "Supervisors manage organizational units, assign caseloads to team members, and monitor team performance."

**Tab 1: My Team & Assignments**

**Demo Action 1: Select a Supervisor**

1. **Dropdown**: Choose `Alex Martinez` (OCSS North supervisor)
2. **View Team**: Show the team dataframe (team leads, support officers, assigned caseloads)

**Script**:
> "Alex Martinez supervises OCSS North, which includes Team Lead Sarah Johnson and Support Officers Michael Chen and Jessica Brown. Each has assigned caseloads."

**Demo Action 2: Reassign a Caseload**

1. **From Worker**: Select `Sarah Johnson`
2. **To Worker**: Select `Michael Chen`
3. **Caseload to Move**: Choose `181000`
4. Click **"🔄 Move Caseload"**

**Script**:
> "Supervisors can reassign caseloads within their unit. This moves caseload 181000 from Sarah to Michael. The change is immediate."

**Expected Outcome**:
- ✅ Success message: "✓ Caseload 181000 moved from Sarah Johnson to Michael Chen"
- ✅ Assignment is updated in session state
- ℹ️ **Note**: You may need to re-select the supervisor in the dropdown to refresh the team dataframe view

**Demo Action 3: Worker Self-Pull Feature**

**Script**:
> "Now let's demonstrate the Worker Self-Pull feature. This allows workers to claim caseloads for themselves—but only for themselves. Workers access this through the Supervisor role."

1. **Scroll down** to the **Worker Self-Pull (Claim a Caseload)** section
2. **Simulate Current Worker**: Enter `Jessica Brown`
3. **Pull As**: Select `Jessica Brown` (must match exactly)
4. **Caseload to Claim**: Choose a caseload (e.g., `181002` if not already assigned to Jessica)

**[Show availability hint below the dropdown]**

**Script**:
> "Notice the availability hint below the dropdown. The system shows:
> - Green info box if the caseload is already assigned to you
> - Orange warning if assigned to someone else, showing who owns it and which unit
> - No message if the caseload is available for claiming"

5. Click **"🧷 Pull Caseload to Self"**

**Expected Outcome**:
- ✅ If caseload is unassigned: Success message "✓ Caseload [ID] claimed by Jessica Brown in unit 'OCSS North'"
- ✅ If already assigned to this person in this unit: Info message "Caseload [ID] is already assigned to Jessica Brown in unit 'OCSS North'."
- ✅ If assigned to someone else: Error message "Caseload [ID] is already assigned to [person] in unit '[unit]'. Cannot pull."
- ℹ️ **Note**: If the caseload was already assigned to Jessica in the sample data, pick a different caseload or demonstrate with a different worker

**Demo Action 4: Show Self-Only Enforcement**

**Script**:
> "Let's demonstrate the self-only enforcement. This prevents workers from claiming caseloads on behalf of others."

1. **Simulate Current Worker**: Keep as `Jessica Brown` (or enter a worker name)
2. **Pull As**: Select a **different person** (e.g., `Michael Chen`) - intentional mismatch
3. **Caseload to Claim**: Choose any caseload
4. Click **"🧷 Pull Caseload to Self"**

**Expected Outcome**:
- ✅ Error message: "You can only pull a caseload for yourself. Make sure 'Pull As' matches the simulated current worker."
- ✅ Assignment is NOT created (validation blocks the action)

**Script**:
> "The system enforces the self-only rule. If someone tries to pull for someone else, the operation is blocked with a clear error message."

**Tab 2: Team Performance Analytics**

**[Switch to tab 2]**

**Script**:
> "This tab shows team-level and individual performance metrics. If no team data is loaded, it displays a friendly message instead of crashing."

**Expected Outcome**:
- ✅ Metrics display or "No team data available" message (no NameError)

---

### Part 5: Support Officer View (5 minutes)

**[Select "Support Officer" Role]**

**Script**:
> "Support Officers process reports for their assigned caseloads. Since authentication isn't enabled yet, they select their name from a dropdown."

**Demo Action 1: Select Acting Support Officer**

1. **Dropdown**: Choose `Michael Chen`
2. **View Metrics**: Show Assigned Caseloads, Active Reports, Pending Approval

**Script**:
> "Michael Chen now sees only the caseloads assigned to him. The metrics update to show his workload."

**Tab 1: Caseload Dashboard**

**Demo Action 2: Process a Report**

1. **Select Caseload**: Choose one of Michael's assigned caseloads (e.g., `181001`)
2. **Expand Report**: Click on a report card to expand it
3. **View Data**: Show the data fields
4. **Edit Report**:
   - Update a field value (e.g., change "Total Students" from 245 to 250)
   - Click **"💾 Update Report"**
5. **Download CSV**: Click **"📥 Download CSV"**

**Script**:
> "Support Officers can review and edit report data directly in the dashboard. Changes are saved in session state—meaning they persist only while the server is running and the browser session is active. Support Officers should export data to CSV for offline work, archiving, or as a backup before the session ends."

**Expected Outcome**:
- ✅ Report data displays correctly
- ✅ Edit form accepts changes
- ✅ Success message after update
- ✅ CSV downloads with updated data

**Tab 2: My Assigned Reports**

**Script**:
> "This tab shows all reports assigned to the Support Officer with filters for status, priority, and due date. Workers can sort and track their progress."

---

### Part 6: IT Administrator View (7 minutes)

**[Select "IT Administrator" Role]**

**Script**:
> "The IT Administrator view is the control center for system configuration, user management, and audit monitoring."

**Tab 1: System Status**

**[Show metrics]**

**Script**:
> "Here we monitor server health, database status, active users, and configuration paths. In production, these would be live metrics."

**Tab 2: User & Caseload Management**

**Demo Action 1: Set Current User (for Audit)**

1. **Current User (for audit)**: Enter `IT Admin Demo User`

**Script**:
> "Always set your name here so audit entries record who made changes. This is critical for accountability."

**Demo Action 2: Create a New Unit**

1. **Select Unit**: Choose `(New Unit)`
2. **New Unit Name**: Enter `OCSS Central`
3. **Supervisor Name**: Enter `Jane Doe`
4. **Team Lead Name**: Enter `Tom Smith`
5. **Support Officer Name**: Enter `Alice Johnson`
6. **Caseload to Assign**: Select `181002`
7. Click **"➕ Create/Update Unit"**

**Script**:
> "The system validates inputs. It prevents duplicate unit names (case-insensitive), deduplicates personnel, and blocks assigning the same caseload to multiple people."

**Expected Outcome**:
- ✅ Success message: "Unit 'OCSS Central' created/updated"
- ✅ New unit appears in "Current Units" list

**Demo Action 3: Test Duplicate Prevention**

1. **Select Unit**: Choose `(New Unit)`
2. **New Unit Name**: Enter `ocss central` (lowercase)
3. Click **"➕ Create/Update Unit"**

**Expected Outcome**:
- ✅ Error: "Unit 'ocss central' already exists (case-insensitive match to 'OCSS Central')..."

**Script**:
> "The system detects and blocks duplicates, even with different capitalization. This keeps data clean."

**Demo Action 4: Remove a Caseload Assignment**

**[Scroll to Remove Caseload Assignment section]**

1. **Select Unit**: Choose `OCSS Central`
2. **Select Assignee**: Choose `Alice Johnson`
3. **Select Caseload**: Choose `181002`
4. Click **"🗑️ Remove Assignment"**

**Script**:
> "When you click Remove Assignment, the system processes the removal and logs an audit entry."

**Expected Outcome**:
- ✅ Success message: "✓ Removed caseload 181002 from Alice Johnson in unit 'OCSS Central'"
- ✅ Audit entry recorded in session state
- ✅ Audit entry persisted to `data/audit_log.jsonl`
- ✅ Assignment removed from unit's assignments list
- ℹ️ **Note**: In the current implementation, the confirmation happens immediately on button click. A confirmation dialog/modal can be added in Phase 2 for additional safety.

**Tab 3: Maintenance & Logs**

**[Switch to tab 3]**

**Demo Action 5: View Audit Log**

**Script**:
> "The Recent System Activity log shows all server events and audit entries. Let's look for the assignment removal we just performed."

**[Show dataframe with timestamp, event, status]**

**Expected Outcome**:
- ✅ Audit entry visible with timestamp, actor (`IT Admin Demo User`), action (`remove_assignment`), unit, assignee, caseload
- ✅ Entry also persisted to `data/audit_log.jsonl` on disk

**Script**:
> "All administrative actions are logged with timestamps and actor names. This provides an audit trail for compliance and troubleshooting."

**Demo Action 6: Maintenance Tools**

**[Show buttons: Run Diagnostics, Generate Audit Report, Backup Database]**

**Script**:
> "These are placeholders for future features like automated diagnostics, audit report generation, and database backups."

---

## Part 7: Technical Deep Dive (Optional, 5 minutes)

**For Technical Audiences Only**

**Script**:
> "Let me show you a few technical details for those interested in the implementation."

**[Open terminal/console]**

### 1. View Audit Log File

```bash
cat data/audit_log.jsonl | tail -5
```

**Script**:
> "Audit entries are persisted to `data/audit_log.jsonl` in JSON Lines format. Each line is a JSON object with timestamp, actor, action, and details."

### 2. Check Server Process

```bash
ps aux | grep streamlit
```

**Script**:
> "The server runs as a Streamlit process. You can monitor it like any other Python application."

### 3. View Application Code Structure

```bash
tree app/
```

**Script**:
> "The application is a single-file Streamlit app: `app/app.py`. All logic, session state, and UI are in this file. We're planning to modularize it in the next phase."

### 4. Database Integration (Coming)

**Script**:
> "Currently, data is session-based (in-memory). This means:
> - All units, assignments, and uploads reset when the server restarts
> - Each browser session has independent state
> - No data sharing between different users or browser windows
> 
> We're planning a PostgreSQL or SQLite backend to persist units, assignments, and reports across sessions. This will enable:
> - Multi-user access to shared data
> - Data persistence across server restarts
> - Proper audit trails in database tables
> - Backup and recovery procedures
> 
> Authentication via LDAP/AD or OAuth is also planned for Phase 2."

---

## Part 8: Testing & Validation Checklist

**Walk through this checklist with the IT team:**

### Functional Tests

- [ ] **Director**: All tabs load without errors
- [ ] **Program Officer**: File upload works; preview shows correct data
- [ ] **Supervisor**: 
  - [ ] Unit selection works
  - [ ] Caseload reassignment succeeds
  - [ ] Worker Self-Pull enforces self-only rule
  - [ ] Availability hints display correctly
- [ ] **Support Officer**: 
  - [ ] Acting as a worker filters caseloads correctly
  - [ ] Report editing saves changes
  - [ ] CSV export downloads valid file
- [ ] **IT Administrator**: 
  - [ ] Unit creation succeeds
  - [ ] Duplicate unit detection works
  - [ ] Caseload assignment deduplication works
  - [ ] Removal triggers confirmation modal
  - [ ] Audit log records actions

### Error Handling

- [ ] Uploading invalid file shows error (not crash)
- [ ] Attempting to pull for someone else blocked with clear message
- [ ] Duplicate unit creation blocked with explanation
- [ ] Empty fields validated (e.g., empty unit name rejected)
- [ ] Missing team_workers variable handled gracefully (no NameError)

### Data Integrity

- [ ] Uploaded reports persist in session_state (for duration of session)
- [ ] Caseload reassignments update immediately in session_state
- [ ] Worker Self-Pull creates correct assignments in session_state
- [ ] Audit entries written to disk (`data/audit_log.jsonl`)
- [ ] Removal cleans up empty assignment lists
- [ ] Session state resets cleanly on server restart (no stale data)
- [ ] Exported CSV files contain accurate data reflecting current session state

### Performance

- [ ] Page load time < 3 seconds
- [ ] File upload for 10KB file < 2 seconds
- [ ] No lag when switching roles
- [ ] No memory leaks after 30 minutes of use

---

## Part 9: Q&A and Next Steps

**Common Questions & Answers**

**Q: Is data persistent across browser sessions?**  
A: Currently no. Data is stored in Streamlit's `st.session_state`, which resets when:
- The server restarts
- The browser session ends
- The browser cache is cleared
- The user navigates away and returns (in some cases)

The **only** persistent data is the audit log in `data/audit_log.jsonl`. Database integration is planned for Phase 2 to enable full data persistence.

**Workaround for Demo/Testing**: Users should export CSV files regularly to preserve important data. IT should backup the `data/` directory.

**Q: How do we add authentication?**  
A: We recommend LDAP/AD integration or OAuth. This will replace the "Simulate Current Worker" fields with real user authentication.

**Q: Can we customize the roles?**  
A: Yes. The role list is defined in `app/app.py` around line 70. You can add/remove roles and customize the UI for each.

**Q: How do we deploy to production?**  
A: Refer to `docs/IT_IMPLEMENTATION_GUIDE.md` for Docker, nginx, SSL, and systemd service setup.

**Q: What about backups?**  
A: Currently, the audit log is the only persistent data (`data/audit_log.jsonl`). To back up:
- Copy the `data/` directory regularly (contains `audit_log.jsonl`)
- Instruct users to export CSV files of important reports
- Consider scheduling a cron job to archive `data/audit_log.jsonl` daily

Once database integration is complete, standard database backup procedures apply (pg_dump for PostgreSQL, file backup for SQLite).

**Q: Can we integrate with existing systems?**  
A: Yes. The app can be extended to connect to SQL databases, REST APIs, or file shares. Contact the dev team for custom integrations.

**Next Steps for IT Team**

1. **Test in Staging**: Deploy to a test server and run through this demo script
2. **Load Test**: Simulate 10-20 concurrent users
3. **Security Review**: Validate input sanitization, session handling
4. **Backup Strategy**: Set up automated backups for `data/` directory
5. **Monitoring**: Configure server monitoring (CPU, memory, disk, logs)
6. **User Training**: Schedule training sessions using `docs/USER_MANUAL.md`
7. **Phase 2 Planning**: Prioritize database persistence and authentication

---

## Demo Wrap-Up Script

**Script**:
> "That concludes the demo of the OCSS Command Center. We've covered all five roles, demonstrated key workflows, and validated system functionality. Questions?"

**Key Takeaways**:
- Role-based dashboard simplifies user experience
- Caseload management enforces accountability with audit trails
- Worker Self-Pull feature empowers teams while preventing conflicts
- Validation and deduplication keep data clean
- Session-based storage is fine for proof-of-concept; database integration needed for production
- System is ready for user acceptance testing and staging deployment

---

**End of Demo Script**

For technical support during deployment, refer to:
- `docs/IT_IMPLEMENTATION_GUIDE.md`
- `docs/TECHNICAL_GUIDE.md`
- `docs/IT_QUICK_START.md`

Contact: dev-team@ocss.agency.gov
