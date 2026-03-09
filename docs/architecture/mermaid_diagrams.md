# OCSS Command Center - Mermaid Diagram Examples

**Version:** 1.0  
**Last Updated:** March 9, 2026

This document demonstrates how to create visual diagrams using Mermaid syntax that renders directly in GitHub.

---

## System Architecture Diagram

```mermaid
graph TB
    subgraph "User Layer"
        Users[OCSS Users<br/>Director | Program Officers<br/>Supervisors | Support Officers]
    end
    
    subgraph "Network Layer"
        Gateway[County Gateway / NGINX<br/>SSL/TLS | SSO | Security]
    end
    
    subgraph "Application Layer"
        App[OCSS Command Center<br/>Python + Streamlit]
        Auth[Authentication<br/>& RBAC]
        Reports[Report Engine<br/>Pandas]
        Dashboards[KPI Dashboards<br/>& Analytics]
        QA[QA & Compliance<br/>Engine]
        Tickets[Help Ticket<br/>Center]
    end
    
    subgraph "Data Layer"
        State[(Application State<br/>JSON Files)]
        Exports[Export Services<br/>Excel | Word | CSV]
    end
    
    subgraph "External Systems"
        SETS[SETS<br/>Child Support System]
        OnBase[Hyland OnBase<br/>Document Management]
        ODJFS[ODJFS<br/>Reporting Infrastructure]
    end
    
    Users -->|HTTPS| Gateway
    Gateway -->|Authenticated| App
    App --> Auth
    App --> Reports
    App --> Dashboards
    App --> QA
    App --> Tickets
    Reports --> State
    App --> Exports
    App -.->|Read Only| SETS
    App -.->|Read Only| OnBase
    App -.->|Report Source| ODJFS
    
    style Users fill:#e1f5ff
    style Gateway fill:#fff3cd
    style App fill:#d4edda
    style State fill:#f8d7da
    style SETS fill:#e2e3e5
    style OnBase fill:#e2e3e5
    style ODJFS fill:#e2e3e5
```

---

## Data Flow Diagram

```mermaid
flowchart TD
    Start[ODJFS Operational Reports<br/>56RA | P-S | Locate] --> Upload[Program Officer<br/>Upload & Metadata]
    
    Upload --> Ingest[Report Ingestion<br/>Validation | Deduplication]
    
    Ingest --> Normalize[Normalization Engine<br/>Pandas Processing]
    
    Normalize --> Route{Route to<br/>Caseload}
    
    Route --> C1[Downtown Establishment<br/>Caseload 181000]
    Route --> C2[Midtown Enforcement<br/>Caseload 181001]
    Route --> C3[Uptown Collections<br/>Caseload 181002]
    
    C1 --> Alerts[Alert Engine<br/>Due Soon | Overdue]
    C2 --> Alerts
    C3 --> Alerts
    
    C1 --> Process[Support Officer<br/>Row Processing]
    C2 --> Process
    C3 --> Process
    
    Process --> QA[QA Validation<br/>Compliance Check]
    
    QA --> Complete{Complete &<br/>Compliant?}
    
    Complete -->|No| Process
    Complete -->|Yes| Dashboard[Leadership Dashboards<br/>KPIs | Metrics]
    
    Dashboard --> Export[Export Services<br/>Excel | Word | CSV]
    
    Complete -->|Yes| SOR[Systems of Record<br/>SETS | OnBase]
    
    style Start fill:#e1f5ff
    style Normalize fill:#d4edda
    style Alerts fill:#fff3cd
    style QA fill:#ffeaa7
    style Dashboard fill:#d4edda
    style SOR fill:#e2e3e5
```

---

## Architecture Component Diagram

```mermaid
graph LR
    subgraph "Frontend"
        UI[Streamlit UI<br/>Role-Based Views]
    end
    
    subgraph "Core Services"
        Auth[auth.py<br/>Authentication]
        Reports[report_engine.py<br/>Report Processing]
        Case[case_logic.py<br/>Caseload Management]
        QA[qa_compliance.py<br/>QA System]
        Notify[notify.py<br/>Alert Engine]
    end
    
    subgraph "Data Services"
        DB[database.py<br/>State Management]
        Export[report_utils.py<br/>Export Services]
    end
    
    subgraph "Configuration"
        Config[config/settings.py<br/>App Configuration]
    end
    
    UI --> Auth
    UI --> Reports
    UI --> Case
    UI --> QA
    UI --> Notify
    
    Reports --> DB
    Case --> DB
    QA --> DB
    Notify --> DB
    Reports --> Export
    
    Auth --> Config
    Reports --> Config
    
    style UI fill:#e1f5ff
    style Auth fill:#fff3cd
    style Reports fill:#d4edda
    style QA fill:#ffeaa7
    style DB fill:#f8d7da
```

---

## Deployment Topology Diagram

