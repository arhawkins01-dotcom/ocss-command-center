# OCSS Command Center - Architecture Documentation

This folder contains enterprise architecture documentation, system diagrams, and technical design materials for IT review.

---

## Quick Access

### Core Architecture Documents

- **[OCSS_Command_Center_Architecture_Guide.md](./OCSS_Command_Center_Architecture_Guide.md)** - Complete architecture guide with system design, data flow, security model, and infrastructure requirements
- **[architecture_diagram.md](./architecture_diagram.md)** - Visual system architecture (GitHub preview)
- **[data_flow_diagram.md](./data_flow_diagram.md)** - End-to-end data processing flow (GitHub preview)
- **[mermaid_diagrams.md](./mermaid_diagrams.md)** - Interactive Mermaid diagrams (text-based, renders in GitHub)

### Technical Design Documents

- **[COMMAND_CENTER_DECISION_LOGIC.md](./COMMAND_CENTER_DECISION_LOGIC.md)** - Business logic and decision workflows
- **[COMMAND_CENTER_REPORT_PROCESSING.md](./COMMAND_CENTER_REPORT_PROCESSING.md)** - Report ingestion and processing architecture
- **[ALERT_SYSTEM_EXAMPLES.md](./ALERT_SYSTEM_EXAMPLES.md)** - Alert engine design and escalation logic

### Diagram Creation

- **[MERMAID_QUICK_GUIDE.md](./MERMAID_QUICK_GUIDE.md)** - Learn how to create text-based diagrams with Mermaid

---

## For IT Reviewers

**Start Here:** [OCSS_Command_Center_Architecture_Guide.md](./OCSS_Command_Center_Architecture_Guide.md)

This document provides:
- Enterprise system architecture diagram
- Data flow and processing pipeline
- Data security model and system boundaries
- Authentication & access control design
- Infrastructure impact assessment
- Recommended pilot testing approach

### Key Technical Details

- **Framework:** Python 3.9+ with Streamlit 1.x
- **Deployment:** County-hosted internal application server
- **Authentication:** SSO header mode integration
- **Data Persistence:** File-based storage (JSON)
- **Network:** Internal county network only
- **Systems of Record:** SETS, OnBase, ODJFS (external)

---

## Visual Architecture Previews

The architecture diagrams are available in multiple formats:

### Static Diagrams (Markdown)
- [System Architecture Diagram](./architecture_diagram.md) - Component layout and integration points
- [Data Flow Diagram](./data_flow_diagram.md) - Report processing workflow

### Interactive Diagrams (Mermaid)
- [Mermaid Diagrams](./mermaid_diagrams.md) - Text-based diagrams with multiple views:
  - System Architecture
  - Data Flow
  - Component Diagram
  - Deployment Topology
  - Authentication Flow
  - State Machine
  - Entity Relationships

**Why Mermaid?**
- ✅ Renders directly in GitHub (no image files needed)
- ✅ Version controlled as text
- ✅ Easy to update and maintain
- ✅ Multiple diagram types (flowcharts, sequences, state machines, ERDs)

---

**Last Updated:** March 9, 2026  
**Version:** 1.1
