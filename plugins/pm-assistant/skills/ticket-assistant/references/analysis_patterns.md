# Ticket and Epic Analysis Patterns

This guide provides structured approaches for analyzing tickets and epics using LLM reasoning.

## Overview

Analysis tasks leverage LLM reasoning to:
- Identify gaps and missing tickets
- Detect mismatches between ticket assumptions and code reality
- Find dependencies and relationships
- Evaluate ticket clarity and completeness
- Generate thoughtful refinement questions

## Pattern 1: Identifying Gaps in Epic Coverage

**Scenario**: User wants to identify missing tickets for an epic (e.g., "Identify gaps in epic XXX-123").

### Process

1. **Fetch the epic**:
   - Get the epic issue to understand scope, description, acceptance criteria
   - Parse the epic's stated goals and requirements

2. **Fetch all subtickets**:
   - Query: `parent:"EPIC-ID"`
   - List all child tickets
   - Map coverage: which parts of the epic have tickets?

3. **Analyze coverage**:
   - Compare epic description against existing tickets
   - Identify missing areas:
     - Frontend/UI components not covered
     - Backend services or APIs not covered
     - Testing or QA work not covered
     - Documentation or knowledge base gaps
     - Deployment or infrastructure work not covered
   - Look for edge cases or error scenarios

4. **Present findings**:
   - List identified gaps with context
   - Suggest new tickets for uncovered work
   - Include estimated scope for each gap

### Example Analysis Structure

**Epic**: "Implement email digest feature"

**Current tickets**:
- AIA-100: Design email digest schema
- AIA-101: Build digest generation API
- AIA-102: Create email templates

**Identified gaps**:
- [ ] UI component: Digest frequency preferences (suggested: 2-3 points)
- [ ] Testing: End-to-end digest flow with real email delivery
- [ ] Documentation: Digest API documentation and examples
- [ ] Infrastructure: Set up scheduled job for digest generation (cron/task queue)

## Pattern 2: Detecting Assumption Mismatches

**Scenario**: User asks "Are there any wrong assumptions in this ticket?" (often comparing ticket description to actual code implementation).

### Process

1. **Extract assumptions from ticket**:
   - Read ticket description, acceptance criteria, requirements
   - Identify explicit assumptions:
     - "API returns JSON array"
     - "User already authenticated"
     - "Database table exists with these fields"
   - Identify implicit assumptions:
     - "Feature X is already implemented"
     - "Libraries are available in codebase"
     - "System can handle concurrent requests"

2. **Cross-reference with provided context**:
   - User may provide code snippets, implementation details, or codebase structure
   - Compare assumptions against actual state
   - Identify mismatches:
     - API returns different format
     - Prerequisites not yet implemented
     - Different database schema
     - Performance constraints
     - Library incompatibilities

3. **Categorize mismatches**:
   - **Critical**: Breaks implementation (e.g., "API structure wrong")
   - **High**: Requires significant rework (e.g., "Missing prerequisite")
   - **Medium**: Needs clarification or small adjustment
   - **Low**: Minor edge case or optimization

4. **Present findings with remediation**:
   - Flag each mismatch clearly
   - Explain impact on implementation
   - Suggest updated acceptance criteria or requirements
   - Use AskUserQuestion tool to confirm: "Should we update the ticket or is there missing context?"

### Example Mismatch Detection

**Ticket assumption**: "Email parser API returns structured fields: { sender, subject, body, attachments }"

**Code reality**: "Parser returns raw MIME structure; field extraction not yet implemented"

**Mismatch**: Critical
- Ticket describes endpoint as done; actually needs field extraction layer
- Acceptance criteria unrealistic for current implementation
- **Suggested fix**: Split into (1) MIME parsing, (2) field extraction, (3) API endpoint

## Pattern 3: Dependency Analysis and Parallelization

**Scenario**: User wants to understand dependencies across tickets for parallel work.

### Process

1. **Extract dependencies from ticket relationships**:
   - Review Blocks/Blocked-by relationships
   - Look for implicit dependencies:
     - "Requires backend API" → ticket mentions API endpoint
     - "Needs database migration" → schema changes
     - "Depends on design decision" → tickets waiting on decisions

2. **Identify critical path**:
   - Work that must complete before others can start
   - Usually: design → backend → frontend → testing

3. **Group by parallelizable tracks**:
   - Frontend UI work (if API contract defined)
   - Backend API implementation
   - Testing and QA scenarios
   - Documentation and knowledge base
   - Infrastructure/deployment work

4. **Suggest optimal sequence**:
   - Propose which work can happen in parallel
   - Identify blockers that must resolve first
   - Recommend team allocation to maximize parallelization

### Example Parallelization

**Tickets for feature**: Email digest feature (AIA-100 to AIA-105)

**Analysis**:
- AIA-100 (Design schema) - critical path start
- AIA-101 (Backend API) - depends on AIA-100 ✓ can start after design
- AIA-102 (Email templates) - independent ✓ can start immediately
- AIA-103 (Frontend UI) - depends on AIA-101 API contract
- AIA-104 (Testing) - depends on AIA-101 being runnable
- AIA-105 (Documentation) - can start after AIA-100

**Suggested parallelization**:
1. **Start simultaneously**: AIA-100 (design), AIA-102 (templates)
2. **Once AIA-100 done**: Start AIA-101 (backend), AIA-105 (docs)
3. **Once AIA-101 done**: Start AIA-103 (frontend), AIA-104 (testing)

## Pattern 4: Clarity and Completeness Review

**Scenario**: User asks "Review existing Linear tickets for completeness, clarity, dependencies, open questions" for a range of tickets.

### Process

