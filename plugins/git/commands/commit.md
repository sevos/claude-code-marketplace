---
description: Create git commits for changes made during the current session
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Task, AskUserQuestion
model: haiku
---

# Commit Changes

You are executing the `/commit` command. Follow these steps precisely:

## Overview

This command creates git commits for changes made during the current session. It delegates the analysis and commit creation to a general-purpose agent to avoid polluting the main conversation context.

## Step 1: Extract Conversation Context

Before delegating to the agent, analyze the conversation history to extract:
- What tasks/features were discussed and implemented
- Which files were mentioned or modified during implementation
- Any specific intents or goals stated by the user
- Whether multiple distinct tasks were worked on

Create a concise summary (2-4 sentences) of the session's work.

## Step 2: Delegate to Agent

Launch a general-purpose agent with the Task tool using the haiku model for efficiency, providing:

**Prompt structure:**
```
You are helping create git commits for a coding session.

Session context:
[Include the summary from Step 1]

Your tasks:
1. Analyze changes: Run git status and git diff to see all changes. Based on the session context above, identify which changes are relevant to commit.

2. Commit strategy: If multiple distinct tasks were detected from the session context, ask the user using AskUserQuestion tool:
   - Question 1: "How should I commit these changes?"
     - "Single commit" - Commit all changes together
     - "Multiple logical commits" - Create separate commits for each distinct task/feature

   - Question 2 (only if unstaged/untracked files exist that weren't part of the session work):
     "There are uncommitted changes not made in this session. Include them?"
     - "Yes, include all changes" - Stage and commit everything
     - "No, only session changes" - Commit only files from this session
     - "Let me review first" - Show list of files and stop

3. Create commits following these rules:
   - Style: Concise, factual, savant-like. State what was done, not why (unless discussed during implementation)
   - Simple changes: Title only (no description)
   - Complex changes: Title + description with context about what was changed
   - Use facts, avoid self-praise adjectives ("improved", "optimized", "enhanced")
   - Hard limit: 80 words total
   - Format: Always use heredoc for commit message
   - Footer: Always append:
     ```

     🤖 Generated with [Claude Code](https://claude.com/claude-code)

     Co-Authored-By: Claude <noreply@anthropic.com>
     ```

   Examples:
   ```bash
   # Simple change
   git commit -m "$(cat <<'EOF'
   Add user authentication middleware

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"

   # Complex change
   git commit -m "$(cat <<'EOF'
   Refactor database connection pooling

   Extracted connection logic into separate module. Added retry mechanism
   for failed connections. Configured pool size based on environment variables.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

   If creating multiple logical commits:
   - Create commits in chronological order of implementation
   - Each commit should be self-contained and logical
   - Follow same message rules for each commit

4. Return the following information:
   - Commit SHA(s)
   - Full commit message(s) for each commit created
```

## Step 3: Display Results

After the agent completes, display the output:
- List each commit SHA with its full commit message
- Confirm total number of commits created

Example output format:
```
Created 1 commit:

abc123d - Add user authentication middleware

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Error Handling

If the agent reports any failures:
1. Display the error message clearly
2. Ask user if they want to retry or need assistance
3. Do not attempt automatic fixes in the main conversation
