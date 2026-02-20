# OCSS Command Center - Security & Deployment Brief

**Prepared For:** Cuyahoga County Office of Child Support Services (OCSS)  
**Date:** February 19, 2026  
**Subject:** Application Safety Features & Path to Production Deployment

---

## Executive Summary

The OCSS Command Center is currently built as a **Demonstration Prototype (v1.0)**. While it functions as a complete operational application with significant process logic, it is designed to run in a controlled demo environment.

To meet the rigorous security and compliance standards of a county health and human services agency, the application is architected to be **modular**, allowing its security and data layers to be "swapped out" for enterprise-grade components approved by Cuyahoga County IT.

---

## 1. Current Safety Features (Demo Ready)

The application presently includes robust **logic-level safety controls** designed to prevent operational errors and ensure data integrity during use:

### ✅ Input Validation & Sanitation
- **Strict File Typing**: The system only accepts valid Excel (`.xlsx`, `.xls`) or CSV files, rejecting executables or scripts.
- **Duplicate Prevention**: Ingestion logic scans metadata and content hashes to prevent duplicate monthly reports from corrupting the dataset.
- **Data Normalization**: Automated cleaning ensures consistent formatting (e.g., standardized dates and caseload numbers) regardless of input style.

### ✅ Operational Guardrails
- **Incomplete Work Blocking**: Support Officers cannot submit a caseload as "Complete" if any row remains in "Pending" or "In Progress" status. This prevents incomplete data from moving upstream to federal reporting lines.
- **Session Isolation**: Data is stored in the specific user's browser session memory. One user cannot accidentally view or modify another active user's session data during a demo.

### ✅ Role-Based Interface
- **Context-Aware UI**: The interface automatically hides administrative functions (e.g., "Delete User", "Reassign Caseload") from lower-level roles, preventing accidental unauthorized actions.

---

## 2. Adaptation for Agency-Wide Deployment (Production)

To move from "Demo" to "Agency-Wide Production," the application requires adaptation in three specific infrastructure layers. These changes **do not require rewriting the application**, but rather configuring it to use County resources.

### A. Authentication & Identity Management
*   **Current State:** Unsecured role selector (Drop-down menu).
*   **Agency Adaptation:** Integrate with **Microsoft Azure Active Directory (Azure AD)**.
    *   **Result:** Staff log in with their standard County credentials (e.g., `jsmith@cuyahogacounty.us`).
    *   **Automated Access:** Roles (Director, Supervisor, Support Officer) are automatically assigned based on the user's existing AD Group membership, removing manual user management.

### B. Data Persistence & PII Protection
*   **Current State:** In-memory session storage (fast, but resets on shutdown).
*   **Agency Adaptation:** Connect the backend to a secure, encrypted database (e.g., **SQL Server** or **PostgreSQL**) managed by County IT.
    *   **PII Safety:** Child Support data contains sensitive PII. In a production build, this data remains in the encrypted database. The Streamlit app acts only as a "viewing glass," ensuring data is encrypted both **in transit** (TLS 1.3) and **at rest** (AES-256).

### C. Hosting & Infrastructure
*   **Current State:** Local/Cloud Development Environment.
*   **Agency Adaptation:** The application is container-ready (Docker/Kubernetes). It can be deployed to:
    *   **Azure Government Cloud**: Secure, FedRAMP-compliant hosting.
    *   **On-Premise Intranet**: Deployed inside the County firewall, making it inaccessible from the public internet.

---

## 3. Deployment Roadmap Recommendation

To safely introduce this tool to the agency, we recommend a phased verification approach:

| Phase | Environment | Goal | Data Sensitivity |
| :--- | :--- | :--- | :--- |
| **1. Soft Demo** | Local Laptop | Verify operational workflow | **Dummy Data Only** |
| **2. IT Pilot** | Internal Dev Server | Verify AD Integration & Database | **Dummy Data** |
| **3. UAT** | Staging Environment | User Acceptance Testing | **De-identified Real Data** |
| **4. Live** | Production Intranet | Agency-Wide Rollout | **Live PII Data** |

---

**Conclusion:**  
The OCSS Command Center is "business logic ready." Its workflow for processing cases is mature. The path to agency-wide deployment involves standard IT integration steps—connecting it to the County's existing secure login and database systems—rather than rebuilding the application itself.
