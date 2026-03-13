
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import os
import json

# 56RA Report Actions and Statuses
RA_ACTIONS = [
    "Scheduled GT", "Pending GTU", "Prepped ADS", "Pending AHU", "Referred to Court",
    "Pending Court", "Sent Contact Letter", "Sent COBO Letter(s)", "Sent Postal Verification",
    "Closed Case", "NCP Unlocatable", "Order Already Established", "Case Already Closed", "OTHER"
]

# Page configuration
st.set_page_config(
    page_title="OCSS Command Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_reports' not in st.session_state:
    st.session_state.uploaded_reports = []

# Initialize uploaded reports by caseload (for Program Officer to upload)
if 'reports_by_caseload' not in st.session_state:
    st.session_state.reports_by_caseload = {'181000': [], '181001': [], '181002': []}

# Organizational units: supervisors, team leads, support officers and caseload assignments
if 'units' not in st.session_state:
    st.session_state.units = {
        'OCSS North': {
            'supervisor': 'Alex Martinez',
            'team_leads': ['Sarah Johnson'],
            'support_officers': ['Michael Chen', 'Jessica Brown'],
            'assignments': {
                'Sarah Johnson': ['181000'],
                'Michael Chen': ['181001'],
                'Jessica Brown': ['181002']
            }
        },
        'OCSS South': {
            'supervisor': 'Priya Singh',
            'team_leads': ['David Martinez'],
            'support_officers': ['Amanda Wilson'],
            'assignments': {
                'David Martinez': ['181001'],
                'Amanda Wilson': ['181000']
            }
        }
    }
# Sidebar - Role Selection
st.sidebar.title("🎯 OCSS Command Center")
st.sidebar.markdown("---")

role = st.sidebar.radio(
    "Select Your Role:",
    ["Director", "Program Officer", "Supervisor", "Support Officer", "IT Administrator"],
    help="Choose your role to see relevant features"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Quick Stats
- **Establishments**: 45
- **Reports Pending**: 12
- **Reports Completed**: 389
- **Last Update**: Today
""")

# Main content area
if role == "Director":
    st.markdown('<div class="header-title">📈 Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Strategy & Oversight**")
    
    # Tabs for Director
    dir_tab1, dir_tab2, dir_tab3 = st.tabs(["📊 KPIs & Metrics", "👥 Caseload Management", "📋 Team Performance"])
    
    with dir_tab1:
        # KPI Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Report Completion Rate", "89.3%", "+2.1%")
        with col2:
            st.metric("On-Time Submissions", "94%", "+1.5%")
        with col3:
            st.metric("Data Quality Score", "96.7%", "+0.3%")
        with col4:
            st.metric("CQI Alignments", "34", "+5")
        
        # Performance Chart
        st.subheader("Monthly Report Submissions")
        months = pd.date_range(start='2025-09-01', periods=6, freq='M').strftime('%b').tolist()
        submissions = [45, 48, 52, 50, 58, 62]
        chart_data = pd.DataFrame({
            'Month': months,
            'Submissions': submissions
        })
        st.bar_chart(chart_data.set_index('Month'))
        
        # Strategic Insights
        col1, col2 = st.columns(2)
        with col1:
            st.info("✅ **Strategic Wins**: All establishments now submitting reports on schedule")
        with col2:
            st.warning("⚠️ **Action Items**: 3 establishments need compliance support")
    
    with dir_tab2:
        st.subheader("👥 Caseload Management - All Workers")
        
        # Worker Caseload Overview
        workers_data = pd.DataFrame({
            'Worker Name': ['Sarah Johnson', 'Michael Chen', 'Jessica Brown', 'David Martinez', 'Amanda Wilson'],
            'Role': ['Support Officer', 'Support Officer', 'Support Officer', 'Support Officer', 'Support Officer'],
            'Total Assigned': [24, 28, 22, 26, 25],
            'Completed': [12, 18, 15, 14, 16],
            'In Progress': [8, 7, 5, 9, 6],
            'Not Started': [4, 3, 2, 3, 3],
            'Completion %': ['50%', '64%', '68%', '54%', '64%'],
            'Avg Time/Report': ['2.1 hrs', '1.8 hrs', '1.6 hrs', '2.0 hrs', '1.9 hrs']
        })
        
        st.dataframe(workers_data, use_container_width=True)
        
        # Workload Distribution Chart
        st.subheader("Workload Distribution by Worker")
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(workers_data.set_index('Worker Name')[['Total Assigned', 'Completed']])
        with col2:
            st.bar_chart(workers_data.set_index('Worker Name')[['Not Started', 'In Progress', 'Completed']])
        
        # Reassign Reports
        st.subheader("📋 Reassign Reports Between Workers")
        col1, col2, col3 = st.columns(3)
        with col1:
            from_worker = st.selectbox("From Worker", workers_data['Worker Name'].tolist())
        with col2:
            to_worker = st.selectbox("To Worker", workers_data['Worker Name'].tolist())
        with col3:
            num_reports = st.number_input("Number of Reports", min_value=1, max_value=10, value=1)
        
        if st.button("🔄 Execute Reassignment", key="director_reassign"):
            st.success(f"✓ {num_reports} report(s) reassigned from {from_worker} to {to_worker}")
    
    with dir_tab3:
        st.subheader("📊 Team Performance Analytics")
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Team Avg Completion", "60%", "+5%")
        with col2:
            st.metric("Team Avg Quality", "96%", "+1%")
        with col3:
            st.metric("Team Efficiency", "1.9 hrs/report", "-0.2 hrs")
        
        # Worker comparison
        st.write("**Individual Performance**")
        for idx, worker in enumerate(workers_data['Worker Name']):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**{worker}**")
            with col2:
                st.progress(int(workers_data['Completion %'].iloc[idx].rstrip('%')) / 100)
            with col3:
                st.metric("Completed", workers_data['Completed'].iloc[idx])
            with col4:
                st.metric("Avg Time", workers_data['Avg Time/Report'].iloc[idx])
            st.divider()

elif role == "Program Officer":
    st.markdown('<div class="header-title">📋 Report Intake Portal</div>', unsafe_allow_html=True)
    st.markdown("**Report Intake & Processing**")
    
    # Tabs for Program Officer
    prog_tab1, prog_tab2 = st.tabs(["📤 Upload & Processing", "👥 Caseload Management"])
    
    with prog_tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Upload Establishment Report")
            
            # Select caseload for upload
            caseload_options = {'181000': 'Downtown Elementary', '181001': 'Midtown Middle School', '181002': 'Uptown High School'}
            selected_caseload = st.selectbox(
                "Select Caseload for Upload",
                list(caseload_options.keys()),
                format_func=lambda x: f"{x} - {caseload_options[x]}"
            )
            
            uploaded_file = st.file_uploader("Choose an Excel file", type=['xls', 'xlsx', 'csv'])
            
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Read Excel file
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    st.info(f"📊 File has {len(df)} rows and {len(df.columns)} columns")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    df = None
                
                if st.button("Process Report", key="process_report_btn"):
                    # Store in reports_by_caseload for Support Officer to see
                    report_entry = {
                        'filename': uploaded_file.name,
                        'timestamp': datetime.now(),
                        'status': 'Ready for Processing',
                        'report_id': f"RPT-{selected_caseload}-{len(st.session_state.reports_by_caseload[selected_caseload])+1:03d}",
                        'data': df if df is not None else pd.DataFrame(),
                        'uploaded_by': 'Program Officer'
                    }
                    
                    # Also add to main uploaded_reports for tracking
                    st.session_state.uploaded_reports.append({
                        'filename': uploaded_file.name,
                        'timestamp': datetime.now(),
                        'status': 'Completed',
                        'caseload': selected_caseload
                    })
                    
                    # Add to caseload-specific list for Support Officer access
                    st.session_state.reports_by_caseload[selected_caseload].append(report_entry)
                    
                    st.success(f"✓ Report {report_entry['report_id']} processed and assigned to Support Officer!")
                    st.balloons()
        
        with col2:
            st.metric("Reports Today", len(st.session_state.uploaded_reports))
            st.metric("Successfully Processed", sum(1 for r in st.session_state.uploaded_reports if r['status'] == 'Completed'))
        
        # Show Uploaded Reports
        if st.session_state.uploaded_reports:
            st.subheader("📤 Reports Successfully Processed")
            
            # Editable report list with rename functionality
            for report_idx, report in enumerate(st.session_state.uploaded_reports):
                col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1.5])
                with col1:
                    st.write(f"**Original:** {report['filename']}")
                with col2:
                    new_name = st.text_input(
                        "Rename to",
                        value=report.get('renamed_to', report['filename']),
                        key=f"rename_{report_idx}",
                        placeholder="Edit report name..."
                    )
                with col3:
                    st.caption(f"Processed: {report['timestamp'].strftime('%b %d, %I:%M %p')}")
                with col4:
                    if st.button("✏️ Update", key=f"update_name_{report_idx}", use_container_width=True):
                        st.session_state.uploaded_reports[report_idx]['renamed_to'] = new_name
                        st.success(f"✓ Renamed to: {new_name}")
            
            # Display updated list
            st.divider()
            st.write("**Final Report Names:**")
            for idx, report in enumerate(st.session_state.uploaded_reports):
                final_name = report.get('renamed_to', report['filename'])
                st.caption(f"📄 {final_name}")
            
            if st.button("🗑️ Clear Processed Reports"):
                st.session_state.uploaded_reports = []
                st.rerun()
        else:
            st.info("📝 No reports processed yet. Upload an establishment report above to begin.")
        
        st.divider()
        
        # Pending Reports
        st.subheader("Pending Review")
        pending_data = {
            'Establishment': ['Lincoln Elementary', 'Grant Middle School', 'Jefferson HS', 'Adams Preschool'],
            'Submitted': ['2 days ago', '5 days ago', '1 week ago', '3 days ago'],
            'Status': ['Ready', 'In Review', 'Flagged', 'Ready']
        }
        st.dataframe(pd.DataFrame(pending_data), use_container_width=True)
        
        # Quality Checks
        st.subheader("Quality Assurance Checklist")
        st.checkbox("✓ All required fields present")
        st.checkbox("✓ Data format validation passed")
        st.checkbox("✓ No duplicate records")
        st.checkbox("✓ CQI alignment verified")
    
    with prog_tab2:
        st.subheader("👥 Processing Team Caseload")
        
        # Officer Caseload Overview
        officers_data = pd.DataFrame({
            'Officer Name': ['Sarah Johnson', 'Michael Chen', 'Jessica Brown'],
            'Total Processed': [145, 152, 138],
            'Today': [12, 15, 9],
            'This Week': [62, 71, 58],
            'Average Quality': ['96%', '97%', '95%'],
            'Processing Speed': ['12 min/report', '11 min/report', '13 min/report']
        })
        
        st.dataframe(officers_data, use_container_width=True)
        
        # Processing metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Team Total Processed", "435", "+25")
        with col2:
            st.metric("Avg Quality", "96%", "+1%")
        with col3:
            st.metric("Avg Processing Time", "12 min/report", "-1 min")
        
        # Officer comparison
        st.subheader("Officer Performance")
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(officers_data.set_index('Officer Name')[['Today', 'This Week']])
        with col2:
            st.bar_chart(officers_data.set_index('Officer Name')['Average Quality'])

elif role == "Supervisor":
    st.markdown('<div class="header-title">📊 KPI Monitoring Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Real-Time KPI Visibility**")
    
    # Tabs for Supervisor
    sup_tab1, sup_tab2, sup_tab3 = st.tabs(["📊 KPI Metrics", "👥 Team Caseload", "📈 Performance Analytics"])
    
    with sup_tab1:
        # KPI Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Response Time", "2.3 days", "-0.5 days")
        with col2:
            st.metric("Quality Score", "94.2%", "+2.1%")
        with col3:
            st.metric("Team Compliance", "100%", "✓")
        
        # Establishment Performance
        st.subheader("Establishment Performance")
        
        establishments = pd.DataFrame({
            'Establishment': ['Lincoln Elem', 'Grant Middle', 'Jefferson HS', 'Adams Presch', 'Madison Elem'],
            'Reports Submitted': [45, 38, 42, 35, 48],
            'Avg Quality Score': [96, 92, 94, 91, 97],
            'Last Submission': ['Today', '2 days', 'Today', '5 days', 'Yesterday']
        })
        st.dataframe(establishments, use_container_width=True)
        
        # Trend Analysis
        st.subheader("Quality Trend")
        dates = pd.date_range(start='2025-08-01', periods=60, freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Quality Score': np.random.uniform(88, 98, 60)
        })
        st.line_chart(trend_data.set_index('Date'))
    
    with sup_tab2:
        st.subheader("👥 Team Caseload Management")

        # Supervisor selector (view by unit)
        supervisors = []
        for unit_name, unit in st.session_state.units.items():
            supervisors.append(unit.get('supervisor'))
        supervisors = [s for s in supervisors if s]

        selected_supervisor = st.selectbox("Select Supervisor to View", options=['(Select)'] + supervisors)

        if selected_supervisor and selected_supervisor != '(Select)':
            # Find unit for this supervisor
            unit_found = None
            for unit_name, unit in st.session_state.units.items():
                if unit.get('supervisor') == selected_supervisor:
                    unit_found = (unit_name, unit)
                    break

            if unit_found:
                unit_name, unit = unit_found
                st.markdown(f"**Unit:** {unit_name}")
                st.markdown(f"**Team Lead(s):** {', '.join(unit.get('team_leads', []))}")
                st.markdown(f"**Support Officers:** {', '.join(unit.get('support_officers', []))}")

                # Build team overview
                team_list = unit.get('support_officers', []) + unit.get('team_leads', [])
                if team_list:
                    team_workers = pd.DataFrame({
                        'Worker Name': team_list,
                        'Total Assigned': [len(unit.get('assignments', {}).get(w, [])) for w in team_list],
                        'Assigned Caseloads': [', '.join(unit.get('assignments', {}).get(w, [])) for w in team_list]
                    })
                    st.dataframe(team_workers, use_container_width=True)

                    # Reassign Reports (within unit)
                    st.subheader("📋 Reassign Reports Within Unit")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        from_worker = st.selectbox("From Worker", team_list, key="from_worker_unit")
                    with col2:
                        to_worker = st.selectbox("To Worker", team_list, key="to_worker_unit")
                    with col3:
                        caseload_choice = st.selectbox("Caseload to move", options=sum([unit.get('assignments', {}).get(w, []) for w in team_list], []), key="caseload_move")

                    if st.button("🔄 Move Caseload", key="move_caseload_unit"):
                        # perform move
                        if caseload_choice in st.session_state.units[unit_name]['assignments'].get(from_worker, []):
                            st.session_state.units[unit_name]['assignments'][from_worker].remove(caseload_choice)
                            st.session_state.units[unit_name]['assignments'].setdefault(to_worker, []).append(caseload_choice)
                            st.success(f"✓ Caseload {caseload_choice} moved from {from_worker} to {to_worker}")
                        else:
                            st.error("Selected caseload not found for the source worker")

                    st.divider()
                    # Worker Self-Pull: allow workers to pull a caseload only to themselves (no claiming for others)
                    st.subheader("🤝 Worker Self-Pull (Claim a Caseload)")
                    # Simulate current worker identity (no auth yet)
                    cur_worker = st.text_input("Simulate Current Worker", value=st.session_state.get('current_worker', ''), help="Enter your worker name to claim caseloads")
                    if cur_worker:
                        st.session_state.current_worker = cur_worker.strip()

                    pull_col1, pull_col2 = st.columns(2)
                    with pull_col1:
                        pull_worker = st.selectbox("Pull As (must match 'Simulate Current Worker')", options=team_list, key="pull_worker_select")
                    with pull_col2:
                        # Available caseloads across unit (flattened)
                        available = sum([unit.get('assignments', {}).get(w, []) for w in team_list], [])
                        # Also include any caseloads that exist but are unassigned
                        unassigned = [c for c in st.session_state.reports_by_caseload.keys() if not any(c in lst for u in st.session_state.units.values() for lst in u.get('assignments', {}).values())]
                        pull_options = sorted(list(set(available + unassigned)))
                        pull_caseload = st.selectbox("Caseload to Claim (to self)", options=pull_options, key="pull_caseload_select")

                        # Show availability hint for the selected caseload
                        assigned_owner = None
                        for uname, u in st.session_state.units.items():
                            for person, caselist in u.get('assignments', {}).items():
                                if pull_caseload in caselist:
                                    assigned_owner = {'unit': uname, 'person': person}
                                    break
                            if assigned_owner:
                                break

                        if assigned_owner:
                            if assigned_owner['person'] == pull_worker and assigned_owner['unit'] == unit_name:
                                st.info(f"Caseload {pull_caseload} is already assigned to {assigned_owner['person']} in this unit.")
                            else:
                                st.warning(f"Caseload {pull_caseload} is currently assigned to {assigned_owner['person']} in unit '{assigned_owner['unit']}'.")

                    if st.button("🧷 Pull Caseload to Self", key="pull_to_self"):
                        if not st.session_state.get('current_worker'):
                            st.error("Set 'Simulate Current Worker' to your name before pulling a caseload.")
                        elif pull_worker != st.session_state.get('current_worker'):
                            st.error("You can only pull a caseload for yourself. Make sure 'Pull As' matches the simulated current worker.")
                        else:
                            # Dedup: ensure caseload not already assigned to someone else
                            already_assigned = None
                            for uname, u in st.session_state.units.items():
                                for person, caselist in u.get('assignments', {}).items():
                                    if pull_caseload in caselist:
                                        already_assigned = (uname, person)
                                        break
                                if already_assigned:
                                    break

                            if already_assigned:
                                # If already assigned to this same person in this unit, inform
                                if already_assigned[1] == pull_worker and already_assigned[0] == unit_name:
                                    st.info(f"Caseload {pull_caseload} is already assigned to you in unit '{unit_name}'.")
                                else:
                                    st.error(f"Caseload {pull_caseload} is already assigned to {already_assigned[1]} in unit '{already_assigned[0]}'. Cannot pull.")
                            else:
                                # Assign to the pull_worker within this unit
                                st.session_state.units[unit_name].setdefault('assignments', {}).setdefault(pull_worker, []).append(pull_caseload)
                                st.success(f"✓ Caseload {pull_caseload} claimed by {pull_worker} in unit '{unit_name}'")
                else:
                    st.info("No team members assigned yet for this supervisor")
            else:
                st.error("Supervisor not found in any unit")
        else:
            st.info("Select a supervisor to view their unit and team caseloads")
    
    with sup_tab3:
        st.subheader("📈 Team Performance Analytics")
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Team Avg Completion", "58%", "+3%")
        with col2:
            st.metric("Avg Quality", "94% ", "+2%")
        with col3:
            st.metric("Team Efficiency", "1.96 hrs/report", "-0.1 hrs")
        
        # Worker comparison
        st.write("**Individual Performance**")
        if 'team_workers' in locals() and isinstance(team_workers, pd.DataFrame) and not team_workers.empty:
            for idx, worker in enumerate(team_workers['Worker Name']):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{worker}**")
                with col2:
                    # Safely handle missing completion % or non-standard values
                    try:
                        comp_pct = int(str(team_workers.get('Completion %', pd.Series()).iloc[idx]).rstrip('%'))
                        st.progress(comp_pct / 100)
                    except Exception:
                        st.progress(0)
                with col3:
                    st.metric("Completed", team_workers.get('Completed', pd.Series()).iloc[idx] if 'Completed' in team_workers.columns else "-")
                with col4:
                    st.metric("Avg Time", team_workers.get('Avg Time/Report', pd.Series()).iloc[idx] if 'Avg Time/Report' in team_workers.columns else "-")
                st.divider()
        else:
            st.info("No team data available — select a supervisor and load the unit first.")


elif role == "Support Officer":
    st.markdown('<div class="header-title">📋 Support Officer - Caseload Management</div>', unsafe_allow_html=True)
    st.markdown("**Assigned Reports & Technical Support**")

    # Choose which Support Officer you are acting as (since no auth yet)
    all_sos = []
    for unit in st.session_state.units.values():
        all_sos.extend(unit.get('support_officers', []))
        all_sos.extend(unit.get('team_leads', []))
    all_sos = sorted(list(set(all_sos)))

    acting_so = st.selectbox("Act as Support Officer / Team Lead", options=['(Select)'] + all_sos)

    # Caseload Metrics (for selected person)
    col1, col2, col3, col4 = st.columns(4)
    if acting_so and acting_so != '(Select)':
        # find caseloads assigned across units
        assigned_caseloads = []
        for unit in st.session_state.units.values():
            for person, caseloads in unit.get('assignments', {}).items():
                if person == acting_so:
                    assigned_caseloads.extend(caseloads)

        st.session_state.setdefault('last_acting_so', acting_so)
        with col1:
            st.metric("Assigned Caseloads", len(assigned_caseloads))
        with col2:
            st.metric("Active Reports", sum(len(st.session_state.reports_by_caseload.get(c, [])) for c in assigned_caseloads))
        with col3:
            st.metric("Pending Approval", 0)
        with col4:
            st.metric("Status", "Active")
    else:
        with col1:
            st.metric("Assigned Caseloads", "-", "-")
        with col2:
            st.metric("Active Reports", "-", "-")
        with col3:
            st.metric("Pending Approval", "-", "-")
        with col4:
            st.metric("Status", "Select yourself to view")

    # Tab Navigation (add 56RA Processing tab)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Caseload Dashboard", "📝 My Assigned Reports", "🆘 Support Tickets", "📚 Knowledge Base", "📑 56RA Processing", "📑 Locate Report Processing", "📑 Paternity-Support Processing"])
    # TAB 7: Paternity-Support Report Processing
    with tab7:
        st.subheader("📑 Paternity-Support (P-S) Report Processing")
        st.caption("Process each case according to Paternity-Support Work List instructions. Only Supervisors/PO3 can close cases or email completed spreadsheets.")

        # Example: Replace with real data source as needed
        ps_cases = [
            {"Case ID": "PS-001", "Status": "Pending-GTU", "NCP": "Jordan Miles", "CP": "Taylor Brooks"},
            {"Case ID": "PS-002", "Status": "Order Already Established", "NCP": "Morgan Lee", "CP": "Chris Fox"},
            {"Case ID": "PS-003", "Status": "NCP Unlocatable", "NCP": "Alex Kim", "CP": "Jamie Ray"},
        ]
        PS_ACTIONS = [
            "GT", "ADS", "COURT REFERRAL", "CONTACT LETTER", "POSTAL", "CLOSED CASE", "NCP UNLOCATABLE",
            "PENDING-GTU", "PENDING-AHU", "PENDING-COURT", "Order Already Established", "Case Already Closed", "OTHER"
        ]
        for case in ps_cases:
            with st.expander(f"Case {case['Case ID']} - {case['Status']}"):
                action = st.selectbox("Action Taken", PS_ACTIONS, key=f"ps_action_{case['Case ID']}")
                date_action = st.date_input("Date Action Taken", value=datetime.now(), key=f"ps_date_{case['Case ID']}")
                order_established = st.checkbox("Order Already Established", key=f"ps_order_{case['Case ID']}")
                already_closed = st.checkbox("Case Already Closed", key=f"ps_closed_{case['Case ID']}")
                address_valid = st.checkbox("Valid NCP Address", key=f"ps_addr_{case['Case ID']}")
                ilsu_cleared = st.checkbox("Cleared ILSU", key=f"ps_ilsu_{case['Case ID']}")
                contact_attempted = st.checkbox("Attempted Contact with Client", key=f"ps_contact_{case['Case ID']}")
                comment = st.text_area("Comments", key=f"ps_comment_{case['Case ID']}")
                # Narration template
                narration_default = f"P-S Report: {case['Status']}. Action Taken: {action}. {comment}"
                narration = st.text_area(
                    "Narration (auto or manual)",
                    value=narration_default,
                    key=f"ps_narration_{case['Case ID']}"
                )
                # Only allow closing if Supervisor/PO3 (simulate with acting_so)
                can_close = acting_so in [u.get('supervisor') for u in st.session_state.units.values()] or acting_so.endswith('PO3')
                if action == "CLOSED CASE" and not can_close:
                    st.warning("Only Supervisors or Establishment PO3 can close cases.")
                if st.button("💾 Save/Submit", key=f"ps_submit_{case['Case ID']}"):
                    st.success(f"Case {case['Case ID']} updated.")
        st.info("When finished, only Supervisors/PO3 can email the completed spreadsheet.")

    # ...existing code for tab1, tab2, tab3, tab4...

    # TAB 5: 56RA Processing
    with tab5:
        st.subheader("📑 56RA Report Processing")
        st.caption("Process each case according to 56RA instructions. Only Supervisors/PO3 can close cases or email completed spreadsheets.")

        # Example: Replace with real data source as needed
        # For demo, create a few sample cases
        cases = [
            {"Case ID": "C-001", "Status": "Pending GTU", "NCP": "John Doe", "CP": "Jane Smith"},
            {"Case ID": "C-002", "Status": "Order Already Established", "NCP": "Mike Lee", "CP": "Anna Kim"},
            {"Case ID": "C-003", "Status": "NCP Unlocatable", "NCP": "Chris Ray", "CP": "Pat Lee"},
        ]
        for case in cases:
            with st.expander(f"Case {case['Case ID']} - {case['Status']}"):
                action = st.selectbox("Action Taken/Status", RA_ACTIONS, key=f"action_{case['Case ID']}")
                date_action = st.date_input("Date Action Taken", value=datetime.now(), key=f"date_{case['Case ID']}")
                narrated = st.checkbox("Case Narrated", key=f"narrated_{case['Case ID']}")
                comment = st.text_area("Comment", key=f"comment_{case['Case ID']}")
                # Narration template
                narration_default = f"56RA Report: {case['Status']}. Action Taken: {action}."
                narration = st.text_area(
                    "Narration (auto or manual)", 
                    value=narration_default,
                    key=f"narration_{case['Case ID']}"
                )
                # Only allow closing if Supervisor/PO3 (simulate with acting_so)
                can_close = acting_so in [u.get('supervisor') for u in st.session_state.units.values()] or acting_so.endswith('PO3')
                if action == "Closed Case" and not can_close:
                    st.warning("Only Supervisors or Establishment PO3 can close cases.")
                if st.button("💾 Save/Submit", key=f"submit_{case['Case ID']}"):
                    st.success(f"Case {case['Case ID']} updated.")
        st.info("When finished, only Supervisors/PO3 can email the completed spreadsheet.")

    # TAB 6: Locate Report Processing
    with tab6:
        st.subheader("📑 Locate Report Processing")
        st.caption("Process each case according to Locate Report instructions. Only Supervisors/PO3 can close cases or email completed spreadsheets.")

        # Example: Replace with real data source as needed
        locate_cases = [
            {"Case ID": "L-001", "Status": "In Locate", "NCP": "Sam Carter", "CP": "Alexis Lee"},
            {"Case ID": "L-002", "Status": "Potential UNL Closure", "NCP": "Jordan Smith", "CP": "Morgan Ray"},
            {"Case ID": "L-003", "Status": "Potential NAS Closure", "NCP": "Taylor Kim", "CP": "Jamie Fox"},
        ]
        LOCATE_ACTIONS = [
            "Searched Databases", "Requested CLEAR Search", "Cleared ILSU", "Attempted Contact CP/CTR/PPF/NCP",
            "Left Voicemail", "Received Address Info", "Sent JFS7711", "Closed UNL", "Closed NAS", "Case Remains in Locate", "OTHER"
        ]
        for case in locate_cases:
            with st.expander(f"Case {case['Case ID']} - {case['Status']}"):
                action = st.selectbox("Action Taken/Status", LOCATE_ACTIONS, key=f"locate_action_{case['Case ID']}")
                date_action = st.date_input("Date Action Taken", value=datetime.now(), key=f"locate_date_{case['Case ID']}")
                databases_cleared = st.text_input("Databases Searched (BMV, SVES, dockets, etc.)", key=f"dbs_{case['Case ID']}")
                ilsu_cleared = st.checkbox("Cleared ILSU", key=f"ilsu_{case['Case ID']}")
                contact_attempted = st.checkbox("Attempted Contact with CP/CTR/PPF/NCP", key=f"contact_{case['Case ID']}")
                comment = st.text_area("Comment", key=f"locate_comment_{case['Case ID']}")
                # Narration template
                narration_default = f"Locate Report: searched {databases_cleared or 'databases'}; action: {action}. {comment}"
                narration = st.text_area(
                    "Narration (auto or manual)",
                    value=narration_default,
                    key=f"locate_narration_{case['Case ID']}"
                )
                # Only allow closing if Supervisor/PO3 (simulate with acting_so)
                can_close = acting_so in [u.get('supervisor') for u in st.session_state.units.values()] or acting_so.endswith('PO3')
                if action in ["Closed UNL", "Closed NAS"] and not can_close:
                    st.warning("Only Supervisors or Establishment PO3 can close cases.")
                if st.button("💾 Save/Submit", key=f"locate_submit_{case['Case ID']}"):
                    st.success(f"Case {case['Case ID']} updated.")
        st.info("When finished, only Supervisors/PO3 can email the completed spreadsheet.")

elif role == "IT Administrator":
    st.markdown('<div class="header-title">⚙️ System Administration</div>', unsafe_allow_html=True)
    st.markdown("**Server Configuration & Monitoring**")
    
    # Tabs for IT Administrator
    it_tab1, it_tab2, it_tab3 = st.tabs(["🖥️ System Status", "👥 User & Caseload Management", "🛠️ Maintenance & Logs"])
    
    with it_tab1:
        # Server Status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Server Status", "🟢 Online", "Up 42 days")
        with col2:
            st.metric("Database Health", "✓ Optimal", "99.7% uptime")
        with col3:
            st.metric("Active Users", "23", "Peak: 47")
        
        # Configuration Paths
        st.subheader("Server Configuration Paths")
        config_info = """
        **Template Directory**: `S:\\OCSS\\CommandCenter\\Template`
        **Report Library**: `S:\\OCSS\\CommandCenter\\ReportLibrary`
        **Exports Archive**: `S:\\OCSS\\CommandCenter\\Exports`
        """
        st.info(config_info)
    
    with it_tab2:
        st.subheader("👥 User & Caseload Management")
        # Current user for audit purposes
        current_user = st.text_input("Current User (for audit)", value=st.session_state.get('current_user', ''), help="Enter your name to be recorded in audit entries.")
        if current_user:
            st.session_state.current_user = current_user
        
        # All Workers Across Organization
        all_workers = pd.DataFrame({
            'Worker Name': ['Sarah Johnson', 'Michael Chen', 'Jessica Brown', 'David Martinez', 'Amanda Wilson'],
            'Role': ['Support Officer', 'Support Officer', 'Support Officer', 'Support Officer', 'Support Officer'],
            'Department': ['OCSS North', 'OCSS South', 'OCSS Central', 'OCSS East', 'OCSS West'],
            'Total Assigned': [24, 28, 22, 26, 25],
            'Completed': [12, 18, 15, 14, 16],
            'In Progress': [8, 7, 5, 9, 6],
            'Completion %': ['50%', '64%', '68%', '54%', '64%']
        })
        
        st.dataframe(all_workers, use_container_width=True)
        
        # Organization Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(all_workers))
        with col2:
            st.metric("Total Assigned Reports", all_workers['Total Assigned'].sum())
        with col3:
            st.metric("Total Completed", all_workers['Completed'].sum())
        with col4:
            st.metric("Org Completion Rate", "60%")
        
        # User Management
        st.subheader("Add/Remove Users")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_user = st.text_input("New User Name")
        with col2:
            new_role = st.selectbox("Role", ["Support Officer", "Program Officer", "Supervisor"])
        with col3:
            new_dept = st.selectbox("Department", ["OCSS North", "OCSS South", "OCSS Central", "OCSS East", "OCSS West"])
        
        if st.button("➕ Add User"):
            st.success(f"✓ User '{new_user}' added as {new_role} in {new_dept}")
        
        # Bulk Caseload Assignment
        st.divider()
        st.subheader("📋 Bulk Caseload Assignment")
        col1, col2 = st.columns(2)
        with col1:
            selected_user = st.selectbox("Assign to User", all_workers['Worker Name'].tolist())
            caseload_size = st.number_input("Number of Reports", min_value=1, max_value=30, value=10)
        with col2:
            assignment_type = st.selectbox("Assignment Type", ["Automatic Distribution", "Manual Selection", "By Establishment"])
            priority = st.selectbox("Priority Level", ["All", "🔴 High Only", "🟡 Medium Only", "🟢 Low Only"])
        
        if st.button("📤 Assign Caseload"):
            st.success(f"✓ {caseload_size} reports assigned to {selected_user}")
        
        st.divider()
        st.subheader("🏷️ Unit Management")
        col1, col2 = st.columns(2)
        with col1:
            unit_names = list(st.session_state.units.keys())
            unit_choice = st.selectbox("Select Unit", options=['(New Unit)'] + unit_names)
            new_unit_name = st.text_input("New Unit Name", value="", placeholder="Enter unit name if creating new")
            supervisor_name = st.text_input("Supervisor Name", value="")
        with col2:
            team_lead = st.text_input("Team Lead Name", value="")
            support_officer = st.text_input("Support Officer Name", value="")
            caseload_to_assign = st.selectbox("Caseload to Assign", options=list(st.session_state.reports_by_caseload.keys()))

        if st.button("➕ Create/Update Unit"):
            # Determine target unit name
            provided_name = new_unit_name.strip()
            if unit_choice == '(New Unit)':
                if not provided_name:
                    st.error("Please provide a valid unit name when creating a new unit.")
                    st.stop()
                # Prevent case-insensitive duplicate unit names
                existing_lower = {u.lower(): u for u in st.session_state.units.keys()}
                if provided_name.lower() in existing_lower:
                    st.error(f"Unit '{provided_name}' already exists (case-insensitive match to '{existing_lower[provided_name.lower()]}'). Pick a different name or select the existing unit to update.")
                    st.stop()
                target_unit = provided_name
            else:
                target_unit = unit_choice

            # Ensure target unit record exists
            st.session_state.units.setdefault(target_unit, {'supervisor': '', 'team_leads': [], 'support_officers': [], 'assignments': {}})

            # Normalize and validate person names
            def norm(name):
                return name.strip()

            sup = norm(supervisor_name)
            tl = norm(team_lead)
            so = norm(support_officer)

            if sup:
                st.session_state.units[target_unit]['supervisor'] = sup

            # Add team lead if not duplicate (case-insensitive)
            if tl:
                existing_tls = [t.lower() for t in st.session_state.units[target_unit]['team_leads']]
                if tl.lower() not in existing_tls:
                    st.session_state.units[target_unit]['team_leads'].append(tl)

            # Add support officer if not duplicate (case-insensitive)
            if so:
                existing_sos = [s.lower() for s in st.session_state.units[target_unit]['support_officers']]
                if so.lower() not in existing_sos:
                    st.session_state.units[target_unit]['support_officers'].append(so)

            # Assign caseload with dedup checks
            if caseload_to_assign:
                assignee = so or tl
                if not assignee:
                    st.warning('No assignee provided for caseload; please enter a Support Officer or Team Lead name to assign.')
                else:
                    # Prevent same caseload assigned to multiple people across all units
                    already_assigned = None
                    for uname, u in st.session_state.units.items():
                        for person, caselist in u.get('assignments', {}).items():
                            if caseload_to_assign in caselist:
                                already_assigned = (uname, person)
                                break
                        if already_assigned:
                            break

                    if already_assigned:
                        # If it's already assigned to same person in same unit, ignore
                        if already_assigned == (target_unit, assignee):
                            st.info(f"Caseload {caseload_to_assign} already assigned to {assignee} in unit '{target_unit}'.")
                        else:
                            st.error(f"Caseload {caseload_to_assign} is already assigned to {already_assigned[1]} in unit '{already_assigned[0]}'. Remove existing assignment before reassigning.")
                            st.stop()
                    else:
                        # Safe to assign; ensure person's assignment list exists and dedupe
                        assignments = st.session_state.units[target_unit].setdefault('assignments', {})
                        person_list = assignments.setdefault(assignee, [])
                        if caseload_to_assign not in person_list:
                            person_list.append(caseload_to_assign)

            st.success(f"✓ Unit '{target_unit}' created/updated")

        # Quick view of units
        st.write("**Current Units:**")
        for uname, u in st.session_state.units.items():
            st.markdown(f"- **{uname}** — Supervisor: {u.get('supervisor')} — Team Leads: {', '.join(u.get('team_leads', []))} — Support Officers: {', '.join(u.get('support_officers', []))}")

        st.divider()
        # Initialize audit log for admin actions in-session
        if 'audit_log' not in st.session_state:
            st.session_state.audit_log = []

        st.subheader("🗑️ Remove Caseload Assignment")
        if st.session_state.units:
            remove_unit = st.selectbox("Select Unit to modify", options=list(st.session_state.units.keys()), key="remove_unit_select")
            if remove_unit:
                assignments = st.session_state.units.get(remove_unit, {}).get('assignments', {})
                person_options = list(assignments.keys())
                if person_options:
                    remove_person = st.selectbox("Select Assignee", options=person_options, key="remove_person_select")
                    caseload_options = assignments.get(remove_person, [])
                    if caseload_options:
                        remove_caseload = st.selectbox("Select Caseload to remove", options=caseload_options, key="remove_caseload_select")
                        if st.button("🗑️ Remove Assignment"):
                            # Show a confirmation modal before removing
                            with st.modal("Confirm Removal"):
                                st.warning(f"You are about to remove caseload **{remove_caseload}** from **{remove_person}** in unit **{remove_unit}**.")
                                st.write("This action will delete the assignment from the in-memory configuration. An audit entry will be recorded in the session log.")
                                col_c1, col_c2 = st.columns([1,1])
                                with col_c1:
                                    if st.button("Confirm Remove", key=f"confirm_remove_{remove_unit}_{remove_person}_{remove_caseload}"):
                                        # Perform removal
                                        try:
                                            assignments[remove_person].remove(remove_caseload)
                                        except ValueError:
                                            st.error("Selected caseload not found in assignments; it may have been removed already.")
                                        else:
                                            # Clean up empty lists
                                            if not assignments.get(remove_person):
                                                del assignments[remove_person]
                                            st.session_state.units[remove_unit]['assignments'] = assignments
                                            # Append audit log entry
                                            st.session_state.audit_log.append({
                                                'timestamp': datetime.now().isoformat(),
                                                'actor': st.session_state.get('current_user', 'IT Administrator (UI)'),
                                                'action': 'remove_assignment',
                                                'unit': remove_unit,
                                                'assignee': remove_person,
                                                'caseload': remove_caseload
                                            })
                                            # Also persist audit entry to disk (append JSONL)
                                            try:
                                                data_dir = os.path.join(os.getcwd(), 'data')
                                                os.makedirs(data_dir, exist_ok=True)
                                                audit_file = os.path.join(data_dir, 'audit_log.jsonl')
                                                with open(audit_file, 'a', encoding='utf-8') as af:
                                                    af.write(json.dumps(st.session_state.audit_log[-1]) + "\n")
                                            except Exception as e:
                                                st.warning(f"Could not persist audit entry to disk: {e}")
                                            st.success(f"✓ Removed caseload {remove_caseload} from {remove_person} in unit '{remove_unit}'")
                                with col_c2:
                                    if st.button("Cancel", key=f"cancel_remove_{remove_unit}_{remove_person}_{remove_caseload}"):
                                        st.info("Removal cancelled.")
                    else:
                        st.info("No caseloads assigned to the selected person.")
                else:
                    st.info("No assignments exist for this unit.")
        else:
            st.info("No units available to modify.")
    
    with it_tab3:
        # System Log
        st.subheader("Recent System Activity")
        logs = pd.DataFrame({
            'Timestamp': pd.date_range(end=datetime.now(), periods=5, freq='H'),
            'Event': [
                '[INFO] Backup completed successfully',
                '[INFO] 12 reports processed',
                '[WARNING] High disk usage detected',
                '[INFO] User session initialized',
                '[INFO] Database optimization running'
            ],
            'Status': ['✓', '✓', '⚠️', '✓', '✓']
        })

        # Include any session-level audit log entries created by IT Admin actions
        audit_entries = []
        for a in st.session_state.get('audit_log', []):
            audit_entries.append({
                'Timestamp': pd.to_datetime(a.get('timestamp')),
                'Event': f"[AUDIT] {a.get('actor')}: {a.get('action')} — caseload {a.get('caseload')} -> {a.get('assignee')} (unit: {a.get('unit')})",
                'Status': 'AUDIT'
            })

        if audit_entries:
            audit_df = pd.DataFrame(audit_entries)
            combined = pd.concat([audit_df, logs], ignore_index=True).sort_values(by='Timestamp', ascending=False)
        else:
            combined = logs.sort_values(by='Timestamp', ascending=False)

        st.dataframe(combined, use_container_width=True)
        
        # Maintenance
        st.subheader("Maintenance Tools")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Run System Diagnostics", key="it_diag"):
                st.success("✓ Diagnostics completed: All systems nominal")
        with col2:
            if st.button("Generate Audit Report", key="it_audit"):
                st.success("✓ Audit report generated for current period")
        with col3:
            if st.button("Backup Database", key="it_backup"):
                st.success("✓ Database backup completed successfully")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em;">
    <p>OCSS Establishment Command Center | Version 1.0.0</p>
    <p>Last Updated: """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</p>
</div>
""", unsafe_allow_html=True)