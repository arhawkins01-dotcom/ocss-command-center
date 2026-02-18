# OCSS Command Center - User Manual

**Version 1.0.0**  
**Last Updated: February 18, 2026**

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
- **Team Coordination**: Supervisors manage units and assign work to team members
- **Audit Trail**: All assignment changes are logged for accountability

### System Requirements

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Network access to the OCSS Command Center server
- Your assigned username/credentials (when authentication is enabled)

---

## Getting Started

### Accessing the System

1. Open your web browser
2. Navigate to: `http://[your-server-address]:8501`
3. The dashboard will load automatically

### Selecting Your Role

On the left sidebar, use the **"Select Your Role"** radio buttons to choose your role:
- Director
- Program Officer
- Supervisor
- Support Officer
- IT Administrator

The main content area will update to show features relevant to your role.

---

## Role-Specific Guides

### Director

**Purpose**: Executive oversight, strategic planning, and performance monitoring.

#### Dashboard Features

**📊 KPIs & Metrics Tab**
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

**📋 Team Performance Tab**
- Individual worker performance comparison
- Team efficiency metrics
- Quality scores by team

#### Quick Actions

- Monitor high-level trends
- Identify teams needing support
- Export reports for executive briefings

---

### Program Officer

**Purpose**: Upload establishment reports and manage caseload data.

#### Dashboard Features

**📤 Upload Reports Tab**

1. **Select Caseload**: Choose the target caseload (181000, 181001, 181002, etc.)
2. **Upload File**: Click "Browse files" and select an Excel (.xlsx) or CSV file
3. **Review Preview**: The system displays:
   - File name and size
   - Number of rows and columns
   - Data preview (first 5 rows)
4. **Confirm Upload**: Click "📤 Upload to Caseload"
5. **View Status**: Uploaded reports appear in Recent Uploads list

**📊 Caseload Overview Tab**
- View all active caseloads
- See upload statistics by caseload
- Monitor report status

**📋 Report Status Tab**
- Track reports in progress
- View completion status
- Export summary data

#### Best Practices

- **File Format**: Use standardized Excel templates for consistent data structure
- **Naming Convention**: Name files clearly (e.g., `ENV_Report_Q1_2026.xlsx`)
- **Data Validation**: Review the preview before uploading to catch errors early
- **Regular Uploads**: Upload reports as soon as they're prepared to keep work flowing

---

### Supervisor

**Purpose**: Manage your unit, assign caseloads to team members, and monitor team performance.

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

This feature allows team members to claim unassigned caseloads for themselves.

1. **Worker Action**:
   - Enter your name in "Simulate Current Worker"
   - Select yourself in "Pull As" (must match)
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

#### Supervisor Best Practices

- **Balance Workload**: Distribute caseloads evenly across team members
- **Monitor Progress**: Check team performance metrics weekly
- **Support Struggling Workers**: Reassign if someone is overloaded
- **Encourage Self-Pull**: Let workers claim new work when they have capacity
- **Audit Trail**: All assignments are logged; you can review changes in IT Admin view

---

### Support Officer

**Purpose**: Process assigned reports for your caseloads and provide technical support.

#### Dashboard Features

**Act as Support Officer / Team Lead**

Since authentication is not yet enabled, select your name from the dropdown to view your assignments.

**Caseload Metrics**
- **Assigned Caseloads**: Number of caseloads you're responsible for
- **Active Reports**: Total reports available for processing
- **Pending Approval**: Reports awaiting review
- **Status**: Your current work status

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
- View all reports assigned to you
- Filter by status, priority, due date
- Sort reports
- Track progress

**🆘 Support Tickets Tab**
- View and manage support requests related to your caseloads

**📚 Knowledge Base Tab**
- Access documentation and guides
- Search for solutions to common issues

#### Support Officer Best Practices

- **Select Yourself**: Always choose your name in the dropdown to see your work
- **Review Data Carefully**: Check all fields before approving reports
- **Use CSV Export**: Download data for offline analysis or archiving
- **Update Status**: Mark reports as approved/submitted to keep workflow moving
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

**👥 User & Caseload Management Tab**

**Current User (for audit)**:
- Enter your name so audit entries record who made changes

**Organization Metrics**:
- Total users, assigned reports, completion rates

**Add/Remove Users**:
1. Enter new user name
2. Select role (Support Officer, Program Officer, Supervisor)
3. Select department
4. Click **"➕ Add User"** (future feature)

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
2. Go to **📤 Upload Reports** tab
3. Select target caseload (e.g., 181000)
4. Click **"Browse files"**
5. Select Excel or CSV file
6. Review preview
7. Click **"📤 Upload to Caseload"**
8. Confirm upload appears in Recent Uploads

### How to Claim a Caseload (Support Officer via Supervisor View)

1. Select **Supervisor** role
2. Choose your supervisor in the dropdown
3. Go to **👥 My Team & Assignments** tab
4. In **Worker Self-Pull** section:
   - Enter your name in "Simulate Current Worker"
   - Select yourself in "Pull As"
   - Choose available caseload
   - Check availability hint
5. Click **"🧷 Pull Caseload to Self"**
6. System confirms claim

### How to Process a Report (Support Officer)

1. Select **Support Officer** role
2. Choose your name in "Act as Support Officer / Team Lead"
3. Go to **📊 Caseload Dashboard** tab
4. Select your assigned caseload
5. Expand a report card
6. Edit fields in the form
7. Click **"💾 Update Report"**
8. Use action buttons:
   - **📥 Download CSV** for offline work
   - **✅ Approve** when complete
   - **📤 Submit** for review

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

### I can't pull a caseload (Support Officer/Supervisor)

**Possible Reasons**:
- Caseload already assigned to someone else (check availability hint)
- "Simulate Current Worker" doesn't match "Pull As"
- You're not in the worker list for this unit

**Solution**:
- Check the availability hint (orange warning shows current owner)
- Ensure both fields have your exact name
- Ask supervisor to reassign if you need a caseload held by someone else

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

**Solution**:
- Ensure you clicked **"💾 Update Report"** inside the form
- Check for success message (green checkmark)
- Note: Session-based storage means data resets if server restarts; export CSV for backup

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
