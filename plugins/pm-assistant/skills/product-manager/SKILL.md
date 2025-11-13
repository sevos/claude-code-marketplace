---
name: product-manager
description: Product Owner assistance for ticket refinement, epic breakdown, dependency analysis, and backlog management. Use this skill when shaping tickets, analyzing quality, identifying gaps, or generating refinement questions. For ticket data operations (get, list, create, update), the skill delegates to the ticket-assistant agent which supports Linear, Local Markdown, and GitHub Issues.
---

# Product Manager Skill

## Overview

This skill enables Product Owner workflows focused on **ticket shaping, structure, and best practices**:
- Refine tickets with proper structure and acceptance criteria
- Analyze tickets for gaps, clarity, completeness, and dependencies
- Break down epics into actionable sub-tickets
- Generate meaningful refinement session questions
- Propose amendments based on conversation context

**Ticket Data Operations**: All ticket access and manipulation (get, list, create, update) is delegated to the **ticket-assistant agent**, which handles Linear MCP, Local Markdown, and GitHub Issues operations.

## Architecture

```
User Request
     ↓
product-manager SKILL (shaping/best practices/analysis)
     ↓ (delegates data operations)
ticket-assistant AGENT (Linear MCP / Local Markdown / GitHub CLI CRUD)
     ↓
[Linear MCP] or [Markdown Files] or [GitHub CLI]
```

## Core Capabilities

### 1. Create Tickets from Conversation

**Scenario**: "Create a ticket for this feature with acceptance criteria" or "Based on the conversation transcript create epic with tickets/ticket"

**Process**:
1. Extract requirements from conversation context
2. Use ticket template from `assets/ticket_template.md`
3. Structure as simple or complex ticket based on scope
4. Apply appropriate type labels (Feature, Bug, Enhancement, etc.)
5. Present proposal to user for review
6. **Use AskUserQuestion tool for confirmation**: Wait for explicit approval before proceeding
7. **After user confirms**: Delegate to ticket-assistant agent to create ticket
8. Report created ticket with ID and link

**Guidelines**:
- Refer to `references/ticket_structure_guide.md` for formatting standards
- Include acceptance criteria for complex work
- Flag open questions when scope is unclear
- Suggest dependencies if work relates to existing tickets
- **Content focus**: Extract user needs and business value; avoid code snippets
- **Include technical details when**:
  - Explicitly instructed to include them
  - Deviating from standard conventions or patterns
  - Non-standard approach requires documentation
  - Critical technical constraints that impact implementation

### 2. Propose Ticket Amendments

**Scenario**: "Are there any wrong assumptions in the ticket?" or "Based on the conversation transcript suggest adjustments to epic XXX-123"

**Process**:
1. Delegate to ticket-assistant agent to fetch existing ticket/epic
2. Analyze current state (description, acceptance criteria, scope)
3. Cross-reference with provided context (code, conversation, etc.)
4. Use patterns from `references/analysis_patterns.md` to identify:
   - Assumption mismatches
   - Scope gaps or overreach
   - Missing edge cases or error handling
   - Outdated requirements
5. Present proposed changes:
   - "Current state" (quote from ticket)
   - "Suggested changes" (with rationale)
   - "Questions for team" (if needed)
6. **Use AskUserQuestion tool for confirmation**: Wait for explicit approval before proceeding
7. **After user confirms**: Delegate to ticket-assistant agent to update ticket
8. Report changes applied

**Guidelines**:
- Be specific: quote the problematic text
- Explain the "why" behind each suggested change
- Distinguish between critical (must fix) and nice-to-have improvements
- Use AskUserQuestion tool if context is ambiguous or requires clarification

### 3. Analyze Tickets for Quality

**Scenario**: "Review existing Linear tickets for completeness, clarity, dependencies, open questions" for range AIA-100 through AIA-110

**Process**:
1. Delegate to ticket-assistant agent to fetch tickets in range
2. For each ticket, evaluate against criteria:
   - **Clarity**: Title, description, acceptance criteria
   - **Completeness**: All required fields, edge cases covered
   - **Dependencies**: Blocks/Blocked-by relationships identified
   - **Open questions**: Uncertainties flagged
3. Use `references/analysis_patterns.md` Pattern 4 for systematic evaluation
4. Compile findings:
   - Strong tickets (ready for development)
   - Needs work (specific improvements recommended)
   - Needs breakdown (too large)
   - Blocked (waiting on decisions)
5. Present report with:
   - Summary per ticket
   - Recommended actions
   - Highest-priority refinements needed

**Guidelines**:
- Use consistent evaluation structure
- Highlight both strengths and issues
- Provide specific, actionable recommendations
- Flag patterns across multiple tickets (e.g., all missing error handling)

### 4. Identify Gaps in Epic Coverage

**Scenario**: "Identify gaps in the planned tickets for epic XXX-123"

