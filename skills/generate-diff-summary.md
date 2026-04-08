---
name: generate-diff-summary
agent: clerk
stage: propose
---

# Generate Diff Summary

## Purpose

Create a human-readable summary of changes in the nightly worktree for user review.

## Inputs

- Nightly worktree path
- Evolution branch name from `log/evolution/<distro>/current.md`

## Outputs

- Diff summary presented to user and archived to `log/evolution/<distro>/results/<date>-diff.md`

## Procedure

1. Read `current.md` to get branch name and nightly path
2. Run `git diff main...<branch>` in the distro repo
3. Summarize: files added, modified, removed
4. For each changed file: one-line description of what changed
5. Include gate results from latest validation run
6. Present to user for review
