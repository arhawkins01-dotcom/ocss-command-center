import re
import os

with open('docs/USER_MANUAL.md', 'r') as f:
    text = f.read()

# Update Roles section in USER_MANUAL.md
text = re.sub(
    r'(### Department Manager / Senior Administrative Officer\n- Purpose: Operational oversight for units or regions\n)- Key views: Unit KPIs, Reassignments, Team Performance',
    r'\1- Key views: Unit KPIs (Department scope for DM; Unit/Dept/Agency scope for SAO), QA Data Exports, Reassignments, Team Performance',
    text
)

text = re.sub(
    r'(### Director / Deputy Director\n- Purpose: Strategic oversight, leadership exports, escalation decisions\n)- Key views: Organization-level KPIs, Caseload Work Status, Leadership Exports',
    r'\1- Key views: Organization-level KPIs, Caseload Work Status, Team Performance Analytics, Leadership QA Exports',
    text
)

text = re.sub(
    r'(### Supervisor\n- Purpose: Team-level assignment, approve caseload submissions, and monitor team alerts\n)- Key views: My Team & Assignments, Worker Self-Pull, Team Performance',
    r'\1- Key views: KPI Metrics (Unit/Department scoped), QA Data Exports, My Team & Assignments, Worker Self-Pull, Team Performance Analytics',
    text
)

text = re.sub(
    r'(### Program Officer\n- Purpose: Upload and seed reports, validate ingestion, and monitor program-level throughput\n)- Key views: Upload & Processing, Ingestion Registry, Program KPIs',
    r'\1- Key views: Upload & Processing, Ingestion Registry, Program KPIs, Team Performance Analytics, Leadership QA Exports',
    text
)

# Update KPIs section
text = re.sub(
    r'(## KPIs & Metrics Dashboards\n\nDashboards show throughput.*?\n\n- Reports Ingested \(period\)\n- Average Days to Complete\n- % Completed On Time\n- Unassigned Caseloads\n- Escalations by Age Bucket\n\n)Leadership exports produce Excel and Word briefing packets with pre-formatted summaries and an ingestion activity sheet.',
    r'\1Leadership exports produce Excel and Word briefing packets with pre-formatted summaries and an ingestion activity sheet. Exports are now directly available on the root KPI Metrics tab across all executive roles (Director, Deputy Director, Program Officer, Department Manager, SAO, and Supervisor). These exports include comprehensive QA flag summaries (FAIL/WARN/INFO/OK metrics with top failure reasons). Additionally, executive and supervisory roles now feature robust Team Performance Analytics views utilizing visual progress bars for individual worker completion rates.',
    text
)

with open('docs/USER_MANUAL.md', 'w') as f:
    f.write(text)

with open('app/knowledge_base/user_guide.md', 'r') as f:
    kb_text = f.read()

kb_text = re.sub(
    r'(\*\*📊 KPIs & Metrics Tab\*\*\n- \*\*Alerts \(Escalation\)\*\*:.*?)\n- View organizational performance metrics:',
    r'\1\n- **Leadership QA Exports**: Export live dashboard stats to an Excel/Word document directly from this tab (includes KPI and QA Flags summary sheets)\n- View organizational performance metrics:',
    kb_text, count=1
)

kb_text = re.sub(
    r'(### Department Manager\n.*?Department Managers have).*?( alerts, caseload rollups, and leadership exports. Key features:\n)- Department KPI tab: view escalations and caseload work-status filtered to units that belong to the manager\'s department',
    r'\1 department-scoped access to\2- Department KPI tab: view escalations, caseload work-status, and monthly submission rates filtered to your department\n- Leadership QA Exports located directly at top of KPI tab\n- **Team Performance Analytics**: View individual completion rate progress bars for all supervised and department staff',
    kb_text, count=1
)

kb_text = re.sub(
    r'(### Senior Administrative Officer\n.*?The Senior Administrative Officer \(SAO\) maps to the Supervisor view with additional leadership capabilities\. SAOs can:\n)- Access team-level caseload status and performance analytics\n- Run leadership exports scoped to their oversight area',
    r'\1- Access team-level caseload status and individual performance analytics\n- Toggle KPI Metrics view between Unit, Department, and Agency scopes\n- Run leadership QA exports directly from the KPI Metrics tab',
    kb_text, count=1
)

kb_text = re.sub(
    r'(### Supervisor\n.*?#### Dashboard Features\n\n)',
    r'\1**📊 KPI Metrics Tab**\n- View KPIs scoped by Unit or Department\n- Access Leadership QA Exports (Excel/Word) directly from this tab\n- Review individual progress completion bars for team members in Performance Analytics\n\n',
    kb_text, count=1
)

with open('app/knowledge_base/user_guide.md', 'w') as f:
    f.write(kb_text)