**Process**:
1. Delegate to ticket-assistant agent to fetch epic and sub-tickets
2. Analyze epic scope vs. ticket coverage using `references/analysis_patterns.md` Pattern 1:
   - Frontend/UI components
   - Backend services and APIs
   - Testing and QA work
   - Documentation and knowledge base
   - Deployment or infrastructure
   - Edge cases and error scenarios
3. Present findings:
   - Identified gaps with context
   - Suggested new tickets for each gap
   - Estimated scope per gap
4. **Use AskUserQuestion tool for confirmation**: Present options to create all tickets, select specific ones, or review proposals first
5. **After user confirms**: Delegate to ticket-assistant agent to create tickets

**Guidelines**:
- Be thorough but realistic (not everything needs a separate ticket)
- Group related gaps (e.g., multiple API endpoints in one ticket)
- Consider team's estimation approach when scoping gaps
- Link new tickets to epic as subtickets

### 5. Analyze Dependencies and Suggest Parallelization

**Scenario**: User asks about dependencies between tickets or how to parallelize work

**Process**:
1. Delegate to ticket-assistant agent to fetch relevant tickets
2. Use `references/analysis_patterns.md` Pattern 3:
   - Extract explicit Blocks/Blocked-by relationships
   - Identify implicit dependencies
   - Find critical path (work that must complete first)
   - Group by parallelizable tracks
3. Present parallelization strategy:
   - Work that can happen simultaneously
   - Critical path dependencies
   - Recommended team allocation
4. Suggest implementation sequence

**Guidelines**:
- Consider frontend/backend can often run in parallel if API contract is clear
- Testing can often run alongside implementation if setup is clear
- Documentation can start early with skeleton/outline
- Infrastructure work often critical path

### 6. Generate Refinement Session Questions

**Scenario**: "Generate questions for the next refinement session for tickets XXX-100 through XXX-110"

**Process**:
1. Delegate to ticket-assistant agent to fetch ticket range
2. Analyze each ticket for uncertainty patterns:
   - Missing acceptance criteria
   - Ambiguous requirements
   - Unknown trade-offs
   - Implicit assumptions
   - Unclear edge cases
3. Use `references/refinement_session_guide.md` and `references/analysis_patterns.md` Pattern 5
4. Generate questions organized by:
   - **Critical blockers**: Must resolve first
   - **Design/Technical questions**: Needed before building
   - **Edge cases**: Clarify completeness
   - **Dependencies**: Identify coordination needs
   - **Success metrics**: Define what "done" means
5. Present as structured question set with:
   - Target audience (Product, Engineering, Design)
   - Why the question matters
   - Suggested answers or options

**Guidelines**:
- Prioritize high-impact questions first
- Frame as open-ended (not leading)
- Group related questions by theme
- Note interdependencies between questions
- Suggest time-boxing for discussion

## Reference Materials

### Ticket Structure and Templates
- **`references/ticket_structure_guide.md`** - Title guidelines, label categories, description formats, acceptance criteria best practices, refinement checklist, red flags
- **`assets/ticket_template.md`** - Ready-to-use templates for simple/complex/bug/epic tickets

### Analysis Patterns
- **`references/analysis_patterns.md`** - 6 structured reasoning patterns:
  1. Identifying gaps in epic coverage
  2. Detecting assumption mismatches
  3. Dependency analysis and parallelization
  4. Clarity and completeness review
  5. Generating refinement session questions
  6. Epic analysis and adjustment suggestions

### Refinement Sessions
- **`references/refinement_session_guide.md`** - Question generation strategies, facilitation tips, sample agendas, post-refinement checklist

### When to Use Each Analysis Pattern

| Pattern | Trigger Question | Reference |
|---------|------------------|-----------|
| Gap Identification | "Identify gaps in epic XXX" | `analysis_patterns.md` Pattern 1 |
| Assumption Mismatch | "Are there wrong assumptions?" | `analysis_patterns.md` Pattern 2 |
| Dependency Analysis | "What are dependencies?" | `analysis_patterns.md` Pattern 3 |
| Quality Review | "Review tickets for completeness" | `analysis_patterns.md` Pattern 4 |
| Refinement Questions | "Generate questions for session" | `analysis_patterns.md` Pattern 5, `refinement_session_guide.md` |
| Epic Adjustment | "Suggest adjustments to epic" | `analysis_patterns.md` Pattern 6 |

## Workflow: Create and Propose

All creation and amendment operations follow this pattern:

### Step 1: Gather Context
- User provides requirements (conversation, transcript, existing ticket)
- If ticket data is needed, delegate to ticket-assistant agent

### Step 2: Analyze and Draft
- Use appropriate patterns from `references/analysis_patterns.md`
- Follow structure from `references/ticket_structure_guide.md` or templates
- Draft ticket/amendment with complete context

### Step 3: Present for Review
- Show "current state" and "proposed state" for amendments
- Show "proposed ticket" for new tickets
- Include rationale for each decision
- Use AskUserQuestion tool if clarification is needed

