
    listen 443 ssl http2;
    server_name ocss.yourdomain.com;

    ssl_certificate /etc/ssl/certs/your-cert.crt;
    ssl_certificate_key /etc/ssl/private/your-key.key;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        OCSS Command Center — Technical Guide

        Version: 1.1.0
        Last Updated: 2026-02-27

        ---

        This document mirrors the new User Manual structure and provides developer-focused details about architecture, data flow, KB seeding rules, deployment, and maintenance.

        Key locations:
        - App entry: `app/app.py`
        - KB seed sources: `docs/USER_MANUAL.md`, `docs/TECHNICAL_GUIDE.md`
        - KB targets: `data/knowledge_base/user_guide.md`, `data/knowledge_base/technical_guide.md`
        - Seed manifest: `data/knowledge_base/.seed_manifest.json`

        ### KB Seeding and Admin Behavior
        - On first run the app seeds `User Guide` and `Technical Guide` from `docs/` into `data/knowledge_base/`.
        - The manifest tracks `source_hash` and `target_hash` for each seeded file along with `seeded_at` and `edited_by_admin` flags.
        - If `edited_by_admin` is `true`, the seeder will not overwrite the in-app copy on subsequent restarts.

        ---

        ## Architecture & Data Flow (Developer View)

        - `app/app.py` manages role routing, top-level UI, and KB rendering.
        - `app/report_engine.py` and `app/report_utils.py` handle parsing, normalization, and ingestion bookkeeping.
        - `data/state/ocss_app_state.json` stores organizational configuration, user assignments, and alert acknowledgements.
        - Uploaded report content is stored in session state for immediate interactive processing.

        Report ingestion (high level):
        1. Upload via Streamlit `file_uploader`.
        2. `report_engine` converts into DataFrame and computes a SHA256 content hash.
        3. Duplicate detection runs against session uploads and previously ingested metadata.
        4. Ingestion record with `ingestion_id` is created and stored in session for the current user flow.

        Important helpers and entry points:
        - `_sha256_file(path)` — compute file hash used by the seed manifest
        - `_read_text_file(path)` — used by KB rendering to safely load Markdown
        - `render_knowledge_base()` — admin/editor UI and download/upload endpoints

        ---

        ## Due-Date Logic & Alerts

        - Due-date (`due_at`) is computed at ingestion time by `_compute_due_at()` using `period` and configured monthly offsets.
        - Alerts are generated comparing `now()` to `due_at` and ingestion timestamps; the escalation ladder maps age buckets to roles.
        - Acknowledgements are persisted to `data/state/ocss_app_state.json` so leadership can filter acknowledged items across restarts.

        ---

        ## Deployment & Runtime

        Local development:
        ```bash
        pip install -r app/requirements.txt
        streamlit run app/app.py --server.enableCORS false --server.enableXsrfProtection false
        ```

        Production recommendations:
        - Terminate TLS at an external reverse proxy (Nginx) and enable `OCSS_AUTH_MODE=header` when integrating with SSO.
        - Containerize with Docker; mount `./data` for persisted KB and state.

        Health & monitoring:
        - Streamlit exposes an internal health endpoint at `/_stcore/health` in container setups.
        - Exported files and artifacts are placed in `exports/`; logs go to `logs/`.

        ---

        ## Developer & Maintenance Notes

        - To reseed KB from repo sources: remove the `edited_by_admin` flag for the file in `data/knowledge_base/.seed_manifest.json` or delete the target file then restart.
        - When updating `docs/` files, the seeder will compute updated hashes automatically; if deterministic control is needed, update the manifest explicitly.
        - Unit tests: run `pytest -q` to validate core logic; main test modules cover `report_utils` and `action_logic`.

        End of Technical Guide

2. Workaround: Save/Download CSV before page close
3. Plan: Implement database persistence (Phase 2)

---

## Appendix C: Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-18 | Initial release - MVP with 5 roles |
| 1.1.0 | Planned | Database integration, authentication |
| 1.2.0 | Planned | Load balancing, improved security |
| 2.0.0 | Planned | API layer, advanced analytics |

---

## Conclusion

The OCSS Command Center is a well-architected, production-ready application built on proven technologies. With proper deployment and the recommended Phase-based implementation plan, it will provide significant value to your organization.

**Recommended Action:** Approve for staging environment deployment with target launch 4-6 weeks from IT approval.

---

**Document Version:** 1.0  
**Last Updated:** February 21, 2026  
**Prepared For:** IT Department Review  
**Contact:** [Your contact information]
