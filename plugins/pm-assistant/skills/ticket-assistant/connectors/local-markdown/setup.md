# Local Markdown Connector - Setup Guide

## Installation

### Step 1: Install Dependencies
```bash
pip install pyyaml
```

### Step 2: Configure Your Project

Create `CLAUDE.md` in your project root:
```markdown
# CLAUDE.md

## Project Management
- **System**: Local-Markdown
- **Directory**: docs/tickets
```

### Step 3: Create Tickets Directory
```bash
mkdir -p docs/tickets
touch docs/tickets/.keep
```

The `.keep` file ensures git tracks the empty `docs/tickets/` directory.

### Step 4: Test the Script

Create a test ticket to verify everything works:
```bash
cat <<'EOF' | TICKETS_DIR=docs/tickets python scripts/markdown_tickets.py create
{
  "title": "Setup authentication",
  "description": "Implement user authentication with JWT tokens",
  "type": "Feature",
  "estimate": 5
}
EOF
```

Expected output:
```json
{
  "id": "TICKET-001",
  "title": "Setup authentication",
  "type": "Feature",
  "status": "Backlog",
  "created_at": "2025-10-17T23:13:26.177589",
  "estimate": 5,
  "body": "Implement user authentication with JWT tokens"
}
```

### Step 5: View Your Ticket
```bash
cat docs/tickets/TICKET-001.md
```

Output:
```markdown
---
title: Setup authentication
type: Feature
status: Backlog
created_at: '2025-10-17T23:13:26.177589'
estimate: 5
---
Implement user authentication with JWT tokens
```

### Step 6: Clean Up Test Ticket

Delete the test ticket to start with a clean slate:
```bash
rm docs/tickets/TICKET-001.md
```

Verify it's gone and `.keep` remains:
```bash
ls -la docs/tickets/
```

### Step 7: Commit Initial Setup to Git
```bash
git add CLAUDE.md docs/tickets/
git commit -m "setup(pm): Initialize local-markdown ticket system"
```

## Next Steps

1. ✅ Setup complete with clean ticket directory
2. ✅ Ready to create your first real ticket
3. ✅ See `connectors/local-markdown.md` for all operations
4. ✅ Use the ticket-assistant skill to create and manage tickets
