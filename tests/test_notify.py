import os
from pathlib import Path
import pytest
from app import notify


def test_send_notification_saves_to_exports(tmp_path, monkeypatch):
    # Ensure exports dir is created inside tmp_path
    monkeypatch.chdir(tmp_path)
    report_id = 'TEST-1'
    csv_bytes = b'col1,col2\n1,2\n'

    res = notify.send_notification_report_csv(report_id, csv_bytes, recipient=None)
    assert isinstance(res, dict)
    assert res.get('sent') is False
    saved = res.get('saved_to')
    assert saved
    assert Path(saved).exists()
    assert Path(saved).read_bytes() == csv_bytes