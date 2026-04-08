---
name: skills
type: static
---

# Skills Quality Gate

## What to Check

Every agent must have at least one skill defined in `skills/`.

## Pass Criteria

- [ ] Every `.md` file in `skills/` has an `agent` field in its YAML frontmatter
- [ ] Every agent name from `agents/` appears as the `agent` field in at least one skill file
- [ ] Every `agent` referenced in a skill file has a corresponding file in `agents/`
