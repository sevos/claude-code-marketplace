# Local Markdown PM System Connector

This connector implements PM operations for storing and managing tickets as markdown files in a local `docs/tickets/` directory.

## Overview

The local-markdown connector enables teams to maintain project tickets using simple markdown files with YAML frontmatter, tracked in version control alongside code. This approach is ideal for:

- Documentation-driven projects
- Teams that want tickets in git history
- Projects where PM system is secondary to code collaboration
- Minimal overhead setups with git as the source of truth

## System Detection

To detect if a project uses local-markdown:

1. **Check CLAUDE.md**: Does project define `System: Local-Markdown`?
2. **Check for docs/tickets directory**: Does `docs/tickets/` exist?
3. **Use AskUserQuestion tool**: If neither is conclusive (see SKILL.md "Using AskUserQuestion for User Input")

### Example CLAUDE.md Configuration

```markdown
# CLAUDE.md

## Project Management

### System
- **Type**: Local-Markdown

### Tickets Location
- **Directory**: docs/tickets
- **Format**: One ticket per file (TICKET-###.md)
```

## File Structure

Each ticket is stored as a separate markdown file in `docs/tickets/`:

```
docs/tickets/
├── TICKET-001.md
├── TICKET-002.md
├── TICKET-003.md
├── .ticket_counter       # Tracks next ID (auto-managed)
└── README.md            # (optional) Overview of project tickets
```

### Ticket File Format

Example: `docs/tickets/TICKET-001.md`

```markdown
---
title: "Implement user authentication"
type: "Feature"
status: "In Progress"
created_at: "2025-10-17T15:30:00"
estimate: 5
---

## Context
Users need a secure way to authenticate with the system.

## Requirements
- Support email/password login
- Add OAuth2 support
- Implement session management

## Acceptance Criteria
- [ ] Login endpoint returns JWT token
- [ ] Token validates on subsequent requests
- [ ] Logout clears session
- [ ] Error handling for invalid credentials
```

### Frontmatter Schema

**Required fields**:
- `title` (string): Ticket title
- `type` (string): Ticket type (Feature, Bug, Enhancement, Documentation, Refactor, Testing, Infrastructure)
- `status` (string): Current status (Backlog, Ready, In Progress, In Review, Done)
- `created_at` (ISO 8601 string): Creation timestamp

**Optional fields**:
- `parent` (string): Parent ticket ID for sub-tickets (e.g., "TICKET-001")
- `blocks` (string or array): Ticket ID(s) this ticket blocks
- `blocked_by` (string or array): Ticket ID(s) blocking this ticket
- `labels` (array): Tags/labels for categorization
- `estimate` (number): Story point estimate
- `updated_at` (ISO 8601 string): Last update timestamp
- `assignee` (string): Assigned person (optional)
- `notes` (string): Additional metadata or context

## Core Operations

All operations are implemented in `scripts/markdown_tickets.py` and invoked via command line.

### 1. Discovery: Establish Tickets Context

**Process**:
1. Check CLAUDE.md for explicit configuration
2. Verify `docs/tickets/` directory exists
3. Optionally read `docs/tickets/README.md` for project context

**Environment Variable**:
```bash
TICKETS_DIR=docs/tickets
```

### 2. Query: Search and Filter Issues

**Function**: `scripts/markdown_tickets.py list [status] [type]`

Search tickets using the Python script:

```bash
# List all tickets
python scripts/markdown_tickets.py list

# List by status
python scripts/markdown_tickets.py list "In Progress"

# List by type
python scripts/markdown_tickets.py list "" "Feature"

# List specific combination
TICKETS_DIR=./docs/tickets python scripts/markdown_tickets.py list "Backlog" "Bug"
```

**Output**: JSON array of tickets with metadata (excludes body content)

```json
[
  {
    "id": "TICKET-001",
    "title": "Implement user authentication",
    "type": "Feature",
    "status": "In Progress",
    "created_at": "2025-10-17T15:30:00",
    "estimate": 5
  }
]
```

**Search Function**: `scripts/markdown_tickets.py search <query> [status]`

```bash
# Search by text
python scripts/markdown_tickets.py search "authentication"

# Search with filter
python scripts/markdown_tickets.py search "auth" "In Progress"
```

### 3. Read: Retrieve Issue Details

**Function**: `scripts/markdown_tickets.py get <ticket_id>`

Fetch full ticket including body:

```bash
python scripts/markdown_tickets.py get TICKET-001
```

**Output**: JSON object with all metadata and body content

