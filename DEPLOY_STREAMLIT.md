Streamlit Deployment and Auto-Update Guide
========================================

This guide explains how to deploy the `ocss-command-center` app to Streamlit Community Cloud (share.streamlit.io) and how to enable automatic updates.

1) Quick deploy via Streamlit Cloud (recommended)

-- Push your code to GitHub (`main` branch).
-- Go to https://share.streamlit.io and sign in with GitHub.
-- Click "New app" → select repository `arhawkins01-dotcom/ocss-command-center`, branch `main`, and set the entrypoint to `streamlit_app.py`.
- Streamlit will install dependencies from `requirements.txt` automatically.
- In the app settings enable "Auto deploy" to redeploy on every push to the selected branch.

2) Optional: Redeploy from CI after tests pass

If you prefer automatic redeploys only after CI passes, add a webhook or deploy trigger and store it as a GitHub secret:

- Create a webhook endpoint that triggers your Streamlit deploy (for example, a small service that calls your hosting provider's deploy API). Streamlit Community Cloud does not currently provide a documented public deploy API; using the built-in "Auto deploy" toggle (above) is the simplest option.
- In your repo settings > Secrets, add `STREAMLIT_REDEPLOY_WEBHOOK` with the webhook URL.
- The included GitHub Actions workflow `.github/workflows/python-tests.yml` will POST to that webhook after successful tests when the secret is present.

Setting the webhook secret (recommended)

- Open your repository on GitHub → Settings → Secrets → Actions → `New repository secret`.
- Set the **Name** to `STREAMLIT_REDEPLOY_WEBHOOK` and **Value** to your webhook URL, then save.
- The CI workflow will use this secret when present to POST a redeploy trigger after tests pass.

Manually triggering the workflow from GitHub (no secret change required)

- The CI workflow supports manual runs via GitHub's "Actions" tab using `workflow_dispatch`.
- From the repo page open **Actions → CI — Tests and optional redeploy**, click **Run workflow**, select the `main` branch and optionally paste a `redeploy_webhook` value to test an ad-hoc deploy URL for this run.

Security note: prefer storing the webhook as a repository secret rather than passing it as a workflow input, which may be visible in logs. If you need help creating a secure webhook receiver (Lambda, small service), I can add an example implementation.

3) Secrets and app configuration

- For runtime secrets (API keys, DB credentials), either add them in the Streamlit Cloud UI under the app's "Secrets" section, or include a `.streamlit/secrets.toml` locally and add values via the Cloud UI. Do NOT commit secrets to Git.

4) Troubleshooting

- If a dependency fails during deployment, check `requirements.txt` for exact versions; Streamlit Cloud shows build logs.
- If the app doesn't update after a push and you have Auto deploy enabled, check the Streamlit app logs and GitHub push events.

Need help wiring a custom deploy webhook or configuring secrets? I can add an example AWS Lambda / small webhook service and update the workflow to call Streamlit's deploy API if you provide API docs or a token.
