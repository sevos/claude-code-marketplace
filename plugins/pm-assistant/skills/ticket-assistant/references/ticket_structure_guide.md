# Ticket Structure and Best Practices

This guide defines how to structure tickets for clarity, completeness, and actionability.

## Ticket Content Standards

**Concise Content**: Maximum 500 words per ticket, ideally 150-200 words.

## Title Guidelines

- **Action-oriented**: Start with clear verbs
- **Specific**: Include what and where, not just "Fix bug" or "Add feature"
- **Under 50 characters**: Concise and scannable
- **Examples**:
  - ✅ "Add CSV export for user data"
  - ✅ "Fix email parser failing on non-ASCII domains"
  - ❌ "Export feature"
  - ❌ "Parser issue"

## Labels and Categorization

Always apply type labels for clarity:
- `Type/Feature` - New functionality
- `Type/Bug` - Defect or broken functionality
- `Type/Enhancement` - Improvement to existing feature
- `Type/Documentation` - Docs, guides, or knowledge base
- `Type/Refactor` - Code cleanup, technical debt
- `Type/Testing` - Test coverage improvements
- `Type/Infrastructure` - Deployment, CI/CD, DevOps

Additional context labels from workspace (if available):
- Priority labels (if defined): High, Medium, Low
- Platform labels: Frontend, Backend, API
- Domain labels: specific to team's structure

## Description Format

Adapt structure based on ticket complexity:

### Simple Tickets (UI changes, text updates, small fixes)

```
Brief context (1-2 sentences):
- What: What needs to change
- Where: Which component/page
- Why: Brief reason if not obvious

Example:
The "Save" button label is inconsistent with other forms.

Change "Save Draft" to "Save" on the user preferences form to match the pattern used across the dashboard.
```

### Complex Tickets (new features, workflows, API changes)

```
## Context
Why this matters (2-3 sentences, can quote user feedback):
- Problem it solves
- User impact
- Business value

## Requirements
Specific, detailed needs (bullet points):
- Functional requirements
- Non-functional requirements (performance, compatibility, etc.)
- Integration points

## Acceptance Criteria
Clear, testable conditions. For complex logic, use Given-When-Then format:

### Given-When-Then Examples:
Given a user is on the email settings page
When they select "Weekly digest"
Then the system saves the preference and shows a confirmation message

### Simple Checkboxes:
- [ ] API endpoint returns 200 status
- [ ] Response includes all required fields
- [ ] Error handling returns 400 for invalid input

## Open Questions
Flag unknowns for relevant parties (Engineering, Product, Business):
- [Engineering] How should we handle authentication for this API?
- [Product] What's the expected behavior for returning users?
- [Business] Do we need audit logging for compliance?
```

### Bug Tickets

Include reproducibility information:

```
## Steps to Reproduce
1. Navigate to email settings
2. Select a date range with special characters
3. Click "Apply"

## Expected Behavior
Settings are saved and confirmed with a message

## Actual Behavior
Page throws a 500 error

## Environment
- Browser: Chrome 120 on macOS
- Device: MacBook Pro
- OS: macOS 14.1
- Network: Stable broadband

## Severity
- Critical: Service down, data loss, security issue
- High: Core feature broken, widespread impact
- Medium: Feature partially broken, workaround exists
- Low: Minor UI issue, edge case, cosmetic
```

## Features vs Bugs

- **Features**: Focus on user need and business value
  - Why does the user need this?
  - What problem does it solve?
  - How does it fit the product roadmap?

- **Bugs**: Focus on reproduction and impact
  - Steps to reproduce (numbered, specific)
  - Expected vs. actual behavior
  - Environment details
  - Severity and workarounds

**Prioritization**: Treat high-severity bugs like features; defer low-severity bugs.

## Acceptance Criteria Best Practices

Make acceptance criteria:
- **Testable**: Can QA or user verify without ambiguity?
- **Specific**: Includes expected data, responses, formats
- **Complete**: Covers happy path and error cases
- **Independent**: Each criterion can be verified separately

### Example: Good vs. Poor

❌ **Poor**: "User can export data"
- Too vague. Export to what format? All data or filtered? Where does the file go?

✅ **Good**:
- [ ] Export button appears in the toolbar
- [ ] Clicking export shows format options (CSV, Excel, JSON)
- [ ] Selected format exports all visible rows
- [ ] File downloads to default downloads folder
- [ ] Exported file contains all columns shown in current view
- [ ] Error handling: Shows message if no data available

## Dependency Management

Explicitly capture ticket relationships:

- **Blocks**: This ticket prevents work on another
  - Use when: "Backend API must be complete before frontend can integrate"
  - Example: Create endpoint (blocks) → Integrate in UI

- **Blocked By**: This ticket is waiting on another
  - Use when: "Frontend work waiting on API design decision"
  - Example: Integrate API (blocked by) → API design decision

- **Relates To**: Related work that should be coordinated but doesn't block
  - Example: Email parser improvements (relates to) → Email formatting standards

## Estimation Guidelines

If team uses estimation:

- **Story points**: Represent relative complexity, not hours
  - 1 point: Simple (UI label, small config)
  - 2-3 points: Straightforward (small feature, isolated fix)
  - 5-8 points: Moderate (feature with dependencies, multiple components)
  - 13+ points: Large (complex feature, needs breakdown)

- **When to split**: Tickets larger than team's typical sprint velocity
  - Examples: 13+ points should usually be split

## Ticket Lifecycle States

Common workflow (adapt to team's actual states):

1. **Backlog**: New, not yet reviewed
2. **Ready for Development**: Refined, detailed, dependencies clear
3. **In Progress**: Work started
4. **In Review**: Awaiting code/product review
5. **Done**: Complete and merged

## Refinement Checklist

Before marking ticket as "Ready for Development":

- [ ] Clear, action-oriented title?
- [ ] Description concise and actionable for developers?
- [ ] Appropriate labels applied?
- [ ] Dependencies identified and linked?
- [ ] Acceptance criteria present (for complex work)?
- [ ] Open questions flagged for relevant parties?
- [ ] Estimate provided (if team uses estimation)?
- [ ] No external blockers?

## Red Flags That Indicate Issues

During review, flag these as needing refinement:

- ❌ Tickets older than 90 days without updates
- ❌ Missing acceptance criteria on complex tickets
- ❌ No clear user value or "why"
- ❌ Acceptance criteria that can't be tested
- ❌ Unclear dependencies or relationships
- ❌ Multiple conflicting acceptance criteria
- ❌ Epic stories with no breakdown
- ❌ Missing error handling or edge cases

## Healthy Backlog Indicators

- Near-term items (next 2 sprints) are detailed and ready
- Long-term items (3+ months) are high-level and strategic
- Dependencies are mapped and clear
- Priorities are current and actionable
- Open questions are flagged for resolution
- No zombie tickets (unchanged for 6+ months)
- Clear epic-to-ticket hierarchy
