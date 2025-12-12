---
name: rails-basecamp-engineer
description: This skill provides expert guidance on implementing Ruby on Rails applications using 37signals (Basecamp/HEY) patterns and conventions. Use when building Rails features, implementing authentication, authorization, multi-tenancy, background jobs, or Hotwire/Turbo/Stimulus following 37signals patterns.
---

# Rails Basecamp Engineer

## Overview

This skill provides comprehensive guidance for building Ruby on Rails applications using 37signals/Basecamp coding patterns. These patterns emphasize composition over inheritance, concern-based organization, minimal controllers, rich domain models, and native Rails capabilities over external gems.

## Core Principles

1. **Composition over inheritance** - Heavy use of concerns to compose behavior
2. **Feature-driven organization** - Group code by domain feature, not by layer
3. **Minimal controllers** - Push business logic to models and concerns
4. **Rich domain models** - Models are the heart of the application
5. **Native Rails first** - Prefer Rails features over external gems
6. **Explicit over implicit** - Clear, readable code over clever shortcuts
7. **Transaction safety** - Wrap critical operations in transactions
8. **Event tracking** - Record significant actions for audit trails

## Reference Files

Load the appropriate reference when implementing specific patterns or domains:

### General Patterns
- `references/models.md` - Model patterns, concerns, associations, callbacks, scopes
- `references/controllers.md` - Controller patterns, concerns, filters, response handling
- `references/current-attributes.md` - CurrentAttributes pattern for request-scoped context

### Domain-Specific Patterns
- `references/authentication.md` - Passwordless magic link and traditional password authentication
- `references/authorization.md` - Role-based and resource-level access control
- `references/multi-tenancy.md` - URL-based (shared DB) and subdomain-based (DB per tenant) approaches
- `references/hotwire.md` - Turbo Frames, Turbo Streams, and Stimulus controller patterns
- `references/background-jobs.md` - Solid Queue configuration, recurring jobs, account context
- `references/event-tracking.md` - Audit trails, activity feeds, notifications, webhooks
- `references/testing.md` - Testing philosophy, fixtures, system tests, and helpers

## Quick Decision Guide

| Task | Reference File |
|------|----------------|
| Setting up a new model with concerns | `models.md` |
| Validations, associations, callbacks | `models.md` |
| Creating controllers and concerns | `controllers.md` |
| Strong parameters, response formats | `controllers.md` |
| Request-scoped context (Current.user, etc.) | `current-attributes.md` |
| Adding user login/logout | `authentication.md` |
| Implementing permissions/roles | `authorization.md` |
| Multi-account/tenant support | `multi-tenancy.md` |
| Real-time UI updates | `hotwire.md` |
| Background processing | `background-jobs.md` |
| Activity feeds, audit trails | `event-tracking.md` |
| Writing tests | `testing.md` |
