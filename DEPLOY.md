# Deploying OCSS Command Center to Streamlit Cloud

This repository is prepared for Streamlit Cloud deployment. The branch `copilot/build-streamlit-application`
contains the Streamlit entrypoint `streamlit_app.py` and a root `requirements.txt` suitable for Cloud.

Quick manual deploy (Streamlit Cloud)

1. Open https://share.streamlit.io and sign in with your GitHub account.
2. Click **New app** → select the repository `arhawkins01-dotcom/ocss-command-center`.
3. Choose branch: `copilot/build-streamlit-application`.
4. Set the main file to `streamlit_app.py` and click **Deploy**.

Notes and recommended settings

- Python & packages: Cloud will install packages from `requirements.txt`.
- If your app uses any external secrets (API keys, DB credentials), add them under the app **Settings → Secrets** in Streamlit Cloud.
- To enable automatic redeploys on push, ensure **Auto-deploy** (or equivalent) is enabled in the Streamlit app settings.

Troubleshooting

- If the app shows "ModuleNotFoundError" on deploy, ensure `app` is a package (this repo includes `app/__init__.py`) and `streamlit_app.py` imports the top-level `app` module.
- Check the Streamlit Cloud logs via **Manage app → Logs** for the redacted error and full traceback.

Automating deployment from CI (optional)

Streamlit Cloud does not provide a public write-api for triggering deploys in all accounts. The easiest automation is:

1. Push changes to the repo/branch that the Streamlit app is configured to use.
2. Configure Streamlit Cloud to auto-deploy on push (app settings).

If you prefer a GitHub Action that runs tests/build checks and then notifies you to redeploy, I can add a workflow that:

- Runs `pytest` / lint on push or PR
- Posts a GitHub status or comment indicating readiness to deploy

If you want fully automated remote redeploys (triggered from CI), I can prepare a workflow, but you'll need to provide any required service token and confirm Streamlit Cloud supports API-triggered deploys for your account.

Next steps I can take for you

- Add a `DEPLOY.md` (done).
- Add a `ci.yml` GitHub Actions workflow to run tests on push/PR.
- Add a workflow to open a PR or comment when CI passes (so you can manually trigger redeploy).

Tell me which automation option you want (CI only / CI + PR comment / CI + try to trigger deploy with credentials) and I'll add the workflow.
