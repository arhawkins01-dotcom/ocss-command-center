import sqlite3
import pandas as pd
import json
from datetime import datetime

DB_FILE = "ocss.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id TEXT UNIQUE,
            caseload_id TEXT,
            type TEXT,
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            active_worker TEXT,
            submitted_date TIMESTAMP,
            reviewed_by TEXT,
            reviewed_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS case_rows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id TEXT,
            case_number TEXT,
            worker_status TEXT DEFAULT 'Not Started',
            assigned_worker TEXT,
            results_of_review TEXT,
            case_closure_code TEXT,
            case_narrated TEXT,
            comment TEXT,
            notes TEXT,
            details_json TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(report_id) REFERENCES reports(report_id)
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")

def create_report_from_df(report_id, caseload_id, report_type, assigned_worker, df_data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM reports WHERE report_id = ?", (report_id,))
        if cursor.fetchone():
             conn.close()
             return False, "Report ID already exists."

        cursor.execute("""
            INSERT INTO reports (report_id, caseload_id, type, assigned_to, status, created_at)
            VALUES (?, ?, ?, ?, 'Open', CURRENT_TIMESTAMP)
        """, (report_id, caseload_id, report_type, assigned_worker))
        
        rows_to_insert = []
        std_cols = ['Case Number', 'Worker Status', 'Assigned Worker', 'Results of Review', 'Case Closure Code', 'Case Narrated', 'Comment']
        for col in std_cols:
            if col not in df_data.columns:
                df_data[col] = ''
                
        for _, row in df_data.iterrows():
            aw = row.get('Assigned Worker')
            if pd.isna(aw) or str(aw).strip() == '':
                aw = assigned_worker
            else:
                aw = str(aw)
                
            record = (
                report_id,
                str(row.get('Case Number', '')),
                str(row.get('Worker Status', 'Not Started')),
                aw,
                str(row.get('Results of Review', '')),
                str(row.get('Case Closure Code', '')),
                str(row.get('Case Narrated', '')),
                str(row.get('Comment', '')),
                '', 
                json.dumps({k: str(v) for k, v in row.items() if k not in std_cols and pd.notna(v)})
            )
            rows_to_insert.append(record)

        cursor.executemany("""
            INSERT INTO case_rows (
                report_id, case_number, worker_status, assigned_worker,
                results_of_review, case_closure_code, case_narrated, comment,
                notes, details_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows_to_insert)
        conn.commit()
        return True, "Report created successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_report_full_df(report_id):
    conn = get_connection()
    meta = pd.read_sql_query("SELECT * FROM reports WHERE report_id = ?", conn, params=(report_id,))
    if meta.empty:
        conn.close()
        return None
    rows_df = pd.read_sql_query("SELECT * FROM case_rows WHERE report_id = ?", conn, params=(report_id,))
    conn.close()
    if rows_df.empty:
        return pd.DataFrame()
    expanded_data = []
    for _, row in rows_df.iterrows():
        item = {
            'Case Row ID': row['id'], 
            'Case Number': row['case_number'],
            'Worker Status': row['worker_status'],
            'Assigned Worker': row['assigned_worker'],
            'Results of Review': row['results_of_review'],
            'Case Closure Code': row['case_closure_code'],
            'Case Narrated': row['case_narrated'],
            'Comment': row['comment'],
            'Case Notes': row['notes'] 
        }
        if row['details_json']:
            try:
                item.update(json.loads(row['details_json']))
            except:
                pass
        expanded_data.append(item)
    return pd.DataFrame(expanded_data)

def update_case_row(row_id, updates):
    column_mapping = {
        'Worker Status': 'worker_status',
        'Results of Review': 'results_of_review',
        'Case Closure Code': 'case_closure_code',
        'Case Narrated': 'case_narrated',
        'Comment': 'comment',
        'Case Notes': 'notes',
        'Assigned Worker': 'assigned_worker'
    }
    conn = get_connection()
    cursor = conn.cursor()
    set_clauses = []
    params = []
    for ui_col, new_val in updates.items():
        if ui_col in column_mapping:
            db_col = column_mapping[ui_col]
            set_clauses.append(f"{db_col} = ?")
            params.append(new_val)
    if set_clauses:
        set_clauses.append("last_updated = CURRENT_TIMESTAMP")
        sql = f"UPDATE case_rows SET {', '.join(set_clauses)} WHERE id = ?"
        params.append(row_id)
        cursor.execute(sql, params)
        conn.commit()
    conn.close()

def update_report_status(report_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET status = ?, last_updated = CURRENT_TIMESTAMP WHERE report_id = ?", (new_status, report_id))
    conn.commit()
    conn.close()

def get_pending_reports_for_supervisor(supervisor_caseloads):
    conn = get_connection()
    if not supervisor_caseloads:
        conn.close()
        return pd.DataFrame()
    placeholders = ','.join(['?'] * len(supervisor_caseloads))
    query = f"SELECT * FROM reports WHERE status = 'Submitted for Review' AND caseload_id IN ({placeholders})"
    df = pd.read_sql_query(query, conn, params=list(supervisor_caseloads))
    conn.close()
    return df

def load_reports_into_state():
    """
    Load all reports from DB into the application's session state structure:
    { caseload_id: [ { 'report_id': ..., 'caseload': ..., 'data': df, 'status': ..., ... }, ... ] }
    """
    conn = get_connection()
    reports_df = pd.read_sql_query("SELECT * FROM reports", conn)
    state_structure = {}
    for _, report in reports_df.iterrows():
        caseload = report['caseload_id']
        report_id = report['report_id']
        data_df = get_report_full_df(report_id)
        report_entry = {
            'report_id': report_id,
            'caseload': caseload,
            'status': report['status'],
            'type': report['type'],
            'assigned_worker': report['assigned_to'], 
            'data': data_df,
            'created_at': report['created_at']
        }
        if caseload not in state_structure:
            state_structure[caseload] = []
        state_structure[caseload].append(report_entry)
    conn.close()
    return state_structure

def sync_report_to_db(report_entry):
    """
    Save the current state of a report entry (DataFrame properties) back to DB.
    Reflects changes like 'Worker Status', 'Case Notes', etc.
    """
    report_id = report_entry['report_id']
    df = report_entry['data']
    status = report_entry.get('status', 'Open')
    update_report_status(report_id, status)
    conn = get_connection()
    cursor = conn.cursor()
    col_map = {
        'Worker Status': 'worker_status',
        'Results of Review': 'results_of_review',
        'Case Closure Code': 'case_closure_code',
        'Case Narrated': 'case_narrated',
        'Comment': 'comment',
        'Case Notes': 'notes',
        'Assigned Worker': 'assigned_worker'
    }
    for index, row in df.iterrows():
        row_id = row.get('Case Row ID')
        if not row_id:
             continue
        updates = []
        params = []
        for ui_col, db_col in col_map.items():
            if ui_col in row:
                updates.append(f"{db_col} = ?")
                params.append(str(row[ui_col]))
        if updates:
            updates.append("last_updated = CURRENT_TIMESTAMP")
            sql = f"UPDATE case_rows SET {{', '.join(updates)}} WHERE id = ?"
            params.append(row_id)
            cursor.execute(sql, params)
    conn.commit()
    conn.close()
