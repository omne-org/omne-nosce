---
name: hooks
type: static
---

# Hooks Quality Gate

## What to Check

Every stage transition should have a corresponding hook in `hooks/`.

## Pass Criteria

- [ ] Each hook file has `from-stage` and `to-stage` in its YAML frontmatter
- [ ] Every `from-stage` and `to-stage` in hooks corresponds to a stage in SYSTEM.md