```mermaid
graph TB
    subgraph "County Network"
        subgraph "DMZ / Reverse Proxy"
            NGINX[NGINX Reverse Proxy<br/>SSL Termination<br/>SSO Integration]
        end
        
        subgraph "Application Server"
            App[OCSS Command Center<br/>Python + Streamlit<br/>Port 8501]
            Storage[File Storage<br/>data/state/<br/>logs/<br/>exports/]
        end
        
        subgraph "Authentication"
            SSO[County SSO<br/>Active Directory]
        end
    end
    
    Internet[County Staff<br/>Internal Network Only]
    
    Internet -->|HTTPS:443| NGINX
    NGINX -->|SSO Token| SSO
    SSO -->|Auth Header| NGINX
    NGINX -->|HTTP:8501| App
    App --> Storage
    
    style Internet fill:#e1f5ff
    style NGINX fill:#fff3cd
    style SSO fill:#ffeaa7
    style App fill:#d4edda
    style Storage fill:#f8d7da
```

---

## Authentication Flow Diagram

```mermaid
sequenceDiagram
    actor User as County Staff
    participant Gateway as County Gateway
    participant SSO as County SSO
    participant App as Command Center
    participant RBAC as Role Engine
    
    User->>Gateway: Access Application
    Gateway->>SSO: Authenticate User
    SSO->>Gateway: Return Auth Token
    Gateway->>App: Forward Request + SSO Header
    App->>RBAC: Extract User Identity
    RBAC->>App: Determine Role & Permissions
    App->>User: Render Role-Based Interface
    
    Note over User,App: All subsequent requests include SSO header
    
    User->>App: Perform Action
    App->>RBAC: Verify Permission
    
    alt Authorized
        RBAC->>App: Allow
        App->>User: Execute & Return Result
    else Unauthorized
        RBAC->>App: Deny
        App->>User: Access Denied Message
    end
```

---

## Report Processing State Machine

```mermaid
stateDiagram-v2
    [*] --> Uploaded: Program Officer Upload
    
    Uploaded --> Validating: Begin Validation
    Validating --> Rejected: Validation Failed
    Validating --> Normalized: Validation Passed
    
    Rejected --> [*]: Manual Review Required
    
    Normalized --> Assigned: Route to Caseload
    Assigned --> InProgress: Support Officer Starts
    
    InProgress --> InProgress: Save Progress
    InProgress --> Submitted: Submit Complete
    
    Submitted --> QAReview: Auto QA Sample
    
    QAReview --> Failed: Non-Compliant
    QAReview --> Approved: Compliant
    
    Failed --> InProgress: Return for Correction
    Approved --> Completed: Final Status
    
    Completed --> [*]: Archive & Dashboard
```

---

## Entity Relationship Diagram

```mermaid
erDiagram
    ORGANIZATION ||--o{ CASELOAD : has
    ORGANIZATION ||--o{ USER : employs
    CASELOAD ||--o{ REPORT : contains
    USER ||--o{ REPORT : processes
    REPORT ||--o{ REPORT_ROW : contains
    REPORT ||--o{ QA_SAMPLE : generates
    USER ||--o{ HELP_TICKET : creates
    CASELOAD ||--o{ ALERT : triggers
    
    ORGANIZATION {
        string org_id PK
        string org_name
        json departments
        json roles
    }
    
    CASELOAD {
        string caseload_id PK
        string org_id FK
        string unit_number
        string assigned_to
        string status
    }
    
    USER {
        string user_id PK
        string org_id FK
        string role
        string name
        json permissions
    }
    
    REPORT {
        string report_id PK
        string caseload_id FK
        string report_type
        date upload_date
        string status
        json metadata
    }
    
    REPORT_ROW {
        string row_id PK
        string report_id FK
        json row_data
        string status
        date processed_date
    }
    
    QA_SAMPLE {
        string sample_id PK
        string report_id FK
        string row_id FK
        int compliance_score
        json criteria_results
    }
    
    HELP_TICKET {
        string ticket_id PK
        string user_id FK
        string category
        string status
        date created
    }
    
    ALERT {
        string alert_id PK
        string caseload_id FK
        string alert_type
        date triggered
        boolean acknowledged
    }
```

---

## How to Use Mermaid Diagrams

### Syntax in Markdown

Simply wrap your Mermaid code in a code fence with `mermaid` language identifier:

\```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
\```

### Supported Diagram Types

1. **Flowchart** - `graph` or `flowchart`
2. **Sequence Diagram** - `sequenceDiagram`
3. **State Diagram** - `stateDiagram-v2`
4. **Entity Relationship** - `erDiagram`
5. **Gantt Chart** - `gantt`
6. **Pie Chart** - `pie`
7. **Class Diagram** - `classDiagram`

### Styling Tips

- Use `subgraph` to group related components
- Apply styles: `style NodeName fill:#color`
- Use arrow types: `-->` (solid), `-.->` (dotted), `==>` (thick)
- Add notes: `Note over A,B: Description`

### GitHub Rendering

✅ Mermaid diagrams render automatically in GitHub markdown files  
✅ No plugins or extensions required  
✅ Version controlled as text  
✅ Easy to update and maintain

---

## Additional Resources

- **Mermaid Documentation:** https://mermaid.js.org/
- **Live Editor:** https://mermaid.live/
- **VS Code Extension:** Mermaid Preview

---

**For IT Review:**
These diagrams are embedded directly in the architecture documentation and render automatically in GitHub. No separate image files needed!
