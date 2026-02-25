import smtplib
import os
from email.message import EmailMessage
from pathlib import Path
from typing import Optional


def _ensure_exports_dir() -> Path:
    base = Path(__file__).resolve().parent.parent
    exports = base / "exports"
    exports.mkdir(parents=True, exist_ok=True)
    return exports


def send_notification_report_csv(report_id: str, csv_bytes: bytes, subject: Optional[str] = None,
                                 recipient: Optional[str] = None, sender: Optional[str] = None) -> dict:
    """Attempt to send a CSV of the report via SMTP. If SMTP is not configured,
    fall back to writing the CSV to `exports/notify_<report_id>.csv` and return
    a dict with `saved_to` set to the path.

    Returns a dict describing the outcome: {'sent': bool, 'error': str, 'saved_to': str}
    """
    # Try to read SMTP config from Streamlit secrets if available (deployed env).
    smtp_config = {}
    try:
        # Local import to avoid a Streamlit dependency at module import time
        import streamlit as _st
        secrets = getattr(_st, 'secrets', {})
        smtp_config = secrets.get('email', {}) if isinstance(secrets, dict) else {}
    except Exception:
        smtp_config = {}

    # Fallback: attempt to read .streamlit/secrets.toml directly (useful for local tests)
    if not smtp_config:
        try:
            try:
                import tomllib as _toml
            except Exception:
                import toml as _toml  # type: ignore
            s_path = Path('.streamlit') / 'secrets.toml'
            if s_path.exists():
                with s_path.open('rb') as fh:
                    data = _toml.load(fh)
                smtp_config = data.get('email', {}) if isinstance(data, dict) else {}
        except Exception:
            smtp_config = smtp_config or {}

    subject = subject or f"OCSS Report Notification: {report_id}"
    recipient = recipient or smtp_config.get('recipient')
    sender = sender or smtp_config.get('sender_email') or f"noreply@{os.uname().nodename}"

    # If SMTP config looks complete, attempt to send
    if smtp_config.get('smtp_server') and smtp_config.get('sender_email') and recipient:
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            msg.set_content(f"Attached is the report export for {report_id}.")
            msg.add_attachment(csv_bytes, maintype='text', subtype='csv', filename=f"{report_id}.csv")

            server = smtplib.SMTP(smtp_config.get('smtp_server'), int(smtp_config.get('smtp_port', 25)))
            if smtp_config.get('starttls'):
                server.starttls()
            if smtp_config.get('username') and smtp_config.get('password'):
                server.login(smtp_config.get('username'), smtp_config.get('password'))
            server.send_message(msg)
            server.quit()
            return {'sent': True, 'error': '', 'saved_to': ''}
        except Exception as exc:
            # Fall through to save-to-disk behavior
            err = str(exc)
    else:
        err = 'SMTP not configured; saved to disk.'

    # Save to exports folder as fallback
    exports = _ensure_exports_dir()
    out_path = exports / f"notify_{report_id}.csv"
    try:
        out_path.write_bytes(csv_bytes)
        return {'sent': False, 'error': err, 'saved_to': str(out_path)}
    except Exception as exc:
        return {'sent': False, 'error': str(exc), 'saved_to': ''}
