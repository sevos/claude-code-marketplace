---
description: Create git commits for changes made during the current session
allowed-tools: Bash(git status:*), Bash(git diff:*), Task, AskUserQuestion
model: claude-haiku-4-5
---

# Commit Changes

You are executing the `/commit` command. Follow these steps precisely:

## Overview

This command creates git commits for changes made during the current session. Questions are asked upfront, then execution is delegated to a general-purpose agent to avoid polluting the main conversation context.

## Step 1: Session Context + Quick Assessment

**Extract session context:**
- Analyze conversation history for tasks/features implemented
- Note which files were mentioned or modified
- Identify if multiple distinct tasks were worked on

**Run lightweight git commands:**
```bash
git status --short
git diff --stat
```

**Assess the changes:**
- Count files with changes
- Identify if there are distinct change groups (multiple features/fixes)
- Check for unstaged/untracked files that weren't part of the session work

Create a concise summary (2-4 sentences) of the session's work for later use.

## Step 2: Ask Questions (if needed)

Use AskUserQuestion to gather decisions BEFORE delegating. Ask questions in a single call when multiple apply:

**Question 1** (ask if multiple distinct tasks detected from session context):
- Header: "Commits"
- Question: "How should I commit these changes?"
- Options:
  - "Single commit" - Commit all changes together
  - "Multiple logical commits" - Create separate commits for each distinct task/feature

**Question 2** (ask ONLY if unstaged/untracked files exist that weren't part of session work):
- Header: "Scope"
- Question: "There are uncommitted changes not made in this session. Include them?"
- Options:
  - "Yes, include all changes" - Stage and commit everything
  - "No, only session changes" - Commit only files from this session
  - "Let me review first" - Show list of files and STOP (do not proceed to Step 3)

If "Let me review first" is selected: List the files and wait for user guidance. Do not proceed.

## Step 3: Delegate to Agent

Launch a general-purpose agent with the Task tool using claude-haiku-4-5 model.

**Include in the prompt:**
1. Session context summary from Step 1
2. User's commit strategy choice (single vs multiple commits)
3. Files to include/exclude based on user's scope choice
4. The commit rules below

**Agent prompt structure:**
```
You are creating git commits for a coding session. Work autonomously - do not ask questions.

## Session Context
[Include summary from Step 1]

## User Decisions
- Commit strategy: [single commit / multiple logical commits]
- Scope: [all changes / session changes only - list specific files if applicable]

## Your Tasks

1. **Analyze changes in detail**
   Run `git diff` on the relevant files to understand what changed.

2. **Stage and commit**
   - Stage appropriate files with `git add`
   - Create commit(s) according to user's strategy choice

3. **Commit message rules**
   - Style: Concise, factual, savant-like. State what was done.
   - Simple changes: Title only (no description)
   - Complex changes: Title + brief description
   - Use facts, avoid self-praise adjectives ("improved", "optimized", "enhanced")
   - Hard limit: 80 words total
   - Format: Always use heredoc:
     ```bash
     git commit -m "$(cat <<'EOF'
     Commit title here

     Optional description for complex changes.
     EOF
     )"
     ```

   If creating multiple commits:
   - Create in chronological order of implementation
   - Each commit should be self-contained and logical

4. **Return results**
   Output each commit SHA and its full message.
```

## Step 4: Display Results

After the agent completes, display:
- Each commit SHA with its full commit message
- Total number of commits created

Example output:
```
Created 1 commit:

abc123d - Add user authentication middleware
```

## Error Handling

If the agent reports failures:
1. Display the error message clearly
2. Ask user if they want to retry or need assistance
