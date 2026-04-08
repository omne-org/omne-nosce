---
name: coverage
type: static
---

# Coverage Quality Gate

## What to Check

Every agent defined in `agents/` must be referenced in `context-map.md`.

## Pass Criteria

- [ ] Every `.md` file in `agents/` has a `name` field in its YAML frontmatter
- [ ] Every agent name from `agents/` appears in at least one row of the context-map agent access matrix
- [ ] Every agent listed in the context-map has a corresponding file in `agents/`
