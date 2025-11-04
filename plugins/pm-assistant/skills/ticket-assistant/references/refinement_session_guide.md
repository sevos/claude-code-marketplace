# Refinement Session Guide

This guide explains how to prepare for and facilitate refinement sessions, including generating meaningful discussion questions.

## Refinement Session Overview

Refinement sessions are where product teams:
- Discuss upcoming work (next 2-3 sprints)
- Break down epics into actionable tickets
- Clarify requirements and acceptance criteria
- Identify dependencies and blockers
- Estimate complexity (if using estimation)
- Align on priorities

## Pre-Refinement: Generating Questions

**Scenario**: "Generate questions for the next refinement session for tickets XXX-100 through XXX-110"

### Question Generation Strategy

Generate questions that:
1. **Unblock implementation** - Remove technical uncertainties
2. **Clarify value** - Ensure everyone understands the "why"
3. **Surface dependencies** - Identify work that affects other work
4. **Challenge assumptions** - Find gaps in thinking
5. **Enable estimation** - Provide clarity for sizing complexity

### Question Categories and Examples

#### 1. Scope and Value Questions

**Product/Business focus**:
- "What's the primary user need this solves?"
- "Why now? What drives the priority?"
- "How does this relate to our OKRs?"
- "What's the definition of success?"
- "Who should we talk to validate this with users?"

**When to use**: For new features, roadmap items, or items with unclear "why"

#### 2. Technical Feasibility Questions

**Engineering focus**:
- "Is our current tech stack a good fit for this?"
- "Are there performance or scalability concerns?"
- "Do we need new infrastructure or tooling?"
- "Is this technically feasible in the next sprint?"
- "What technical debt might block this?"

**When to use**: Complex features, infrastructure work, new integrations

#### 3. Design and UX Questions

**Design focus**:
- "Have we designed this user flow?"
- "Are there accessibility requirements?"
- "How does this fit our existing design system?"
- "What's the mobile experience like?"
- "Should we prototype or validate first?"

**When to use**: Customer-facing features, UI changes

#### 4. Dependency and Integration Questions

**Cross-functional**:
- "Does this depend on other work in progress?"
- "Could this block other teams or projects?"
- "Does this integrate with [system X]? How?"
- "What APIs or data do we need from [team Y]?"
- "What's the integration test strategy?"

**When to use**: Any feature involving multiple systems, teams, or components

#### 5. Edge Cases and Error Handling

**Completeness focus**:
- "What happens if [error scenario]?"
- "How do we handle concurrent requests?"
- "What's the rollback strategy if things go wrong?"
- "Are there rate limits or capacity considerations?"
- "What about inactive/deleted users/data?"

**When to use**: Critical systems, features affecting data integrity, payment/security

#### 6. Decision-Required Questions

**Flag blockers**:
- "Do we need a design decision before starting?"
- "Should we do [approach A] or [approach B]? What are the trade-offs?"
- "Is this a platform-wide change requiring architectural decision?"
- "Should we spike this first to reduce uncertainty?"

**When to use**: Items with multiple paths forward or architectural implications

#### 7. Rollout and Deployment Questions

**Operations focus**:
- "Should this go behind a feature flag?"
- "How do we roll this out without impacting users?"
- "What monitoring/alerts do we need?"
- "Is there a canary/gradual rollout strategy?"
- "What's the rollback procedure?"

**When to use**: User-facing changes, infrastructure changes, high-impact work

### Question Framing for Different Audiences

**For Engineering-heavy sessions**:
- Focus on technical feasibility and dependencies
- Include spike/investigation questions
- Address edge cases and error scenarios
- Discuss performance and testing implications

**For Product-heavy sessions**:
- Emphasize user value and success metrics
- Clarify scope and priorities
- Discuss trade-offs between features
- Identify missing user research or validation

**For Cross-functional sessions**:
- Start with "why" (value and goals)
- Surface dependencies early
- Identify design/technical gaps
- End with "what's next" (work plan)

## Sample Refinement Question Sets

### Example 1: New Feature (Email Digest)

```
**Value & Scope**:
- What problem does email digest solve for users?
- Who's the primary user? What's their current workflow?
- Should frequency be configurable per user or system-wide?

**Technical**:
- Can our email system handle batch sending this volume?
- Should we use a background job or scheduled task?
- What email format (HTML/plain text/both)?

**Edge Cases**:
- What if user has no emails in the period?
- How do we handle timezone differences?
- Unsubscribe mechanism?

**Dependencies**:
- Does this block or depend on other email features?
- Do we need design approval before building?

**Success**:
- How do we measure if this succeeds?
- What's the rollout timeline?
```

### Example 2: Bug Fix (Parser Failing on Special Characters)

```
**Clarification**:
- What's the impact? How many users affected?
- Which special characters cause failures?
- Is this a security issue or just a UX problem?

**Root Cause**:
- Have we root-caused this?
- Is it encoding, parsing, or validation?

**Solution Scope**:
- Should we fix just these characters or handle all UTF-8?
- Do we need to update error messages?
- Should we add input validation on the frontend?

**Testing**:
- What test cases should we add?
- How do we prevent regression?

**Rollout**:
- Is this a hotfix or can we batch with other parser work?
- Do we need to handle existing data that's affected?
```

