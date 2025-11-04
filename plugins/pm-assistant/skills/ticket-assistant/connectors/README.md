# PM System Connectors

Connectors implement the interface between generic PM workflows and specific project management systems.

## Adding a New PM System Connector

Each connector must implement the following operations to be compatible with the PM Assistant skill.

### Connector Interface

Every connector file should document and implement these core operations:

#### 1. Discovery: Establish Team and Project Context
- Detect if the project uses this PM system (MCP server, config file, or AskUserQuestion tool)
- Find team/project identifiers
- Retrieve available workspaces, teams, or projects
- Get current user information
- Use AskUserQuestion tool when multiple teams/projects exist

#### 2. Query: Search and Filter Issues
- Implement system-specific query syntax (filters, JQL, GraphQL, etc.)
- Support common filters: team, project, status, assignee
- Support hierarchy queries: parent/epic relationships
- Return paginated results

#### 3. Read: Retrieve Issue Details
- Fetch full issue data (title, description, acceptance criteria, metadata)
- Retrieve relationships (blocks, blocked-by, parent/child, relates-to)
- Get available statuses, labels, cycles/sprints
- Retrieve comments and history

#### 4. Create: New Issues
- Accept ticket data (title, description, labels, assignees, etc.)
- Map generic ticket types (Feature, Bug, Enhancement) to system labels
- Link to parent epic if needed
- Return created issue ID and link

#### 5. Update: Modify Existing Issues
- Accept issue ID and fields to update
- Preserve unchanged fields
- Update relationships (add/remove dependencies)
- Support description, labels, status, assignee changes

#### 6. Comments: Collaboration
- Create comments on issues
- Retrieve comment history

### Connector File Structure

Each connector should be a markdown reference file in `connectors/` with:

1. **System Detection** section
   - How to detect if project uses this system
   - Configuration examples (CLAUDE.md)

2. **Core Operations** section
   - Detailed documentation of each operation
   - API calls or MCP function names
   - Parameters and return values
   - Example workflows

3. **System-Specific Concepts** section
   - Terminology (e.g., Jira "projects" vs Linear "teams")
   - Data model differences
   - Limitations or caveats

4. **Common Workflows** section
   - Fetch epic with sub-tickets
   - Create epic with sub-tickets
   - Search and analyze multiple tickets
   - Propose and apply changes

5. **Error Handling** section
   - Common error scenarios
   - Remediation steps

### Example Connectors

- **linear.md** - Linear MCP server connector (currently implemented)
- **local-markdown.md** - Local markdown files in docs/tickets/ (currently implemented)
  - **local-markdown/setup.md** - Setup instructions
- **jira.md** (future) - Jira Cloud API connector
- **github.md** (future) - GitHub Issues API connector
- **azure-boards.md** (future) - Azure Boards connector

### Using Connectors in SKILL.md

The main skill file should:

1. Detect which PM system is active
2. Load the appropriate connector reference
3. Call the connector's documented operations
4. Use universal patterns from `analysis_patterns.md` regardless of system

Example detection pattern:
```markdown
## PM System Detection and Initialization

1. Check for available MCP servers
2. Check CLAUDE.md for explicit system declaration
3. Use AskUserQuestion tool if ambiguous (see SKILL.md "Using AskUserQuestion for User Input")
4. Load connector reference from `connectors/{system}.md`
```

### Terminology Mapping

Each connector should define how it maps generic PM concepts to its system:

| Generic Concept | Linear | Local-Markdown | Jira | GitHub |
|---|---|---|---|---|
| Team/Project | Team + Project | Implicit in directory | Project + Boards | Organization + Repository |
| Issue Type | Label (Type/*) | Type field | Issue Type | Issue or Discussion |
| Sprint/Cycle | Cycle | (not supported) | Sprint | Milestone |
| Epic/Parent | Parent issue | Parent field | Epic | Milestone/Project v2 |
| Sub-task | Sub-ticket | Parent field | Sub-task | Nested issue (linked) |
| Dependency | Blocks/Blocked-by | Blocks/Blocked-by fields | Link (depends on, blocks) | Link (dependency) |
| Status | State | Status field | Status | State (Open, Closed) |
| Label | Label | Labels array | Label | Label |

## Implementation Notes

- All connectors should support the same analysis patterns (gap analysis, dependency mapping, etc.)
- Connectors should gracefully handle errors specific to their system
- Configuration should be discoverable from both MCP servers and CLAUDE.md files
- Return values should normalize across systems (e.g., all return issue ID + link)

## Testing a New Connector

1. Create the connector reference file with complete documentation
2. Update SKILL.md to support the new system in its detection logic
3. Test detection: Can the skill identify projects using this system?
4. Test operations: Can the skill create, read, update, and query issues?
5. Test with analysis patterns: Do gap analysis, dependency analysis, etc. work?
