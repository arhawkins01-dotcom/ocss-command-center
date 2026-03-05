# OCSS Command Center - 2-Minute Opening Script (IT + Developers)

Use this script to open the Cuyahoga County IT and developer demo.

## Script

Thank you everyone for joining. Today we are demonstrating the OCSS Command Center as a practical, role-based operations tool for report intake, workflow execution, and performance visibility.

This is a pilot-phase technical demonstration focused on three things:
1. Operational fit for county users.
2. IT readiness for hosting and support.
3. Developer readiness for Phase 2 enhancements.

From an architecture standpoint, this is a Streamlit and Python application with a single entry point at `app/app.py`. It includes role-aware workflows across Program Officer, Supervisor, Support Officer, and IT Administrator views.

Before starting, we validated readiness with a preflight and test pass, and we confirmed service health on the active endpoint. During the demo, we will show ingestion checks, assignment controls, self-pull enforcement, row-level processing, export behavior, and IT-facing operational screens.

Important constraint for transparency: this phase does not yet include full enterprise authentication and full persistence for uploaded report content across restart. We will close with recommended Phase 2 decisions on authentication direction, persistence model, and production hosting approach.

Our goal today is to leave with clear technical decisions, owners, and next actions that move this from pilot operation to production readiness.

## Optional 20-Second Transition to Live Walkthrough

With that context, we will begin in the Program Officer flow to show report ingestion and validation behavior, then move to Supervisor and Support workflows, and finish in IT Administrator for operational controls.