### Example 3: Infrastructure Work (Database Migration)

```
**Why and When**:
- Why do we need this migration now?
- What's the impact of not doing it?
- Is this blocking feature work?

**Approach**:
- What's the migration strategy (zero-downtime? maintenance window?)?
- Do we need a feature flag or gradual rollout?
- What's the rollback plan?

**Scope**:
- Affected tables and data volumes?
- Performance impact?
- Monitoring and alerting?

**Dependencies**:
- Deployment sequence with other work?
- Do other teams need to prepare?

**Communication**:
- Do users need notification?
- What's the customer-facing impact?
```

## During Refinement: Using Questions to Guide Discussion

### Facilitation Tips

**Opening** (set context):
- "We're refining the next 2 sprints' work"
- "Goal is to clarify scope, surface unknowns, and identify dependencies"
- "It's okay if we don't have all answers—we'll capture questions for resolution"

**Present the work** (overview):
- Share epic or feature theme
- Briefly describe what we're working on
- Set the context for why now

**Ask clarifying questions** (engagement):
- Start with scope and value: "What problem does this solve?"
- Move to feasibility: "Is this technically doable?"
- Explore details: "What about edge case X?"
- Flag unknowns: "Do we need design input on this?"

**Capture decisions** (outcomes):
- What did we decide?
- What's still open?
- Who owns next steps?

**Identify follow-ups** (action items):
- Spike investigations
- Design reviews needed
- External dependencies
- Clarifications from stakeholders

### Handling "I Don't Know" Responses

When questions can't be answered:

1. **Capture as open question**:
   - Assign to appropriate person/team
   - Link in ticket for traceability
   - Flag as blocking or non-blocking

2. **Offer options to move forward**:
   - "Should we make an assumption to proceed?"
   - "Do we need a spike to validate?"
   - "Can we defer this to a separate ticket?"

3. **Note dependency**:
   - "This is blocked on [decision/clarification]"
   - "Engineering to spike approach by [date]"

## Post-Refinement: Ticket Quality Checklist

After refinement, ensure tickets are ready for development:

### Before Moving to Sprint

**For each ticket**, verify:

- [ ] **Title** is specific and action-oriented
- [ ] **Description** is concise (150-200 words) and answers: what, why, how
- [ ] **Type label** applied (Feature, Bug, Enhancement, etc.)
- [ ] **Acceptance criteria** are testable and specific (for complex work)
- [ ] **Dependencies** are identified and linked (if applicable)
- [ ] **Open questions** are flagged (if any remain)
- [ ] **Estimate** is provided (if team uses estimation)
- [ ] **No external blockers** (all prerequisites in progress or done)

### Team Readiness Check

**Before sprint starts**:
- [ ] All near-term tickets are in "Ready for Development" state
- [ ] Dependencies between tickets are clear
- [ ] Team has asked all blocking questions
- [ ] Success metrics defined for features
- [ ] Testing approach discussed for new work

## Sample Refinement Session Agenda

**Duration**: 60-90 minutes for 2-week sprint

### Timeboxed Segments

**0:00-5:00**: Opening and context
- Share sprint theme or roadmap context
- Overview of items to refine

**5:00-45:00**: Ticket refinement (30-40 minutes)
- Present each epic/feature
- Ask clarifying questions
- Discuss design, technical approach, edge cases
- Identify dependencies
- Capture open questions

**45:00-55:00**: Dependency mapping (10 minutes)
- Review identified dependencies
- Suggest parallelization opportunities
- Flag critical path

**55:00-85:00**: Estimation and prioritization (20-30 minutes)
- If using estimation, estimate tickets
- Confirm prioritization
- Ensure sprint capacity alignment

**85:00-90:00**: Wrap-up
- Recap decisions and open questions
- Assign owners for follow-ups
- Confirm next sprint readiness

## Common Refinement Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "This is too big" | Scope creep or lack of breakdown | Suggest splitting: by layer, by user journey, by value slice |
| "We don't know how to estimate" | Missing technical details | Spike first, then estimate. Or use T-shirt sizing (S/M/L). |
| "We're blocked on [X]" | External dependency or decision needed | Create separate decision/spike ticket; mark main ticket as blocked |
| "Acceptance criteria are too vague" | Product unclear on requirements | Ask specific questions; rewrite criteria to be testable |
| "This doesn't fit in a sprint" | Ticket too large | Break into sub-tickets; move lower-priority items to next sprint |
| "We forgot about [edge case]" | Incomplete analysis | Add as acceptance criteria; may increase estimate |

## Tips for Efficient Refinement

- **Prepare ahead**: Share ticket drafts before the session so team can read
- **Time-box discussions**: Allocate time per epic/feature, move on if no progress
- **Use templates**: Consistent ticket structure speeds discussion
- **Ask not to answer**: Ask questions; don't impose solutions
- **Record decisions**: Capture what was decided, not just what was discussed
- **Assign ownership**: Each open question has an owner and due date
