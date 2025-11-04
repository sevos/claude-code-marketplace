# Ticket Template

Use this template as a starting point for new tickets. Adapt based on complexity:
- **Simple tickets**: Use minimal template (title + brief what/why/how)
- **Complex features**: Use full template with all sections
- **Bugs**: Use bug-specific template (STR + Expected vs Actual)

## Simple Ticket Template

```
Title: [Action] [What] [Where if specific]

[1-2 sentence context about why this matters]

[Brief: what needs to change]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
```

## Complex Feature Ticket Template

```
Title: [Action] [What] for [User Type/Context]

## Context
[2-3 sentences explaining why this matters]
- Problem it solves:
- User impact:
- Business value:

## Requirements
- Functional requirement 1
- Functional requirement 2
- Non-functional requirement (performance, compatibility, etc.)
- Integration points with [System X]

## Acceptance Criteria

### Given-When-Then Examples
Given [initial state]
When [action taken]
Then [expected outcome]

### Additional Checkboxes
- [ ] API endpoint returns 200 status
- [ ] Error handling for [edge case] returns 400
- [ ] Documentation updated
- [ ] Test coverage at [X]%

## Open Questions
- [Engineering] How should we handle [technical concern]?
- [Product] What's the expected behavior for [scenario]?
- [Business] Do we need [compliance/security feature]?

## Dependencies
- Depends on: [Ticket ID if applicable]
- Blocks: [Ticket ID if applicable]

## Estimate
[Story points or T-shirt size if using estimation]
```

## Bug Ticket Template

```
Title: [Bug] [Component] [Symptom]

## Steps to Reproduce
1. Navigate to [page/screen]
2. [Action 1]
3. [Action 2]
4. [Observe result]

## Expected Behavior
[What should happen]

## Actual Behavior
[What is actually happening]

## Environment
- Browser: [Chrome 120 on macOS / etc.]
- Device: [Device model]
- OS: [OS and version]
- Network: [Stable / Flaky / etc.]
- User Type: [Admin / Regular user / etc.]

## Additional Context
[Screenshots, error logs, data samples if helpful]

## Severity
- [ ] Critical (Service down, data loss, security)
- [ ] High (Core feature broken, widespread impact)
- [ ] Medium (Feature partially broken, workaround exists)
- [ ] Low (Minor UI issue, edge case, cosmetic)

## Acceptance Criteria
- [ ] Bug reproduction confirmed
- [ ] Root cause identified and documented
- [ ] Fix implemented and tested
- [ ] Regression test added
- [ ] Verified in [environment]
```

## Epic Ticket Template

```
Title: [Capability] for [User/Team/Domain]

## Overview
[1-2 sentence description of the epic scope]

## Goals
- Goal 1: [Specific, measurable outcome]
- Goal 2: [Specific, measurable outcome]

## Scope
**In Scope**:
- Feature/capability 1
- Integration with [System X]
- Support for [User type/scenario]

**Out of Scope** (explicitly defer):
- Feature that's related but separate
- Advanced feature deferred to later

## Success Metrics
- [Metric 1]: Target [X] by [Date]
- [Metric 2]: Target [X] by [Date]

## Key Dependencies
- Requires: [System/Feature that must be in place]
- Blocks: [Work that will be blocked on this]
- Integrates with: [Related systems]

## Acceptance Criteria
- [ ] All child tickets completed
- [ ] Documentation complete
- [ ] [User type] can [primary use case]
- [ ] Performance target [X] met
- [ ] Rollout to [X]% of users successful

## Open Questions
- [Product] Should we support [feature variant]?
- [Engineering] Is [architecture choice] the right approach?
- [Design] What's the rollout experience?

## Planned Breakdown (Initial)
- [Ticket category 1]: e.g., Backend API implementation
- [Ticket category 2]: e.g., Frontend UI
- [Ticket category 3]: e.g., Testing and validation
- [Ticket category 4]: e.g., Documentation
```

## Notes on Template Usage

**Title Writing Tips**:
- ✅ "Add CSV export for user data"
- ✅ "[Bug] Email parser fails on UTF-8 domains"
- ✅ "[Epic] Mobile app for iOS"
- ❌ "Export feature"
- ❌ "Parser issue"

**When to use Complex Template**:
- Feature impacts multiple systems
- Epic or large feature
- Cross-team dependencies
- Performance or security considerations
- Unclear requirements or assumptions

**When to use Simple Template**:
- UI/text changes
- Small bug fixes
- Documentation updates
- Isolated improvements

**Accepting Criteria Tips**:
- Make them testable without ambiguity
- Include both happy path and error cases
- For complex logic, use Given-When-Then format
- For simple features, checkboxes are fine
- Avoid "code is clean" or vague criteria
