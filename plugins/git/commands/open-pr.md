---
description: Create commits, push branch, and open a pull request on GitHub
argument-hint: [draft]
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git checkout:*), Bash(gh pr create:*), Bash(xdg-open:*), AskUserQuestion
---

# Open Pull Request

You are executing the `/open-pr` command. Follow these steps precisely:

## Parameters
- `draft` (optional): Create PR as draft if specified (e.g., `/open-pr draft`)

## Step 0: Branch Check

**CRITICAL: Run this check FIRST before any other steps.**

Check current branch with `git branch --show-current`.

**If on main or master branch:**
1. Analyze changes briefly to understand what was modified/added
2. Generate 4 best-effort branch name suggestions based on changes:
   - Use format: `feature/descriptive-name`, `fix/descriptive-name`, or `refactor/descriptive-name`
   - Make names concise but descriptive (2-4 words max)
   - Vary the suggestions to give different perspectives on the changes
3. Ask user to choose branch name using AskUserQuestion:
   - Question: "You're on the main/master branch. Choose a branch name:"
   - Options: Present the 4 generated branch names as options
   - Note: User can always select "Other" to provide custom branch name
4. Create and checkout new branch: `git checkout -b <chosen-branch-name>`

**If on any other branch:** Proceed to Step 1.

## Step 1: Analyze Changes

Run `git status` and `git diff` to analyze all changes:
- Identify files modified/created by Claude in current session
- Identify unstaged/untracked files NOT modified by Claude
- Review conversation context to detect if session involved multiple distinct tasks (separate features, fixes, or refactorings discussed/implemented)

## Step 2: Commit Strategy Questions

If you detect multiple distinct tasks from conversation context, ask user using AskUserQuestion tool (both questions in same group):

**Question 1** (always ask if multiple tasks detected):
- "How should I commit these changes?"
  - "Single commit" - Commit all changes together
  - "Multiple logical commits" - Create separate commits for each distinct task/feature

**Question 2** (ask ONLY if unstaged/untracked files exist that Claude didn't modify):
- "There are uncommitted changes not made in this session. Include them?"
  - "Yes, include all changes" - Stage and commit everything
  - "No, only Claude's changes" - Commit only files Claude modified
  - "Let me review first" - Show list of files and stop

## Step 3: Create Commits

**Commit Message Rules:**
- **Style**: Concise, factual, savant-like. State what was done, not why (unless discussed during implementation)
- **Simple changes**: Title only (no description)
- **Complex changes**: Title + description
  - Description adds context about what was changed
  - Use facts, avoid self-praise adjectives ("improved", "optimized", "enhanced")
  - Only state intents if explicitly discussed during implementation
- **Hard limit**: 80 words total
- **Format**: Always use heredoc for commit message

**Examples:**
```bash
# Simple change
git commit -m "$(cat <<'EOF'
Add user authentication middleware
EOF
)"

# Complex change
git commit -m "$(cat <<'EOF'
Refactor database connection pooling

Extracted connection logic into separate module. Added retry mechanism
for failed connections. Configured pool size based on environment variables.
EOF
)"
```

If creating multiple logical commits:
- Create commits in chronological order of implementation
- Each commit should be self-contained and logical
- Follow same message rules for each commit

## Step 4: Push Branch

Check if force-push is needed (`git status` shows diverged branch).

**If force-push required**: Ask user for confirmation before proceeding.

**Otherwise**: Auto-push with `git push -u origin <branch-name>`

**On push failure**: Explain error and ask if you should retry with alternative approach.

## Step 5: Create Pull Request

**PR Title**: Use title from commit message (if single commit) or summarize all commits (if multiple)

**PR Description Rules:**
- **Always include description** (even for simple changes)
- Same style as commit messages: factual, concise, savant-like
- For single commit: Expand on commit message with more context
- For multiple commits: List key changes made across commits
- Avoid self-praise language, state facts only
- **Hard limit**: 150 words

**PR Metadata:**
- Auto-detect default branch (main/master) as base
- If `draft` parameter passed: add `--draft` flag
- No labels/reviewers unless user specifies

**Create PR:**
```bash
gh pr create --title "PR title" --body "$(cat <<'EOF'
PR description content here.
EOF
)" [--draft]
```

**On PR creation failure**: Explain error and ask if you should retry with alternative approach.

## Step 6: Open PR Page

After successful PR creation, extract PR URL from `gh` output and open it:
```bash
xdg-open <PR_URL>
```

## Error Handling

If any step fails:
1. Explain what went wrong clearly
2. Provide the specific error message
3. Ask user if you should retry with an alternative approach
4. If user confirms, attempt automatic fix or provide manual commands

## Final Output

After successful completion, output:
- Commit SHA(s)
- Branch name
- PR URL
- Confirmation that PR page was opened