```json
{
  "id": "TICKET-001",
  "title": "Implement user authentication",
  "type": "Feature",
  "status": "In Progress",
  "created_at": "2025-10-17T15:30:00",
  "estimate": 5,
  "body": "## Context\n...",
  "_file": "TICKET-001.md"
}
```

**Get Sub-tickets**: `scripts/markdown_tickets.py get-subtickets <parent_id>`

```bash
# Get all child tickets of an epic
python scripts/markdown_tickets.py get-subtickets TICKET-001
```

Returns: JSON array of sub-tickets

### 4. Create: New Issues

**Function**: `scripts/markdown_tickets.py create`

Create new ticket via stdin:

```bash
cat <<EOF | python scripts/markdown_tickets.py create
{
  "title": "Add password reset flow",
  "description": "## Context\nUsers need to reset forgotten passwords...",
  "type": "Feature",
  "estimate": 3
}
EOF
```

**Parameters**:
- `title` (required): Ticket title
- `description` (required): Ticket body/description
- `type` (required): Feature, Bug, Enhancement, etc.
- `parent` (optional): Parent ticket ID
- `estimate` (optional): Story points
- `status` (optional): Defaults to "Backlog"
- `labels` (optional): Array of labels

**Output**: Created ticket object with auto-generated ID

```json
{
  "id": "TICKET-002",
  "title": "Add password reset flow",
  "type": "Feature",
  "status": "Backlog",
  "created_at": "2025-10-17T16:00:00",
  "body": "## Context\n..."
}
```

**Important**: ID generation is handled by the script. Claude should never manually generate IDs.

### 5. Update: Modify Existing Issues

**Function**: `scripts/markdown_tickets.py update <ticket_id>`

Update ticket via stdin:

```bash
cat <<EOF | python scripts/markdown_tickets.py update TICKET-001
{
  "status": "Done",
  "body": "Updated description with new requirements"
}
EOF
```

**Parameters**:
- `status`: New status
- `body` or `description`: New ticket body
- Any other metadata fields (title, estimate, labels, etc.)

**Output**: Updated ticket object

```json
{
  "id": "TICKET-001",
  "title": "Implement user authentication",
  "status": "Done",
  "created_at": "2025-10-17T15:30:00",
  "updated_at": "2025-10-17T17:00:00"
}
```

### 6. Dependency Analysis

**Function**: `scripts/markdown_tickets.py analyze-dependencies`

Analyze all ticket relationships:

```bash
python scripts/markdown_tickets.py analyze-dependencies
```

**Output**: Dependency graph

```json
{
  "blocks": {
    "TICKET-001": ["TICKET-002", "TICKET-003"]
  },
  "blocked_by": {
    "TICKET-002": ["TICKET-001"]
  },
  "parent": {
    "TICKET-002": "TICKET-001",
    "TICKET-003": "TICKET-001"
  },
  "total_tickets": 3
}
```

## Local-Markdown Specific Concepts

### Ticket ID Format
- Sequential numbering: TICKET-001, TICKET-002, etc.
- Zero-padded to 3 digits for consistent sorting
- `.ticket_counter` file tracks next ID (auto-managed)
- IDs are **never** manually generated; always use the script

### File-Based Relationships

**Parent/Child** (Epics):
- Set `parent: "TICKET-001"` in child ticket
- Query: `get-subtickets TICKET-001` returns all children

**Blocks/Blocked-by** (Dependencies):
- Set `blocks: "TICKET-003"` to indicate this blocks another
- Set `blocked_by: "TICKET-002"` to indicate this is blocked
- Can be single string or array of IDs

**Example Epic with Sub-tickets**:
```markdown
# TICKET-001.md (Epic)
---
title: "Email feature rollout"
type: "Feature"
status: "In Progress"
---

Epic description...

# TICKET-002.md (Sub-ticket)
---
title: "Design email schema"
type: "Feature"
parent: "TICKET-001"
blocks: ["TICKET-003", "TICKET-004"]
---

Design details...

# TICKET-003.md (Sub-ticket)
---
title: "Implement email API"
type: "Feature"
parent: "TICKET-001"
blocked_by: "TICKET-002"
---

API implementation...
```

### Version Control Integration

Since tickets are markdown files in version control:

- **Git History**: Ticket changes appear in commit history
- **Pull Requests**: Ticket changes go through code review
- **Branches**: Work tickets on feature branches
- **Blame/Annotate**: See who and when each ticket was changed

### Directory Structure Best Practice

