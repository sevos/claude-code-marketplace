---
description: Create commits, push branch, and open a pull request on GitHub
argument-hint: [draft]
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git checkout:*), Task, AskUserQuestion
model: claude-haiku-4-5
---

# Open Pull Request

You are executing the `/open-pr` command. Follow these steps precisely:

## Parameters
- `draft` (optional): Create PR as draft if specified (e.g., `/open-pr draft`)

## Overview

This command creates commits, pushes a branch, and opens a PR. Questions are asked upfront in the main agent, then execution is delegated to preserve context.

---

## Step 0: Branch Check

**CRITICAL: Run this check FIRST.**

Check current branch: `git branch --show-current`

**If on main or master branch:**
1. Run `git diff --stat` to understand changes briefly
2. Generate 4 branch name suggestions based on changes:
   - Format: `feature/name`, `fix/name`, or `refactor/name`
   - Concise: 2-4 words max
3. Ask user using AskUserQuestion:
   - Header: "Branch"
   - Question: "You're on main/master. Choose a branch name:"
   - Options: The 4 generated branch names
4. Create and checkout: `git checkout -b <chosen-branch-name>`

**If on any other branch:** Proceed to Step 1.

## Step 1: Quick Assessment

**Extract session context:**
- Analyze conversation for tasks/features implemented
- Note files mentioned or modified
- Identify if multiple distinct tasks were worked on

**Run lightweight git commands:**
```bash
git status --short
git diff --stat
```

**Assess:**
- Distinct change groups (multiple features/fixes)?
- Unstaged/untracked files not from session work?

Create a concise summary (2-4 sentences) of the session's work.

## Step 2: Ask Questions (if needed)

Use AskUserQuestion to gather decisions BEFORE delegating. Ask in a single call when multiple apply:

**Question 1** (if multiple distinct tasks detected):
- Header: "Commits"
- Question: "How should I commit these changes?"
- Options:
  - "Single commit" - Commit all changes together
  - "Multiple logical commits" - Create separate commits for each task

**Question 2** (if unstaged/untracked files exist not from session):
- Header: "Scope"
- Question: "There are uncommitted changes not made in this session. Include them?"
- Options:
  - "Yes, include all changes" - Stage and commit everything
  - "No, only session changes" - Commit only session files
  - "Let me review first" - Show files and STOP

If "Let me review first": List files and wait. Do not proceed.

## Step 3: Delegate to Agent

Launch a general-purpose agent with the Task tool using claude-haiku-4-5 model.

**Include in the prompt:**
1. Session context summary
2. Commit strategy choice
3. Files to include/exclude
4. Branch name (current branch)
5. Whether draft PR was requested
6. All execution rules below

**Agent prompt structure:**
```
You are creating commits, pushing a branch, and opening a PR. Work autonomously - do not ask questions.

## Session Context
[Include summary from Step 1]

## User Decisions
- Commit strategy: [single commit / multiple logical commits]
- Scope: [all changes / session changes only - list specific files if applicable]
- Branch: [branch name]
- Draft PR: [yes/no]

## Your Tasks

### 1. Analyze changes
Run `git diff` on relevant files to understand what changed.

### 2. Create commits
Stage and commit according to user's strategy.

**Commit message rules:**
- Style: Concise, factual. State what was done.
- Simple changes: Title only
- Complex changes: Title + brief description
- Avoid self-praise adjectives
- Hard limit: 80 words total
- Format:
  ```bash
  git commit -m "$(cat <<'EOF'
  Commit title here

  Optional description.
  EOF
  )"
  ```

If multiple commits: chronological order, each self-contained.

### 3. Push branch
Check if force-push needed (`git status` shows diverged).

- If force-push required: Report this and STOP. Do not force push without explicit instruction.
- Otherwise: `git push -u origin <branch-name>`

On push failure: Report error and stop.

### 4. Create Pull Request

**PR Title:**
- Single commit: Use commit message title
- Multiple commits: Summarize all commits

**PR Description:**
- Always include description
- Factual, concise style (same as commits)
- Single commit: Expand on commit message
- Multiple commits: List key changes
- Hard limit: 150 words

**Create PR:**
```bash
gh pr create --title "PR title" --body "$(cat <<'EOF'
PR description here.
EOF
)" [--draft if requested]
```

On failure: Report error and stop.

### 5. Open PR in browser
```bash
xdg-open <PR_URL>
```

### 6. Return results
Output:
- Commit SHA(s) with messages
- Branch name
- PR URL
- Confirmation browser was opened
```

## Step 4: Display Results

After agent completes, display:
- Commit SHA(s) with messages
- Branch name
- PR URL
- Total commits created

## Error Handling

If agent reports failures:
1. Display error clearly
2. Ask if user wants to retry or needs assistance
