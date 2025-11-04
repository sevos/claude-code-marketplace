# Linear PM System Connector

This connector implements PM operations for the Linear project management system.

## Overview

The Linear connector provides the interface between the generic PM Assistant workflows and Linear's MCP server. All Linear-specific operations (discovery, query, create, update) are encapsulated here.

## System Detection

To detect if a project uses Linear:

1. **Check for MCP server**: Is `mcp__linear-server__get_user` available?
2. **Check CLAUDE.md**: Does project define `System: Linear`?
3. **Use AskUserQuestion tool**: If neither is conclusive (see SKILL.md "Using AskUserQuestion for User Input")

### Example CLAUDE.md Configuration

```markdown
# CLAUDE.md

## Project Management

### System
- **Type**: Linear

### Linear Team
- **Team Prefix**: PROD

### Linear Projects
- **Backend Services** - https://linear.app/yourworkspace/project/backend-services-abc123
- **Frontend UI** - https://linear.app/yourworkspace/project/frontend-ui-def456
```

## Core Operations

### 1. Discovery: Find Team and Project Context

**Process**:
1. Check CLAUDE.md for explicit configuration
2. If not found, call `mcp__linear-server__list_teams` to list available teams
3. Call `mcp__linear-server__list_projects` to find the project
4. Use AskUserQuestion tool if multiple options exist (present team/project choices with descriptions)

**Functions**:
```
mcp__linear-server__get_user
- No parameters required
- Returns: Current user information including team membership

mcp__linear-server__list_teams
- Returns all available teams in workspace
- Use to verify team ID/prefix before operations

mcp__linear-server__get_team
- Parameters: teamId (e.g., "AIA")
- Returns team details including projects, settings, labels

mcp__linear-server__list_projects
- Optional: Filter by team
- Returns all projects accessible to the user
- Use to find the correct project ID (e.g., "Email parser")

mcp__linear-server__get_project
- Parameters: projectId
- Returns project details, settings, team affiliation
```

### 2. Query: Search and Retrieve Issues

**Linear Filter Syntax**:
```
team:TEAMID                    # Filter by team prefix
project:"Project Name"         # Filter by exact project name
status:"In Progress"           # Filter by status
assignee:@me                   # Assigned to current user
parent:"EPIC-ID"              # Get sub-tickets of an epic
Combine with AND/OR operators
```

**Functions**:
```
mcp__linear-server__list_issues
- Parameters:
  - filter: Linear query filter (see syntax above)
  - limit: Number of results (optional)
- Returns: List of issues matching criteria
- Example: filter: "team:AIA project:\"Email parser\" status:\"In Progress\""

mcp__linear-server__get_issue
- Parameters: issueId (e.g., "AIA-123")
- Returns: Full issue details including description, acceptance criteria, relationships

mcp__linear-server__search_documentation
- Parameters: query string
- Returns: Matching documentation from Linear workspace
```

### 3. Read: Retrieve Relationships and Metadata

**Functions**:
```
mcp__linear-server__get_issue_status
- Parameters: statusId
- Returns: Status details

mcp__linear-server__list_issue_statuses
- Returns: All available statuses in workspace

mcp__linear-server__list_issue_labels
- Returns: All available labels with types (Type/Feature, Type/Bug, etc.)

mcp__linear-server__create_issue_label
- Parameters: name, color, description (optional)
- Returns: New label ID

mcp__linear-server__list_project_labels
- Parameters: projectId
- Returns: Labels configured for this project

mcp__linear-server__list_cycles
- Parameters: teamId (optional)
- Returns: All available cycles/sprints

mcp__linear-server__list_documents
- Optional: Filter by project
- Returns: All documents in workspace

mcp__linear-server__get_document
- Parameters: documentId
- Returns: Document content

mcp__linear-server__list_comments
- Parameters: issueId
- Returns: All comments on the issue
```

### 4. Create: New Issues

**Function**:
```
mcp__linear-server__create_issue
- Parameters:
  - teamId: Team prefix (e.g., "AIA")
  - projectId: Project identifier
  - title: Issue title (string, required)
  - description: Issue description (markdown, optional)
  - stateId: Status ID (optional)
  - assigneeId: User ID to assign (optional)
  - labelIds: Array of label IDs (optional)
  - cycleId: Sprint/cycle ID (optional)
  - parentId: Parent issue for sub-tickets (optional)
  - estimate: Story points (optional, numeric)
- Returns: Created issue object with ID
```