```
docs/
├── tickets/
│   ├── TICKET-001.md       # Epic: Authentication
│   ├── TICKET-002.md       # Sub: Schema design
│   ├── TICKET-003.md       # Sub: API implementation
│   ├── TICKET-004.md       # Feature: Email sending
│   └── README.md           # Index and guidelines
├── architecture/
├── guides/
└── api.md
```

## Common Workflows

### Workflow: Create Epic with Sub-tickets

```bash
# 1. Create epic
cat <<EOF | python scripts/markdown_tickets.py create
{
  "title": "Implement email digest feature",
  "description": "## Overview\nUsers can opt-in to weekly email digests...",
  "type": "Feature"
}
EOF
# Returns: TICKET-001

# 2. Create sub-ticket 1
cat <<EOF | python scripts/markdown_tickets.py create
{
  "title": "Design digest schema",
  "description": "Database schema for storing digests...",
  "type": "Feature",
  "parent": "TICKET-001",
  "estimate": 2
}
EOF
# Returns: TICKET-002

# 3. Create sub-ticket 2 (blocked by #1)
cat <<EOF | python scripts/markdown_tickets.py create
{
  "title": "Implement digest API",
  "description": "REST endpoint for digest operations...",
  "type": "Feature",
  "parent": "TICKET-001",
  "blocked_by": "TICKET-002",
  "estimate": 5
}
EOF
# Returns: TICKET-003
```

### Workflow: Search and Analyze Multiple Tickets

```bash
# 1. List all feature tickets in backlog
python scripts/markdown_tickets.py list "Backlog" "Feature"

# 2. Search for related tickets
python scripts/markdown_tickets.py search "email"

# 3. Analyze dependencies to understand blockers
python scripts/markdown_tickets.py analyze-dependencies

# 4. Get full details of specific ticket
python scripts/markdown_tickets.py get TICKET-001

# 5. Get all sub-tickets of epic
python scripts/markdown_tickets.py get-subtickets TICKET-001
```

### Workflow: Propose and Apply Changes

```bash
# 1. Get current ticket
python scripts/markdown_tickets.py get TICKET-001

# 2. (Claude presents proposed changes to user)

# 3. User confirms
# (In SKILL.md workflow: wait for explicit user confirmation)

# 4. Apply changes
cat <<EOF | python scripts/markdown_tickets.py update TICKET-001
{
  "status": "In Progress",
  "body": "Updated description with new requirements..."
}
EOF
```

## Error Handling

**Common Error Scenarios**:

| Scenario | Solution |
|----------|----------|
| `docs/tickets/` directory doesn't exist | Script creates it automatically |
| Ticket ID not found | Verify ticket ID format (TICKET-###) and file exists |
| Invalid YAML in frontmatter | Fix YAML syntax and retry |
| Parent ticket doesn't exist | Create parent first, or remove parent field |
| Circular dependency (A blocks B, B blocks A) | Script detects but doesn't prevent; team should fix |

**Approach**:
- Always validate TICKETS_DIR is set correctly
- Verify tickets directory exists before operations
- Parse output as JSON and check for `error` field
- For sub-tickets, always verify parent exists first

## Integration with PM Assistant Skill

### Detection Logic (in SKILL.md)

1. Check for `CLAUDE.md` with `System: Local-Markdown`
2. Check for `docs/tickets/` directory
3. Use AskUserQuestion tool if ambiguous

### SKILL.md Workflow Modifications

When local-markdown is detected:

- All ticket queries use: `python scripts/markdown_tickets.py <operation>`
- Set `TICKETS_DIR` environment variable
- Parse JSON output from script
- Follow same analysis patterns as Linear (system-agnostic)
- All relationship fields use frontmatter metadata

### Example Usage in SKILL.md

```markdown
## Query Tickets
python scripts/markdown_tickets.py list [status] [type]

## Get Full Ticket
python scripts/markdown_tickets.py get TICKET-001

## Search
python scripts/markdown_tickets.py search "query text"

## Analyze Dependencies
python scripts/markdown_tickets.py analyze-dependencies
```

## Setup

For installation and setup instructions, see:
- **`connectors/local-markdown/setup.md`** - Step-by-step setup guide

## Notes

- All timestamps are ISO 8601 format
- Descriptions support Markdown formatting
- The `.ticket_counter` file is auto-managed; don't edit manually
- Relationship fields (parent, blocks, blocked_by) accept single string or array
- Script requires Python 3.7+ and PyYAML library
- For large ticket counts (1000+), consider index-based approach in future
