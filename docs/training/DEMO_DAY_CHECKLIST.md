# OCSS Command Center - Demo Day Checklist

Date: __________  
Audience: Cuyahoga County IT and Developers  
Facilitator: __________

## 1) 30-20 Minutes Before Demo

- [ ] Open terminal in repository root: `/workspaces/ocss-command-center`
- [ ] Run preflight:

```bash
./scripts/demo_preflight.sh
```

- [ ] If app is not running, start app:

```bash
./scripts/start_app.sh
```

- [ ] Confirm health endpoint returns `ok`:

```bash
curl -sS http://localhost:8501/_stcore/health
# if port 8501 is busy, use the port printed by start_app.sh
```

- [ ] Confirm browser access on the active port
- [ ] Confirm sample caseloads and users are visible in UI

## 2) 10 Minutes Before Demo

- [ ] Close unrelated tabs/windows and silence notifications
- [ ] Open these references in advance:
  - `docs/IT_DEVELOPER_DEMO_RUNBOOK.md`
  - `docs/IT_DEVELOPER_2MIN_OPENING_SCRIPT.md`
  - `docs/IT_DEVELOPER_2MIN_CLOSING_SCRIPT.md`
  - `docs/TECHNICAL_GUIDE.md`
  - `docs/IT_IMPLEMENTATION_GUIDE.md`
- [ ] Keep terminal visible for live verification commands
- [ ] Confirm backup presenter can access same URL

## 3) Live Demo Flow (Condensed)

- [ ] Intro: architecture and current phase constraints (use `IT_DEVELOPER_2MIN_OPENING_SCRIPT.md`)
- [ ] Program Officer: upload + ingestion validation behavior
- [ ] Supervisor: assignment + self-pull enforcement
- [ ] Support Officer: row-level processing + export
- [ ] IT Administrator: system views and operational controls
- [ ] Close with decisions and next actions (use `IT_DEVELOPER_2MIN_CLOSING_SCRIPT.md`)

## 4) Real-Time Evidence to Capture

- [ ] Active app URL + port used
- [ ] Health check output (`ok`)
- [ ] Test status statement (full suite pass)
- [ ] Open risks and requested follow-ups

## 5) Post-Demo Actions (Same Day)

- [ ] Share links to technical and deployment docs
- [ ] Log decisions (hosting, auth direction, persistence timeline)
- [ ] Create issue list for Phase 2 items and owners

## 6) Fast Recovery Steps

If UI becomes unresponsive:

```bash
pkill -f "streamlit run" || true
./scripts/start_app.sh
```

If port collision occurs, use the alternate port printed by startup logs.