**Workflow for Creating Tickets**:
1. Prepare ticket data (title, description, acceptance criteria)
2. Fetch available labels with `list_issue_labels` (for Type/Feature, Type/Bug, etc.)
3. Get default project cycle with `list_cycles` if needed
4. Call `create_issue` with all parameters
5. Return created ticket ID and link

### 5. Update: Modify Existing Issues

**Function**:
```
mcp__linear-server__update_issue
- Parameters:
  - issueId: Issue identifier (e.g., "AIA-123")
  - title: New title (optional)
  - description: New description (optional)
  - stateId: New status (optional)
  - assigneeId: New assignee (optional)
  - labelIds: New labels (optional)
  - cycleId: New cycle (optional)
  - estimate: New estimate (optional)
- Returns: Updated issue object
```

**Workflow for Updating Tickets**:
1. Fetch existing ticket with `get_issue` to preserve unchanged fields
2. Prepare amendments
3. Call `update_issue` with changes
4. Report what was updated

### 6. Comments and Collaboration

**Functions**:
```
mcp__linear-server__create_comment
- Parameters:
  - issueId: Issue identifier
  - body: Comment text (markdown)
- Returns: Created comment object
```

## Linear-Specific Concepts

### Team Prefix and Issue IDs
- Each Linear team has a unique prefix (e.g., "AIA", "PROD", "ENG")
- Issue IDs include the team prefix: AIA-100, PROD-50, etc.
- Always scope operations to the correct team using filters

### Cycles (Sprints)
- Linear calls sprints "cycles"
- Cycles are team-specific
- Use `list_cycles` to get available sprints for scheduling

### Labels
- Labels have types: `Type/Feature`, `Type/Bug`, `Type/Enhancement`, etc.
- Labels are workspace-wide or project-specific
- Fetch available labels before creating issues to use correct label IDs

### Relationships: Parent/Child and Blocks/Blocked-by
- **Parent/Child**: Epics have sub-tickets (parent issue links)
- **Blocks/Blocked-by**: Explicit dependency relationships
- Query sub-tickets: `parent:"EPIC-ID"`
- Both types are included in issue details

### Workspaces
- All operations occur within a single Linear workspace
- User must be authenticated to that workspace
- Team and project context filter all operations

## Common Workflows

### Workflow: Fetch Epic with Subtickets
```
1. Call get_issue(epicId) to get epic details
2. Call list_issues(filter: "parent:\"EPIC-ID\"") to get sub-tickets
3. Process each sub-ticket
```

### Workflow: Create Epic with Subtickets
```
1. Create parent issue (epic) with create_issue
2. Get the returned parent ID
3. Create child issues with parentId pointing to epic
4. Optionally add labels, assignees, cycles
```

### Workflow: Search and Analyze Multiple Tickets
```
1. Call list_issues(filter: "team:TEAMID project:\"ProjectName\" ...") with appropriate filters
2. For each issue ID returned, call get_issue to fetch full details
3. Analyze relationships (blocks, blocked-by)
4. Compile findings
```

### Workflow: Propose and Apply Changes
```
1. Fetch existing ticket with get_issue
2. Present proposal to user
3. Use AskUserQuestion tool to get explicit confirmation
4. Call update_issue with changes after user confirms via tool
5. Report what was updated
```

## Error Handling

**Common Error Scenarios**:
- **Project not found**: Verify team prefix and project name in filters
- **Team not found**: Call list_teams to see available teams
- **Issue not found**: Verify issue ID includes correct team prefix
- **Invalid label ID**: Fetch available labels with list_issue_labels before using
- **Insufficient permissions**: Check user role in Linear workspace

**Approach**:
- Always validate team/project context before operations
- Provide specific error messages with remediation steps
- If ambiguous, use AskUserQuestion tool to confirm context before proceeding

## Notes

- All timestamps are ISO 8601 format
- Descriptions support Markdown formatting
- Acceptance criteria should be formatted as checkboxes or Given-When-Then
- Always verify team/project before bulk operations
- For large operations, use AskUserQuestion tool to confirm with user before proceeding
