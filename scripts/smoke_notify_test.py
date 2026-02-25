#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from app import database
try:
    from app import notify
except Exception:
    import notify


def run():
    report_id = f"SMOKE-{int(pd.Timestamp.now().timestamp())}"
    caseload = '181000'
    df = pd.DataFrame([{'Case Number': 'C-1', 'Worker Status': 'Not Started', 'Assigned Worker': 'Test User'}])

    ok, msg = database.create_report_from_df(report_id, caseload, 'General', 'Test User', df)
    print('create_report:', ok, msg)
    if not ok:
        return 1

    # Approve the report
    database.approve_report(report_id, reviewer='smoke-tester')
    print('approve called')

    # Build CSV bytes and call notify
    rows_df = database.get_report_full_df(report_id)
    csv_b = rows_df.to_csv(index=False).encode('utf-8')
    res = notify.send_notification_report_csv(report_id, csv_b, recipient='ashombia.hawkins@jfs.ohio.gov')
    print('notify result:', res)

    # Verify DB reviewed_by
    conn = database.get_connection()
    cur = conn.cursor()
    cur.execute('SELECT report_id, status, reviewed_by, reviewed_date FROM reports WHERE report_id = ?', (report_id,))
    row = cur.fetchone()
    print('db row:', dict(row) if row else None)

    # cleanup: delete inserted rows
    cur.execute('DELETE FROM case_rows WHERE report_id = ?', (report_id,))
    cur.execute('DELETE FROM reports WHERE report_id = ?', (report_id,))
    conn.commit()
    conn.close()
    print('cleanup done')
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
