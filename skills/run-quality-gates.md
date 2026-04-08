---
name: run-quality-gates
agent: inspector
stage: validate
---

# Run Quality Gates

## Purpose

Execute automated quality gate checks against a nightly distro build.

## Inputs

- Target distro directory (nightly worktree path)
- Gate definitions from `cfg/quality-gates/`

## Outputs

- Gate results in `log/evolution/<distro>/results/<date>-gates.md`

## Procedure

1. Run: `python .omne/image/tools/inspect_tool.py <nightly-path>`
2. Capture output (per-gate pass/fail with issue details)
3. Write results to log/evolution/<distro>/results/
4. If any gate fails: report failures to Architect with file references
5. If all pass: report success to Architect
