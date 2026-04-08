---
name: system
type: static
---

# System Quality Gate

## What to Check

`SYSTEM.md` must have valid frontmatter and reference all agents.

## Pass Criteria

- [ ] `SYSTEM.md` has YAML frontmatter with fields: `distro`, `distro-version`, `domain`
- [ ] `SYSTEM.md` contains a `## Agents` section
- [ ] Every agent file in `agents/` is listed in the Agents section
- [ ] Every agent listed in the Agents section has a corresponding file in `agents/`
