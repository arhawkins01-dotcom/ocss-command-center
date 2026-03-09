# OCSS Command Center - IT Documentation

This folder contains deployment guides, security documentation, and technical implementation materials for Cuyahoga County IT Department.

---

## Quick Access

### Primary IT Resources

- **[README_IT_DEPLOYMENT.md](./README_IT_DEPLOYMENT.md)** - IT deployment overview
- **[IT_IMPLEMENTATION_GUIDE.md](./IT_IMPLEMENTATION_GUIDE.md)** - Step-by-step deployment instructions
- **[SECURITY_AND_DEPLOYMENT_BRIEF.md](./SECURITY_AND_DEPLOYMENT_BRIEF.md)** - Security model and infrastructure requirements
- **[IT_QUICK_START.md](./IT_QUICK_START.md)** - Quick reference for IT setup

### Demo & Testing Materials

- **[IT_DEVELOPER_DEMO_RUNBOOK.md](./IT_DEVELOPER_DEMO_RUNBOOK.md)** - Demo environment setup
- **[IT_DEMO_SCRIPT.md](./IT_DEMO_SCRIPT.md)** - Demo walkthrough script
- **[IT_DEVELOPER_2MIN_OPENING_SCRIPT.md](./IT_DEVELOPER_2MIN_OPENING_SCRIPT.md)** - Quick demo introduction
- **[IT_DEVELOPER_2MIN_CLOSING_SCRIPT.md](./IT_DEVELOPER_2MIN_CLOSING_SCRIPT.md)** - Demo conclusion

### Additional Resources

- **[SHARE_WITH_IT_TEMPLATE.md](./SHARE_WITH_IT_TEMPLATE.md)** - Template for IT communication
- **[GITHUB_ACCESS_GUIDE.md](./GITHUB_ACCESS_GUIDE.md)** - GitHub repository access instructions

---

## For IT Deployment

**Start Here:** [IT_IMPLEMENTATION_GUIDE.md](./IT_IMPLEMENTATION_GUIDE.md)

### Deployment Requirements

- **Server:** Windows or Linux internal application server
- **Runtime:** Python 3.9+ with pip package manager
- **Network:** Internal county network only (no external internet required)
- **Authentication:** SSO header mode integration with county auth infrastructure
- **Storage:** File-based persistence (no database server required)
- **Reverse Proxy:** NGINX or equivalent for SSL/TLS termination and SSO integration

### Security Model

See [SECURITY_AND_DEPLOYMENT_BRIEF.md](./SECURITY_AND_DEPLOYMENT_BRIEF.md) for:
- Authentication & authorization design
- Data security boundaries
- Session management
- System-of-record separation
- Network security requirements

---

## Infrastructure Impact

**One Internal Application Server Required**

- Standard county server allocation
- No external cloud dependencies
- No database server required
- Standard HTTPS reverse proxy configuration
- SSO header mode integration with existing auth infrastructure

**No Recurring Cloud Costs**

---

## Architecture Documentation

For complete system architecture, see:
- [Architecture Guide](../architecture/OCSS_Command_Center_Architecture_Guide.md)
- [System Architecture Diagram](../architecture/architecture_diagram.md)
- [Data Flow Diagram](../architecture/data_flow_diagram.md)

---

**Last Updated:** March 9, 2026  
**Ready for IT Review**