### Step 4: Wait for Confirmation
- **Use AskUserQuestion tool** to get explicit user confirmation before proceeding
- **Do not proceed** until user confirms via the tool response
- Offer to adjust draft if user suggests changes
- Re-present adjusted version and confirm again using AskUserQuestion

### Step 5: Apply Changes
- Delegate to ticket-assistant agent to create/update tickets
- Agent handles all PM system-specific operations

### Step 6: Report Results
- Confirm what was created/updated
- Provide ticket ID and Link (if available)
- Ask: "What would you like to do next?"

## Best Practices

### Ticket Quality
- Read `references/ticket_structure_guide.md` for quality standards
- Ensure titles are specific and action-oriented
- Include acceptance criteria for complex work
- Flag open questions when scope is unclear
- Link dependencies explicitly

### Analysis Completeness
- Quote specific text when identifying issues
- Explain the "why" behind recommendations
- Distinguish between facts (what's written) and inferences
- Flag assumptions clearly
- Suggest options with trade-offs when multiple paths exist

### User Confirmation Protocol
- Always show proposals before applying
- **Use AskUserQuestion tool** to get explicit user confirmation with clear options
- Wait for confirmation response from the tool before proceeding
- Never assume approval
- Offer revision if user suggests changes
- Re-present for approval after revisions (using AskUserQuestion again)

### Delegating to Agent
- Use ticket-assistant agent for all data operations (get, list, create, update, search)
- Agent handles PM system detection and operations
- Focus skill logic on analysis, shaping, and best practices

## Using AskUserQuestion for User Input

When user input is required during workflow execution, use the **AskUserQuestion** tool to present structured options. This ensures clear, actionable choices and reduces ambiguity.

### When to Use AskUserQuestion

Use the tool for:
1. **Clarifying questions during analysis** - When requirements, scope, or context needs clarification
2. **Confirmation before actions** - Before creating or updating tickets in the PM system

Do NOT use for:
- Open-ended conversational follow-ups ("What would you like to do next?")
- Refinement session questions (those are for human facilitators)

### Example 1: Clarifying Requirements During Analysis

**Scenario**: Analyzing a ticket but scope is ambiguous between two interpretations.

```
Use AskUserQuestion tool with:
{
  "questions": [{
    "question": "The ticket mentions 'email notifications' but doesn't specify the scope. What should be included?",
    "header": "Scope",
    "multiSelect": true,
    "options": [
      {
        "label": "Digest emails",
        "description": "Scheduled summary emails sent daily/weekly"
      },
      {
        "label": "Real-time notifications",
        "description": "Immediate emails when events occur"
      },
      {
        "label": "Transactional emails",
        "description": "System-triggered emails (password reset, confirmations)"
      }
    ]
  }]
}
```

### Example 2: Confirming Before Creating Tickets

**Scenario**: Identified 3 gaps in epic coverage, ready to create tickets.

```
Use AskUserQuestion tool with:
{
  "questions": [{
    "question": "I've identified 3 missing tickets for the email digest epic. Should I create them?",
    "header": "Create Tickets",
    "multiSelect": false,
    "options": [
      {
        "label": "Create all 3 tickets",
        "description": "Create tickets for: UI preferences component, end-to-end testing, and scheduled job setup"
      },
      {
        "label": "Show me the proposals first",
        "description": "Present detailed ticket proposals for review before creating"
      },
      {
        "label": "Create only high-priority ones",
        "description": "Create tickets for UI component and testing, defer infrastructure work"
      }
    ]
  }]
}
```

### Guidelines for Effective Questions

**Structure**:
- Use clear, specific question text
- Provide 2-4 options (not just yes/no when possible)
- Include descriptions explaining what each option means
- Use `multiSelect: true` only when choices are not mutually exclusive

**Headers**:
- Keep short (max 12 chars): "Scope", "Approach", "Confirm", "Priority"
- Describes the decision type

**Options**:
- Label: Concise choice (1-5 words)
- Description: Explain implications or what happens if chosen

## Directory Structure

```
plugins/pm-assistant/skills/ticket-assistant/
├── SKILL.md                           # This file
├── README.md                          # User-facing documentation
├── assets/
│   └── ticket_template.md             # Ticket templates
├── references/                        # Domain knowledge
│   ├── ticket_structure_guide.md      # Ticket quality standards
│   ├── analysis_patterns.md           # Analysis methodologies
│   └── refinement_session_guide.md    # Refinement facilitation
└── connectors/                        # PM system reference (optional)
    └── linear.md                      # Linear MCP quick reference (if needed)
```

## Notes

- Maximum 500 words per ticket (concise content)
- All timestamps use ISO 8601 format
- Descriptions support Markdown formatting
- Always delegate ticket data operations to ticket-assistant agent
- Focus on analysis, shaping, and best practices in this skill
