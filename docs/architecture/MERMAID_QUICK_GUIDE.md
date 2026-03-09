# Quick Guide: Creating Mermaid Diagrams

**Mermaid** lets you create diagrams using simple text syntax that renders automatically in GitHub.

---

## 🚀 Quick Start

### 1. Basic Flowchart

```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B
```

**Code:**
```
graph LR
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B
```

---

## 📊 Common Diagram Types

### Flowchart / Process Diagram

```mermaid
flowchart TB
    Start[Upload Report] --> Validate[Validate Data]
    Validate --> Check{Valid?}
    Check -->|Yes| Process[Process Report]
    Check -->|No| Error[Show Error]
    Process --> End[Complete]
```

**Syntax:**
- `graph TB` or `flowchart TB` (TB = Top to Bottom)
- `LR` = Left to Right, `RL` = Right to Left, `BT` = Bottom to Top
- `[Text]` = Rectangle, `{Text}` = Diamond, `([Text])` = Stadium

---

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant App
    participant Database
    
    User->>App: Submit Report
    App->>Database: Save Data
    Database-->>App: Confirm
    App-->>User: Success Message
```

**Code:**
```
sequenceDiagram
    participant User
    participant App
    participant Database
    
    User->>App: Submit Report
    App->>Database: Save Data
    Database-->>App: Confirm
    App-->>User: Success Message
```

---

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review: Submit
    Review --> Approved: Accept
    Review --> Draft: Reject
    Approved --> [*]
```

---

### Entity Relationship Diagram

```mermaid
erDiagram
    REPORT ||--o{ ROW : contains
    USER ||--o{ REPORT : creates
    
    REPORT {
        string report_id
        string report_type
        date upload_date
    }
    
    ROW {
        string row_id
        string report_id
        json data
    }
```

---

## 🎨 Styling & Formatting

### Add Colors

```mermaid
graph LR
    A[Step 1] --> B[Step 2]
    B --> C[Step 3]
    
    style A fill:#d4edda
    style B fill:#fff3cd
    style C fill:#f8d7da
```

**Code:**
```
style A fill:#d4edda
style B fill:#fff3cd
style C fill:#f8d7da
```

---

### Subgraphs (Group Components)

```mermaid
graph TB
    subgraph "Frontend"
        A[UI]
        B[Auth]
    end
    
    subgraph "Backend"
        C[API]
        D[Database]
    end
    
    A --> C
    B --> C
    C --> D
```

---

### Arrow Types

```mermaid
graph LR
    A -->|Solid| B
    B -.->|Dotted| C
    C ==>|Thick| D
    D ---|Plain| E
```

**Code:**
```
A -->|Label| B    (Solid arrow with label)
B -.->|Label| C   (Dotted arrow)
C ==>|Label| D    (Thick arrow)
D ---|Label| E    (Plain line)
```

---

## 🛠️ Creating Your Own Diagrams

### Step 1: Write the Code

In any markdown file, create a code fence with `mermaid`:

\```mermaid
graph LR
    A[Your Node] --> B[Another Node]
\```

### Step 2: Test Online

Use the **Mermaid Live Editor** to preview and test:
👉 https://mermaid.live/

### Step 3: Add to Repository

Paste your Mermaid code into any `.md` file in your repository. GitHub will automatically render it!

---

## 📝 Examples for OCSS Command Center

### System Overview

```mermaid
graph TB
    Users[OCSS Staff] -->|HTTPS| Gateway[County Gateway]
    Gateway -->|SSO| App[Command Center]
    App --> Reports[Report Engine]
    App --> Dashboard[Dashboards]
    Reports --> Data[(State Files)]
    
    style Users fill:#e1f5ff
    style Gateway fill:#fff3cd
    style App fill:#d4edda
```

### Authentication Flow

```mermaid
sequenceDiagram
    User->>Gateway: Access App
    Gateway->>SSO: Verify Identity
    SSO->>Gateway: Auth Token
    Gateway->>App: Request + Token
    App->>User: Role-Based UI
```

### Deployment Architecture

```mermaid
graph TB
    subgraph "County Network"
        Proxy[NGINX Proxy]
        Server[App Server]
        Storage[(File Storage)]
    end
    
    Users[County Staff] -->|HTTPS| Proxy
    Proxy --> Server
    Server --> Storage
```

---

## 💡 Tips & Tricks

1. **Start Simple** - Begin with basic flowcharts, add complexity gradually
2. **Use Live Editor** - Test at mermaid.live before committing
3. **Check Syntax** - One wrong character can break rendering
4. **Add Comments** - Use `%%` for comments: `%% This is a comment`
5. **Preview Locally** - Install "Markdown Preview Mermaid Support" VS Code extension

---

## 🔗 Resources

- **Official Docs:** https://mermaid.js.org/
- **Live Editor:** https://mermaid.live/
- **Syntax Guide:** https://mermaid.js.org/intro/syntax-reference.html
- **Examples:** https://mermaid.js.org/ecosystem/integrations.html

---

## ✅ Advantages for IT Documentation

| Feature | Mermaid | PNG/JPG Images |
|---------|---------|---------------|
| Version Control | ✅ Text-based diffs | ❌ Binary files |
| Easy Updates | ✅ Edit text | ❌ Recreate image |
| GitHub Rendering | ✅ Automatic | ⚠️ Upload required |
| Accessibility | ✅ Screen reader friendly | ❌ Alt text only |
| File Size | ✅ Small (text) | ⚠️ Large (images) |
| Collaboration | ✅ Easy to review | ❌ Hard to review |

---

**Ready to create diagrams?**  
See [mermaid_diagrams.md](./mermaid_diagrams.md) for complete OCSS Command Center examples!
