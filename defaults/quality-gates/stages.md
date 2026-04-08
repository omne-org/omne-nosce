---
name: stages
type: static
---

# Stages Quality Gate

## What to Check

`SYSTEM.md` must declare stages, and each stage must have entry gate, artifacts, and exit gate.

## Pass Criteria

- [ ] `SYSTEM.md` contains a `## Stages` section
- [ ] Stages section contains a markdown table
- [ ] Table has columns: Stage, Entry Gate, Artifacts, Exit Gate
- [ ] Each row has non-empty values in all four columns
- [ ] At least one stage is declared
