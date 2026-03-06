import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import os
import json

# Alert System
try:
    from app.alert_system import AlertLevel, create_alert, get_alert_manager
    from app.alert_ui import render_alert_badge, render_active_alerts, render_alert_dashboard
    ALERT_SYSTEM_AVAILABLE = True
except ImportError:
    ALERT_SYSTEM_AVAILABLE = False

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
# Initialize Alert Manager if available
if ALERT_SYSTEM_AVAILABLE:
    alert_manager = get_alert_manager()

# Sidebar - Role Selection
st.sidebar.title("🎯 OCSS Command Center")
st.sidebar.success("✅ **System Status: OPEN** - Ready for Operations")

# Alert Badge in Sidebar
if ALERT_SYSTEM_AVAILABLE:
    st.sidebar.markdown("####")
    render_alert_badge(position="sidebar")

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
            if ALERT_SYSTEM_AVAILABLE:
                create_alert(
                    title="Reports Reassigned",
                    message=f"{num_reports} report(s) reassigned from {from_worker} to {to_worker}",
                    level=AlertLevel.INFO,
                    category="assignment",
                    metadata={'from': from_worker, 'to': to_worker, 'count': num_reports},
                    persistent=True
                )
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
                if ALERT_SYSTEM_AVAILABLE:
                    create_alert(
                        title="File Uploaded",
                        message=f"File '{uploaded_file.name}' uploaded successfully",
                        level=AlertLevel.INFO,
                        category="file_operations",
                        metadata={'filename': uploaded_file.name, 'size': f"{uploaded_file.size / 1024:.1f} KB"}
                    )
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Read Excel file
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    if ALERT_SYSTEM_AVAILABLE:
                        create_alert(
                            title="File Parsed",
                            message=f"File contains {len(df)} rows and {len(df.columns)} columns",
                            level=AlertLevel.INFO,
                            category="file_operations",
                            metadata={'rows': len(df), 'columns': len(df.columns)}
                        )
                    st.info(f"📊 File has {len(df)} rows and {len(df.columns)} columns")
                except Exception as e:
                    if ALERT_SYSTEM_AVAILABLE:
                        create_alert(
                            title="File Processing Error",
                            message=f"Unable to read file: {str(e)}",
                            level=AlertLevel.ERROR,
                            category="file_operations",
                            persistent=True,
                            metadata={'error': str(e), 'filename': uploaded_file.name}
                        )
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
                    
                    if ALERT_SYSTEM_AVAILABLE:
                        create_alert(
                            title="Report Processed",
                            message=f"Report {report_entry['report_id']} processed and assigned to Support Officer",
                            level=AlertLevel.INFO,
                            category="processing",
                            metadata={'report_id': report_entry['report_id'], 'caseload': selected_caseload},
                            persistent=True
                        )
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
                            if ALERT_SYSTEM_AVAILABLE:
                                create_alert(
                                    title="Caseload Moved",
                                    message=f"Caseload {caseload_choice} moved from {from_worker} to {to_worker} in unit {unit_name}",
                                    level=AlertLevel.INFO,
                                    category="assignment",
                                    metadata={'caseload': caseload_choice, 'from': from_worker, 'to': to_worker, 'unit': unit_name},
                                    persistent=True
                                )
                            st.success(f"✓ Caseload {caseload_choice} moved from {from_worker} to {to_worker}")
                        else:
                            if ALERT_SYSTEM_AVAILABLE:
                                create_alert(
                                    title="Caseload Not Found",
                                    message=f"Caseload {caseload_choice} not assigned to {from_worker}",
                                    level=AlertLevel.ERROR,
                                    category="assignment"
                                )
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
                                if ALERT_SYSTEM_AVAILABLE:
                                    create_alert(
                                        title="Caseload Claimed",
                                        message=f"Caseload {pull_caseload} claimed by {pull_worker} in unit '{unit_name}'",
                                        level=AlertLevel.INFO,
                                        category="assignment",
                                        metadata={'caseload': pull_caseload, 'worker': pull_worker, 'unit': unit_name},
                                        persistent=True
                                    )
                                st.success(f"✓ Caseload {pull_caseload} claimed by {pull_worker} in unit '{unit_name}'"
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

    # Tab Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Caseload Dashboard", "📝 My Assigned Reports", "🆘 Support Tickets", "📚 Knowledge Base"])
    
    # TAB 1: Caseload Report Dashboard
    with tab1:
        st.subheader("📊 Process Reports by Caseload")
        
        # Caseload data with Excel information
        caseload_data = {
            '181000': {
                'name': 'Downtown Elementary',
                'reports': [
                    {'id': 'ENV-181000-001', 'date': '2026-02-18', 'filename': 'ENV_Report_Q1_2026.xlsx', 
                     'data': {'Total Students': 245, 'Staff': 15, 'Classrooms': 12, 'Completion %': 85, 'Grade Levels': '3-5', 'Assessment Date': '2/15/2026', 'Quality Score': 94}},
                    {'id': 'ENV-181000-002', 'date': '2026-02-15', 'filename': 'Safety_Audit_Feb.xlsx',
                     'data': {'Safety Issues': 3, 'Resolved': 2, 'Pending': 1, 'Status': 'In Review', 'Inspector': 'John Smith', 'Review Date': '2/14/2026', 'Next Audit': '3/14/2026'}}
                ]
            },
            '181001': {
                'name': 'Midtown Middle School',
                'reports': [
                    {'id': 'ENV-181001-001', 'date': '2026-02-17', 'filename': 'ENV_Report_Q1_2026.xlsx',
                     'data': {'Total Students': 520, 'Staff': 35, 'Classrooms': 28, 'Completion %': 92, 'Grade Levels': '6-8', 'Assessment Date': '2/16/2026', 'Quality Score': 96}},
                    {'id': 'ENV-181001-002', 'date': '2026-02-12', 'filename': 'Compliance_Check.xlsx',
                     'data': {'Standards Met': 47, 'Outstanding': 2, 'Non-Compliant': 1, 'Score': '94%', 'Reviewer': 'Sarah Johnson', 'Review Date': '2/11/2026', 'Action Items': 2}}
                ]
            },
            '181002': {
                'name': 'Uptown High School',
                'reports': [
                    {'id': 'ENV-181002-001', 'date': '2026-02-19', 'filename': 'ENV_Report_Q1_2026.xlsx',
                     'data': {'Total Students': 1200, 'Staff': 85, 'Classrooms': 62, 'Completion %': 78, 'Grade Levels': '9-12', 'Assessment Date': '2/17/2026', 'Quality Score': 90}},
                ]
            }
        }
        
        # Caseload selection
        col1, col2 = st.columns([1, 2])
        with col1:
            # If acting as a Support Officer, limit caseloads to assigned ones
            if 'acting_so' in locals() and acting_so and acting_so != '(Select)':
                options = []
                for unit in st.session_state.units.values():
                    for person, caseloads in unit.get('assignments', {}).items():
                        if person == acting_so:
                            options.extend(caseloads)
                # fallback to all if none assigned
                if not options:
                    options = list(caseload_data.keys())
            else:
                options = list(caseload_data.keys())

            selected_caseload = st.selectbox(
                "Select Caseload Number",
                options,
                format_func=lambda x: f"{x} - {caseload_data[x]['name']}"
            )
        with col2:
            st.info(f"**Caseload {selected_caseload}**: {caseload_data[selected_caseload]['name']}")
        
        st.divider()
        
        # Display reports for selected caseload
        if selected_caseload in caseload_data:
            caseload_info = caseload_data[selected_caseload]
            st.subheader(f"📋 Reports for {caseload_info['name']}")
            st.caption("These reports were uploaded by Program Officer. View details below.")
            
            # FIRST: Show uploaded reports from Program Officer session (LIVE DATA)
            uploaded_reports_list = st.session_state.reports_by_caseload.get(selected_caseload, [])
            
            if uploaded_reports_list:
                st.write("**📤 Recently Uploaded Reports (Live Data):**")
                for report_idx, report in enumerate(uploaded_reports_list):
                    with st.expander(f"📄 {report['report_id']} - {report['filename']} ({report['timestamp'].strftime('%m/%d %H:%M')})", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Report ID", report['report_id'])
                        with col2:
                            st.metric("Status", report['status'])
                        with col3:
                            st.metric("Uploaded by", report['uploaded_by'])
                        
                        if not report['data'].empty:
                            st.divider()
                            st.subheader("📊 Data Preview")
                            st.dataframe(report['data'], use_container_width=True)
                            
                            # Export options
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                csv_export = report['data'].to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV",
                                    data=csv_export,
                                    file_name=f"{report['report_id']}.csv",
                                    mime="text/csv",
                                    key=f"download_uploaded_{report['report_id']}"
                                )
                            with col2:
                                if st.button("✅ Approve", key=f"approve_upload_{report['report_id']}"):
                                    st.success(f"✓ {report['report_id']} approved!")
                            with col3:
                                if st.button("📤 Submit", key=f"submit_upload_{report['report_id']}"):
                                    st.success(f"✓ {report['report_id']} submitted for processing!")
                
                st.divider()
            
            # THEN: Show sample/demo reports (for reference)
            st.write("**📑 Sample Reports (Demo Data):**")
            
            for report_idx, report in enumerate(caseload_info['reports']):
                with st.expander(f"📄 {report['id']} - {report['filename']} ({report['date']})", expanded=False):
                    # Report metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Report ID", report['id'])
                    with col2:
                        st.metric("Date", report['date'])
                    with col3:
                        st.metric("Status", "Ready")
                    
                    st.divider()
                    
                    # Editable fields section
                    st.subheader("📝 Report Data - Editable Fields")
                    
                    # Initialize session state for edits if not exists
                    edit_key = f"report_edits_{report['id']}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = report['data'].copy()
                    
                    # Create form for editable fields
                    with st.form(key=f"form_{report['id']}"):
                        edited_data = {}
                        
                        # Display fields in columns for better layout
                        for field_idx, (key, value) in enumerate(report['data'].items()):
                            # Determine input type based on value
                            if isinstance(value, int) and '%' not in str(key):
                                # Number input for numeric values
                                edited_data[key] = st.number_input(
                                    label=f"{key}",
                                    value=int(st.session_state[edit_key].get(key, value)),
                                    key=f"input_{report['id']}_{field_idx}"
                                )
                            elif isinstance(value, float):
                                edited_data[key] = st.number_input(
                                    label=f"{key}",
                                    value=float(st.session_state[edit_key].get(key, value)),
                                    format="%.2f",
                                    key=f"input_{report['id']}_{field_idx}"
                                )
                            else:
                                # Text input for string values
                                edited_data[key] = st.text_input(
                                    label=f"{key}",
                                    value=str(st.session_state[edit_key].get(key, value)),
                                    key=f"input_{report['id']}_{field_idx}"
                                )
                        
                        st.divider()
                        
                        # Form submission
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            submitted = st.form_submit_button("💾 Update Report", use_container_width=True)
                            if submitted:
                                st.session_state[edit_key] = edited_data
                                st.success("✓ Report data updated!")
                    
                    st.divider()
                    
                    # Display current data summary
                    st.subheader("📊 Current Values")
                    summary_df = pd.DataFrame(list(st.session_state[edit_key].items()), columns=['Field', 'Value'])
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)
                    
                    st.divider()
                    
                    # Action and Export buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        # Generate CSV from report data
                        report_csv = pd.DataFrame(list(st.session_state[edit_key].items()), columns=['Field', 'Value']).to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=report_csv,
                            file_name=f"{report['id']}.csv",
                            mime="text/csv",
                            key=f"download_csv_report_{report['id']}"
                        )
                    with col2:
                        if st.button("✅ Approve", key=f"approve_report_{selected_caseload}_{report_idx}", use_container_width=True):
                            st.success(f"✓ {report['id']} approved!")
                    with col3:
                        if st.button("💾 Save", key=f"save_report_{selected_caseload}_{report_idx}", use_container_width=True):
                            st.success(f"✓ {report['id']} saved!")
                    with col4:
                        if st.button("📤 Submit", key=f"submit_report_{selected_caseload}_{report_idx}", use_container_width=True):
                            st.success(f"✓ {report['id']} submitted for review!")
        
        st.divider()
        
        # Summary statistics
        st.subheader("📊 Caseload Summary")
        total_reports = sum(len(caseload['reports']) for caseload in caseload_data.values())
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Caseloads", len(caseload_data))
        with col2:
            st.metric("Total Reports Available", total_reports)
        with col3:
            st.metric("Reports in Progress", 3)
        with col4:
            st.metric("Status", "Ready")
    
    # TAB 2: Assigned Reports by Caseload
    with tab2:
        st.subheader("My Caseload - Assigned Reports")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Status", ["Not Started", "In Progress", "Under Review", "Completed"], 
                                          default=["Not Started", "In Progress"])
        with col2:
            priority_filter = st.multiselect("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"],
                                            default=["🔴 High", "🟡 Medium"])
        with col3:
            sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Establishment", "Date Added"])
        
        # Assigned Reports Table
        assigned_reports = pd.DataFrame({
            'Report ID': ['REP-2026-0045', 'REP-2026-0046', 'REP-2026-0047', 'REP-2026-0048', 'REP-2026-0049', 'REP-2026-0050'],
            'Establishment': ['Lincoln Elementary', 'Grant Middle School', 'Jefferson HS', 'Adams Preschool', 'Madison Elementary', 'Monroe Academy'],
            'Status': ['Not Started', 'In Progress', 'Under Review', 'Not Started', 'In Progress', 'Completed'],
            'Priority': ['🔴 High', '🟡 Medium', '🔴 High', '🟢 Low', '🟡 Medium', '✓ Completed'],
            'Due Date': ['Feb 20', 'Feb 19', 'Feb 22', 'Feb 25', 'Feb 21', 'Feb 18'],
            'Progress': [0, 65, 85, 0, 40, 100],
            'Assigned': ['Feb 10', 'Feb 12', 'Feb 11', 'Feb 14', 'Feb 13', 'Feb 15']
        })
        
        # Initialize session state for report editing
        if 'selected_report' not in st.session_state:
            st.session_state.selected_report = None
        if 'report_updates' not in st.session_state:
            st.session_state.report_updates = {}
        
        # Display reports with expandable details
        for idx, row in assigned_reports.iterrows():
            with st.expander(f"📋 {row['Establishment']} ({row['Report ID']}) - {row['Status']} - Due: {row['Due Date']}", 
                            expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.progress(row['Progress'] / 100)
                    st.caption(f"Progress: {row['Progress']}%")
                with col2:
                    st.metric("Priority", row['Priority'])
                with col3:
                    st.metric("Assigned", row['Assigned'])
                
                st.divider()
                
                # Report Processing Form Inside Expander
                st.markdown(f"### Processing {row['Establishment']}")
                
                status_update = st.selectbox(
                    "Update Status",
                    ["Not Started", "In Progress", "Under Review", "Completed"],
                    index=["Not Started", "In Progress", "Under Review", "Completed"].index(row['Status']),
                    key=f"status_update_{idx}"
                )
                
                # Report Review Form
                col1, col2 = st.columns(2)
                with col1:
                    establishment_name = st.text_input("Establishment Name", value=row['Establishment'], key=f"est_name_{idx}")
                    report_type = st.selectbox("Report Type", ["Annual", "Quarterly", "Monthly"], key=f"type_{idx}")
                    report_name = st.text_input("Report Name", value=f"{row['Establishment']} - {row['Report ID']}", key=f"report_name_{idx}", help="Edit the report name/title")
                with col2:
                    submitted_by = st.text_input("Submitted By", placeholder="Officer Name", key=f"submitted_{idx}")
                    submission_date = st.date_input("Submission Date", key=f"subdate_{idx}")
                    reference_number = st.text_input("Reference/ID", value=row['Report ID'], key=f"ref_num_{idx}")
                
                # Data validation
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.checkbox("✓ Required Fields", value=True, key=f"req_fields_{idx}")
                with col2:
                    st.checkbox("✓ Format Valid", value=True, key=f"format_{idx}")
                with col3:
                    st.checkbox("✓ No Duplicates", value=True, key=f"dup_{idx}")
                with col4:
                    st.checkbox("✓ CQI Aligned", value=True, key=f"cqi_{idx}")
                
                # Notes and comments
                notes = st.text_area(
                    "Processing Notes",
                    placeholder="Record any issues, observations, or special notes...",
                    height=80,
                    key=f"notes_{idx}"
                )
                
                # Action buttons
                st.divider()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("💾 Save Progress", key=f"save_{idx}", use_container_width=True):
                        st.success(f"✓ Report '{report_name}' progress saved!")
                        st.session_state.report_updates[row['Report ID']] = {
                            'status': status_update,
                            'establishment': establishment_name,
                            'report_name': report_name,
                            'reference_number': reference_number,
                            'submitted_by': submitted_by,
                            'notes': notes,
                            'updated_at': datetime.now()
                        }
                with col2:
                    if st.button("✅ Mark Complete", key=f"complete_{idx}", use_container_width=True):
                        st.success(f"✓ {row['Establishment']} marked complete!")
                        st.balloons()
                with col3:
                    if st.button("📧 Send for Review", key=f"review_{idx}", use_container_width=True):
                        st.info(f"✓ Report sent to supervisor for review")
                with col4:
                    if st.button("❌ Close", key=f"close_{idx}", use_container_width=True):
                        st.rerun()
        
        # Bulk Actions
        st.divider()
        st.subheader("Bulk Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✓ Mark Selected as Complete"):
                st.success("Selected reports marked as complete")
        with col2:
            if st.button("🔄 Reassign Reports"):
                st.info("Opened reassignment dialog")
        with col3:
            if st.button("📊 Export Caseload Report"):
                st.success("Caseload report downloaded")
    
    # TAB 2: Support Tickets
    with tab2:
        # Support Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Open Tickets", "8", "-2")
        with col2:
            st.metric("Avg Response Time", "1.2 hrs", "-0.3 hrs")
        with col3:
            st.metric("Resolution Rate", "94%", "+3%")
        with col4:
            st.metric("User Satisfaction", "4.7/5.0", "+0.2")
        
        # Support Tickets
        st.subheader("Active Support Tickets")
        tickets = pd.DataFrame({
            'Ticket ID': ['SUP-2026-001', 'SUP-2026-002', 'SUP-2026-003', 'SUP-2026-004'],
            'Establishment': ['Lincoln Elementary', 'Grant Middle School', 'Jefferson HS', 'Adams Preschool'],
            'Issue': [
                'Excel upload format error',
                'Login credentials not working',
                'Report submission timeout',
                'Data validation failure'
            ],
            'Priority': ['🔴 High', '🟡 Medium', '🔴 High', '🟡 Medium'],
            'Status': ['In Progress', 'Assigned', 'Waiting', 'In Progress']
        })
        st.dataframe(tickets, use_container_width=True)
        
        # Create new support ticket
        st.subheader("Open New Support Ticket")
        col1, col2 = st.columns(2)
        with col1:
            establishment = st.selectbox("Select Establishment", 
                ['Lincoln Elementary', 'Grant Middle School', 'Jefferson HS', 'Adams Preschool', 'Madison Elementary'],
                key="support_ticket_establishment")
            priority = st.radio("Priority Level", ["🟢 Low", "🟡 Medium", "🔴 High"], key="support_priority")
        with col2:
            issue_type = st.selectbox("Issue Category",
                ["File Upload", "Authentication", "Data Validation", "Performance", "Technical", "Other"],
                key="support_issue_type")
            description = st.text_area("Issue Description", placeholder="Describe the problem...", key="support_description")
        
        if st.button("📝 Create Ticket", key="create_support_ticket"):
            st.success(f"✓ Ticket created for {establishment} - {priority}")
    
    # TAB 3: FAQ & Knowledge Base
    with tab3:
        st.subheader("📚 Knowledge Base & Troubleshooting")
        with st.expander("❓ How do I upload a report?"):
            st.write("""
            1. Log in with your credentials
            2. Navigate to the 'Report Intake Portal'
            3. Click 'Choose an Excel file'
            4. Select your establishment's report file
            5. Click 'Process Report'
            
            **Accepted formats**: .xls, .xlsx, .csv
            """)
        
        with st.expander("❓ What should I do if my upload fails?"):
            st.write("""
            - Check file format (Excel or CSV only)
            - Verify all required columns are present
            - Remove any special characters from headers
            - Check file size (max 10MB)
            - If issue persists, open a support ticket
            """)
        
        with st.expander("❓ How do I reset my password?"):
            st.write("""
            Click 'Forgot Password' on the login screen and follow the email instructions.
            If you don't receive an email within 5 minutes, contact IT Support.
            """)
        
        with st.expander("❓ What are the system requirements?"):
            st.write("""
            - **Browser**: Chrome, Firefox, Safari, Edge (latest version)
            - **Internet**: Minimum 2 Mbps connection
            - **File format**: Excel 2010 or later (.xlsx)
            - **Computer**: Any Windows, Mac, or Linux system
            """)
        
        # Training Resources
        st.subheader("📖 Training & Resources")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Quick Start Guide**\nGet up and running in 5 minutes")
        with col2:
            st.info("**Video Tutorials**\nStep-by-step walkthroughs")
        with col3:
            st.info("**Live Chat**\nConnect with a support specialist")
        
        # Common Issues
        st.subheader("🔧 Common Issues & Solutions")
        common_issues = pd.DataFrame({
            'Issue': [
                'Cannot login',
                'File format rejected',
                'Slow performance',
                'Export not working',
                'Data not saving'
            ],
            'Possible Cause': [
                'Wrong credentials or account inactive',
                'Wrong file format or corrupted file',
                'Network latency or browser cache',
                'File permissions or server issue',
                'Internet disconnected or session timeout'
            ],
            'Quick Fix': [
                'Reset password or contact IT',
                'Use Excel (.xlsx) format',
                'Clear browser cache',
                'Try different browser',
                'Refresh page and retry'
            ]
        })
        st.dataframe(common_issues, use_container_width=True)
    
    # Support Tickets (removed duplicate - now in tab2)
    st.subheader("Active Support Tickets")
    tickets = pd.DataFrame({
        'Ticket ID': ['SUP-2026-001', 'SUP-2026-002', 'SUP-2026-003', 'SUP-2026-004'],
        'Establishment': ['Lincoln Elementary', 'Grant Middle School', 'Jefferson HS', 'Adams Preschool'],
        'Issue': [
            'Excel upload format error',
            'Login credentials not working',
            'Report submission timeout',
            'Data validation failure'
        ],
        'Priority': ['🔴 High', '🟡 Medium', '🔴 High', '🟡 Medium'],
        'Status': ['In Progress', 'Assigned', 'Waiting', 'In Progress']
    })
    st.dataframe(tickets, use_container_width=True)
    
    # Create new support ticket
    st.subheader("Open New Support Ticket")
    col1, col2 = st.columns(2)
    with col1:
        establishment = st.selectbox("Select Establishment", 
            ['Lincoln Elementary', 'Grant Middle School', 'Jefferson HS', 'Adams Preschool', 'Madison Elementary'])
        priority = st.radio("Priority Level", ["🟢 Low", "🟡 Medium", "🔴 High"])
    with col2:
        issue_type = st.selectbox("Issue Category",
            ["File Upload", "Authentication", "Data Validation", "Performance", "Technical", "Other"])
        description = st.text_area("Issue Description", placeholder="Describe the problem...")
    
        if st.button("📝 Create Ticket", key="new_support_ticket"):
            if ALERT_SYSTEM_AVAILABLE:
                create_alert(
                    title="Support Ticket Created",
                    message=f"Ticket created for {establishment} with {priority} priority",
                    level=AlertLevel.INFO,
                    category="support",
                    metadata={'establishment': establishment, 'priority': priority, 'issue_type': issue_type}
                )
            st.success(f"✓ Ticket created for {establishment} - {priority}")
    
    # Training Resources
    st.subheader("📖 Training & Resources")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Quick Start Guide**\nGet up and running in 5 minutes")
    with col2:
        st.info("**Video Tutorials**\nStep-by-step walkthroughs")
    with col3:
        st.info("**Live Chat**\nConnect with a support specialist")
    
    # Common Issues
    st.subheader("🔧 Common Issues & Solutions")
    common_issues = pd.DataFrame({
        'Issue': [
            'Cannot login',
            'File format rejected',
            'Slow performance',
            'Export not working',
            'Data not saving'
        ],
        'Possible Cause': [
            'Wrong credentials or account inactive',
            'Wrong file format or corrupted file',
            'Network latency or browser cache',
            'File permissions or server issue',
            'Internet disconnected or session timeout'
        ],
        'Quick Fix': [
            'Reset password or contact IT',
            'Use Excel (.xlsx) format',
            'Clear browser cache',
            'Try different browser',
            'Refresh page and retry'
        ]
    })
    st.dataframe(common_issues, use_container_width=True)

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
        
        # Alert Dashboard (if system available)
        if ALERT_SYSTEM_AVAILABLE:
            st.divider()
            st.subheader("📢 System Alerts & Events")
            render_alert_dashboard(alert_manager)
    
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
            if ALERT_SYSTEM_AVAILABLE:
                create_alert(
                    title="User Added",
                    message=f"User '{new_user}' added as {new_role} in {new_dept}",
                    level=AlertLevel.INFO,
                    category="user_management",
                    metadata={'user': new_user, 'role': new_role, 'department': new_dept}
                )
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