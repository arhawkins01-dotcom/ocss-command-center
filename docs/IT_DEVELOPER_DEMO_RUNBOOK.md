# OCSS Command Center - IT and Developer Demo Runbook

Version: 1.0.0  
Last Updated: 2026-03-05

## Audience
- Cuyahoga County IT operations and security reviewers
- County developers and technical stakeholders

## Demo Goals
- Validate the application can be started and reached reliably on a shared demo host.
- Demonstrate current architecture, workflow behavior, and known constraints.
- Capture implementation decisions and Phase 2 engineering priorities.

## 1) Pre-Demo Checklist (15-20 minutes before)

Run from repository root:

```bash
./scripts/demo_preflight.sh
```

Expected outcome:
- Focused test suite passes
- Streamlit availability is verified
- Active app endpoint is detected, or startup command is provided

If no app is running yet:

```bash
./scripts/start_app.sh
```

Then confirm health:

```bash
curl -sS http://localhost:8501/_stcore/health
# or the port shown by start_app.sh, often 8502 when 8501 is in use
```

## 2) Suggested 30-Minute Agenda

1. System context and architecture (5 min)
2. Live workflow walkthrough by role (12 min)
3. IT controls, deployment, and operations review (8 min)
4. Developer deep dive and Q and A (5 min)

## 3) Architecture Talking Points (IT + Dev)

- Framework: Streamlit + Python (single web app process).
- Entry point: `app/app.py`.
- State model:
  - Best-effort persisted state in `data/state/ocss_app_state.json`.
  - Session-only data for uploaded report content and in-progress row edits.
- Role/view logic and capabilities:
  - `app/roles.py`
  - `app/action_logic.py`
- Report ingestion and validation:
  - `app/report_utils.py`
- Auth mode control:
  - `app/auth.py` (`OCSS_AUTH_MODE`)

## 4) Live Demo Flow (Technical)

### A. Startup and Health Verification

1. Launch app with `./scripts/start_app.sh`.
2. Note selected port in terminal output.
3. Verify `_stcore/health` endpoint returns `ok`.
4. Open app in browser on the same port.

### B. Functional Walkthrough

1. Program Officer: upload and processing path
2. Supervisor: assignment and self-pull enforcement
3. Support Officer: row-level processing and export
4. IT Administrator: system status and management views

### C. Reliability and Guardrails

1. Duplicate-period and hash checks during ingestion
2. Clear validation errors for invalid actions
3. CSV export behavior for handoff and recovery workflows

## 5) Commands for IT Review

```bash
# focused tests used for demo readiness
/usr/local/bin/python -m pytest -q app/tests/test_roles.py app/tests/test_capabilities.py tests/test_notify.py

# optional broader pass
/usr/local/bin/python -m pytest -q

# task-based app launch (if using VS Code task)
# Task label: Run OCSS App
```

## 6) Known Constraints to Call Out Clearly

- No full enterprise authentication/authorization stack in this phase.
- Uploaded report content is not persisted across restart in current model.
- Single-instance Streamlit deployment is suitable for pilot-level concurrency.

## 7) Evidence to Capture During Demo

- Health check output (`ok`)
- Test pass output summary
- App URL and port used
- Open risks and requested follow-up actions from IT and developers

## 8) Post-Demo Handoff

- Share references:
  - `docs/TECHNICAL_GUIDE.md`
  - `docs/IT_IMPLEMENTATION_GUIDE.md`
  - `docs/SECURITY_AND_DEPLOYMENT_BRIEF.md`
- Create a short decision log entry for:
  - Hosting target and support model
  - Authentication direction
  - Persistence/database phase timeline
