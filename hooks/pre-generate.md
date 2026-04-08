---
name: pre-generate
from-stage: design
to-stage: generate
---

# Pre-Generate Hook

## Gate

Design must be approved by user before generation can begin.

## Check

- [ ] `log/evolution/<distro>/proposals/` contains a design file (`*-design.md`)
- [ ] Design file contains: agents table, stages table, context map, hooks list
- [ ] Design file has been presented to and approved by user
