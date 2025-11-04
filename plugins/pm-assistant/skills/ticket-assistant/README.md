# Claude Ticket Assistant Skill

AI-powered Product Owner assistance for ticket management and refinement across multiple project management systems.

## What It Does

When you work with tickets in Linear, Jira, GitHub Issues, or other supported PM systems, this Skill automatically activates to help you:

- **Create tickets** — Draft well-structured tickets with acceptance criteria from conversations
- **Analyze tickets** — Review for completeness, clarity, gaps, and dependencies
- **Propose amendments** — Suggest improvements based on code context or new information
- **Identify gaps** — Find missing coverage when breaking down epics
- **Generate questions** — Create structured refinement session discussion points
- **Plan work** — Suggest parallelization strategies and dependency analysis

## Supported PM Systems

- **Linear** (fully supported)
- Future systems (Jira, GitHub Issues, Azure Boards, etc.) via extensible connector framework

## Setup

### 1. Install the Plugin

This skill is part of the **pm-assistant** plugin available in the Claude Code Plugin Marketplace.

To install, use the marketplace installation command or manually install the plugin from the marketplace.

### 2. Configure Your PM System

**For Linear**:
Follow the [Linear MCP documentation](https://linear.app/docs/mcp) to set up the MCP server and authenticate with Linear.

**For other systems**:
Follow the appropriate MCP or API documentation for your PM system (Jira, GitHub, etc.).

### 3. Add Project Context (Recommended)
Create `CLAUDE.md` in your project root to establish default PM system and project context:

**Example for Linear**:
```markdown
# CLAUDE.md

## Project Management
- **System**: Linear
- **Team Prefix**: PROD
- **Project**: Backend Services
```

The skill will use these settings for all operations in the project.

## How to Use

Simply describe what you need with Linear tickets. The Skill activates automatically:

```
Review the tickets for this sprint and identify any gaps

Create a ticket for implementing dark mode with acceptance criteria

What are the dependencies between PROD-100 and PROD-110?

Generate questions for our refinement session on the payment feature

Suggest improvements to this epic based on the code review
```

The Skill will:
1. Fetch relevant tickets from Linear
2. Analyze them using proven patterns
3. Present findings or proposals for review
4. **Wait for your explicit confirmation** before making changes
5. Apply updates and report results

## Documentation

- **SKILL.md** — Complete workflow guide and patterns
- **assets/ticket_template.md** — Ready-to-use templates
- **references/ticket_structure_guide.md** — Quality standards (system-agnostic)
- **references/analysis_patterns.md** — Six analysis workflows with examples
- **references/refinement_session_guide.md** — Refinement best practices
- **connectors/linear.md** — Linear MCP API reference and operations
- **connectors/local-markdown.md** — Local Markdown connector documentation
  - **connectors/local-markdown/setup.md** — Setup instructions for local markdown
- **connectors/README.md** — Connector interface and extensibility guide

## Key Principles

✅ **Extensible architecture** — Linear-specific code isolated in connectors; ready for Jira, GitHub, etc. in future
✅ **Always proposes before acting** — Shows changes for your review
✅ **Requires explicit confirmation** — Never assumes approval
✅ **Specific and quoted** — References exact text when identifying issues
✅ **Explains rationale** — Shows why changes matter
✅ **Reusable patterns** — Analysis and refinement workflows system-agnostic

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not activating | Explicitly ask: "Use the ticket-assistant skill to review these tickets..." |
| Team/project not found | Add a `CLAUDE.md` file with Linear team and project (see Setup step 3) |
| Can't find tickets | Verify Linear is configured correctly in CLAUDE.md and MCP server is authenticated |

---

See **SKILL.md** for comprehensive documentation and workflow examples.