1. **Fetch all tickets** in the specified range (e.g., AIA-100 through AIA-110)

2. **Evaluate each ticket against criteria**:

   **Clarity Assessment**:
   - Is title specific and action-oriented?
   - Is description concise and understandable?
   - Are acceptance criteria testable and specific?
   - Would a developer confidently estimate and implement?

   **Completeness Check**:
   - Does complex ticket have acceptance criteria?
   - Are bugs reproducible (steps provided)?
   - Are features properly scoped?
   - Are dependencies identified?
   - Are open questions flagged?

   **Dependency Verification**:
   - Are blocking relationships explicitly set?
   - Could work run in parallel if clearer?
   - Are implicit dependencies made explicit?

   **Open Questions Assessment**:
   - Are uncertainties flagged?
   - Are questions assignable to right parties?

3. **Compile findings**:
   - Create summary per ticket
   - Highlight strengths and issues
   - Rank by urgency of refinement needed

4. **Present with recommendations**:
   - Strong tickets (ready for development)
   - Needs clarity (specific improvements recommended)
   - Needs breakdown (too large or complex)
   - Blocked by decisions (needs input from product/design)

### Evaluation Template

For each ticket, assess:

```
Ticket: AIA-XXX - [Title]
Status: [Ready/Needs Work/Blocked]

Clarity: [✓/⚠/✗] with reason
Completeness: [✓/⚠/✗] with reason
Dependencies: [✓/⚠/✗] with reason
Questions: [✓/⚠/✗] with reason

Issues found:
- [Issue 1 with recommendation]

Recommended next step:
- [Action needed]
```

## Pattern 5: Generating Refinement Session Questions

**Scenario**: User asks "Generate questions for the next refinement session for tickets XXX-100 through XXX-110".

### Process

1. **Fetch tickets** in the range

2. **Identify uncertainty patterns**:
   - Missing acceptance criteria
   - Ambiguous requirements
   - Conflicting specs
   - Implicit assumptions
   - Unknown edge cases
   - Unclear priorities or value

3. **Generate clarifying questions** organized by type:

   **For Product/Business**:
   - "What's the priority of this feature relative to X?"
   - "Who is the primary user and what problem does this solve?"
   - "What's the expected timeline/deadline?"
   - "Are there any compliance or regulatory requirements?"

   **For Engineering**:
   - "Is this technically feasible with current stack?"
   - "Are there performance constraints we should consider?"
   - "Does this require changes to authentication/authorization?"
   - "What's the rollout strategy (feature flag, gradual, etc.)?"

   **For Design/UX**:
   - "Have we designed the user flows for this?"
   - "Are there accessibility requirements?"
   - "What's the visual/interaction pattern from existing UI?"

   **For All**:
   - "How does this integrate with existing feature X?"
   - "What happens in error scenarios?"
   - "What's the success metric for this?"

4. **Organize questions strategically**:
   - Start with high-impact, blockers
   - Group by theme or epic
   - Flag critical unknowns
   - Note dependencies between questions

### Example Question Set

**For epic "Email digest feature" refinement session**:

**Critical blockers** (must resolve first):
- [Product] Is the digest frequency (daily/weekly/monthly) configurable per user or system-wide?
- [Engineering] Can our email system handle the volume of digest sends? Should we batch them?

**Design questions** (needed before building):
- [Design] Have we designed the digest preview UI?
- [All] What unsubscribe mechanism do we need for digests?

**Edge cases** (clarify before acceptance):
- [Product] What happens if a user has no emails in the digest period?
- [Engineering] How do we handle timezone differences for "weekly" digests?

## Pattern 6: Epic Analysis and Adjustment Suggestions

**Scenario**: User wants "Based on the conversation transcript suggest adjustments to the epic XXX-123".

### Process

1. **Fetch the epic** with full description and current subtickets

2. **Analyze conversation transcript** for:
   - New insights or requirements not in epic description
   - Stakeholder concerns or constraints
   - Changed priorities or scope
   - Technical challenges or trade-offs discussed
   - User feedback or use cases mentioned

3. **Cross-reference with current epic**:
   - What's aligned between epic description and conversation?
   - What's missing from epic description?
   - What's in epic that wasn't discussed or is outdated?
   - Are subtickets still appropriate?

4. **Suggest adjustments**:
   - Update epic description with new context
   - Recommend new tickets for discussion outcomes
   - Suggest removing or deferring scope
   - Highlight dependencies discovered in discussion
   - Flag trade-offs for decision

5. **Present as proposed amendments**:
   - "Current epic description" vs. "Suggested updates"
   - "Current subtickets" vs. "Suggested changes"
   - Rationale for each change

### Amendment Template

```
Epic: XXX-123 - [Current Title]

Current scope: [quote from description]

Suggested scope updates:
- Add: [new requirement or insight]
- Remove: [scope to defer]
- Clarify: [ambiguous part with suggested rewording]

New subtickets suggested:
- [Ticket with estimated scope]

Subtickets to reconsider:
- [Ticket that may no longer fit]

Dependencies or blockers discovered:
- [Dependency or constraint]
```

## General Analysis Guidelines

**Always**:
- Quote specific text from tickets/epics in findings
- Provide specific, actionable recommendations
- Explain the "why" behind observations
- Distinguish between facts (what's written) and inferences (what's implied)
- Flag assumptions clearly

**Consider**:
- Team's estimation approach (story points, t-shirt, none)
- Sprint velocity and capacity
- Current backlog health and priorities
- Existing patterns in ticket structure (to match style)

**When unsure**:
- Use AskUserQuestion tool for clarifying questions
- Flag as open question for refinement
- Suggest options with trade-offs
- Don't assume team preferences or standards
