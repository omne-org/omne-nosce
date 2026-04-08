---
name: pre-promote
from-stage: propose
to-stage: promote
---

# Pre-Promote Hook

## Gate

All quality gates must pass and user must approve before promotion.

## Check

- [ ] `log/evolution/<distro>/results/` contains a recent gate run (`*-gates.md`)
- [ ] All gates in the latest run show PASS status
- [ ] Diff summary has been presented to and approved by user
