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

### Core Patterns
- `references/models.md` - Model patterns, concerns, associations, callbacks, scopes
- `references/controllers.md` - Controller patterns, concerns, filters, response handling
- `references/current-attributes.md` - CurrentAttributes pattern for request-scoped context
- `references/routing.md` - CRUD-everything routing philosophy, polymorphic URLs
- `references/poros.md` - Plain Old Ruby Objects patterns
- `references/view-helpers.md` - Stimulus-integrated view helpers

### Domain-Specific Patterns
- `references/authentication.md` - Authentication overview and shared architecture
  - `references/authentication/magic-link.md` - Passwordless magic link (primary 37signals pattern)
  - `references/authentication/password.md` - Traditional password authentication
- `references/authorization.md` - Role-based and resource-level access control
- `references/multi-tenancy/` - Multi-tenancy approaches:
  - `references/multi-tenancy/shared-database.md` - Shared DB with tenant_id filtering (Fizzy/Basecamp pattern)
  - `references/multi-tenancy/database-per-tenant.md` - Separate DB per tenant (activerecord-tenanted)

### Frontend & Hotwire
- `references/hotwire.md` - Turbo Frames, Turbo Streams overview
- `references/stimulus/` - Stimulus controller catalog:
  - `stimulus/utility-controllers.md` - copy-to-clipboard, hotkey, toggle-class, beacon
  - `stimulus/form-controllers.md` - auto-submit, autoresize, local-save, character-counter
  - `stimulus/ui-controllers.md` - dialog, lightbox, navigable-list, fetch-on-visible
  - `stimulus/interaction-controllers.md` - drag-and-drop, sortable, resize
- `references/frontend/` - CSS approach alternatives:
  - `frontend/vanilla-css.md` - 37signals CSS (layers, OKLCH, design tokens)
  - `frontend/daisyui.md` - DaisyUI/TailwindCSS alternative (uses Context7 for live docs)

### Infrastructure
- `references/background-jobs.md` - Solid Queue configuration, recurring jobs, account context
- `references/caching.md` - HTTP caching (ETags), fragment caching, touch invalidation
- `references/configuration.md` - ENV patterns, multi-database, Solid Stack setup
- `references/mailers.md` - Minimal mailer patterns, bundled notifications

### Other
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
| Routing with CRUD-everything | `routing.md` |
| Adding user login/logout | `authentication.md` + subdirectory |
| Implementing permissions/roles | `authorization.md` |
| Multi-account/tenant support | `multi-tenancy/shared-database.md` or `database-per-tenant.md` |
| Real-time UI updates (Turbo) | `hotwire.md` |
| Stimulus controllers | `stimulus/` subdirectory |
| CSS styling (vanilla) | `frontend/vanilla-css.md` |
| CSS styling (DaisyUI) | `frontend/daisyui.md` |
| Background processing | `background-jobs.md` |
| HTTP caching, ETags | `caching.md` |
| Sending emails | `mailers.md` |
| Activity feeds, audit trails | `event-tracking.md` |
| Writing tests | `testing.md` |
| View helpers with Stimulus | `view-helpers.md` |
| Business logic objects | `poros.md` |
| ENV configuration | `configuration.md` |
