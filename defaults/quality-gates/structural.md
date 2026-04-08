---
name: structural
type: static
---

# Structural Quality Gate

## What to Check

Every distro image must have the required directory structure and files.

## Pass Criteria

- [ ] `agents/` directory exists and contains at least one `.md` file
- [ ] `skills/` directory exists and contains at least one `.md` file
- [ ] `hooks/` directory exists and contains at least one `.md` file
- [ ] `context-map.md` exists at image root
- [ ] `SYSTEM.md` exists at image root
- [ ] No directory exceeds 2 levels of nesting from image root
