# Claude Product Manager Skill

AI-powered Product Owner assistance for ticket management and refinement across multiple project management systems.

## What It Does

When you work with tickets in Linear, GitHub Issues, Local Markdown, or other supported PM systems, this Skill automatically activates to help you:

- **Create tickets** — Draft well-structured tickets with acceptance criteria from conversations
- **Analyze tickets** — Review for completeness, clarity, gaps, and dependencies
- **Propose amendments** — Suggest improvements based on code context or new information
- **Identify gaps** — Find missing coverage when breaking down epics
- **Generate questions** — Create structured refinement session discussion points
- **Plan work** — Suggest parallelization strategies and dependency analysis

## Supported PM Systems

- **Linear** — Full support via Linear MCP server
- **GitHub Issues** — Full support via GitHub CLI (`gh`)
- **Local Markdown** — File-based tickets in `docs/tickets/`
- Future systems (Jira, Azure Boards, etc.) via extensible connector framework

## Setup

### 1. Install the Plugin

This skill is part of the **pm-assistant** plugin available in the Claude Code Plugin Marketplace.

To install, use the marketplace installation command or manually install the plugin from the marketplace.

### 2. Configure Your PM System

**For Linear**:
1. Follow the [Linear MCP documentation](https://linear.app/docs/mcp) to set up the MCP server
2. Authenticate with Linear
3. Add `CLAUDE.md` configuration (see step 3)

**For GitHub Issues**:
1. Install GitHub CLI: https://cli.github.com/ or `brew install gh`
2. Authenticate: `gh auth login`
3. Verify git remote: `git remote get-url origin` (must be a GitHub repository)
4. Add `CLAUDE.md` configuration (see step 3)

**For Local Markdown**:
1. Create tickets directory: `mkdir -p docs/tickets`
2. Initialize counter: `echo "1" > docs/tickets/.ticket_counter`
3. Add `CLAUDE.md` configuration (see step 3)

### 3. Add Project Context (Required)
Create `CLAUDE.md` in your project root to declare which PM system to use:

**Example for Linear**:
```markdown
# CLAUDE.md

## Project Management
- **System**: Linear
- **Team Prefix**: PROD
- **Project**: Backend Services
```

**Example for GitHub Issues**:
```markdown
# CLAUDE.md

## Project Management
- **System**: GitHub-Issues
```
Note: Repository is auto-detected from git remote origin.

**Example for Local Markdown**:
```markdown
# CLAUDE.md

## Project Management
- **System**: Local-Markdown
- **Directory**: docs/tickets
```

The skill will use these settings for all operations in the project.

## How to Use

Simply describe what you need with tickets. The Skill activates automatically and works with your configured PM system:

```
Review the tickets for this sprint and identify any gaps

Create a ticket for implementing dark mode with acceptance criteria

What are the dependencies between PROD-100 and PROD-110?

Generate questions for our refinement session on the payment feature

Suggest improvements to this epic based on the code review
```

The Skill will:
1. Fetch relevant tickets from your PM system (Linear, GitHub Issues, or Local Markdown)
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

✅ **Extensible architecture** — PM system-specific code isolated in connectors; supports Linear, GitHub Issues, and Local Markdown
✅ **Always proposes before acting** — Shows changes for your review
✅ **Requires explicit confirmation** — Never assumes approval
✅ **Specific and quoted** — References exact text when identifying issues
✅ **Explains rationale** — Shows why changes matter
✅ **Reusable patterns** — Analysis and refinement workflows system-agnostic

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not activating | Explicitly ask: "Use the product-manager skill to review these tickets..." |
| Team/project not found (Linear) | Add `CLAUDE.md` file with Linear team and project (see Setup step 3) |
| Can't find tickets (Linear) | Verify Linear is configured correctly in CLAUDE.md and MCP server is authenticated |
| Repository not detected (GitHub) | Verify git remote origin exists and is a GitHub URL: `git remote get-url origin` |
| `gh` command not found (GitHub) | Install GitHub CLI: https://cli.github.com/ or `brew install gh` |
| Not authenticated (GitHub) | Run `gh auth login` to authenticate with GitHub |
| Tickets directory not found (Local Markdown) | Create directory specified in CLAUDE.md: `mkdir -p docs/tickets` |
| System not declared | Add `CLAUDE.md` with `System` field set to Linear, GitHub-Issues, or Local-Markdown |

---

See **SKILL.md** for comprehensive documentation and workflow examples.
