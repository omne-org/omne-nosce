---
distro: omne-nosce
distro-version: 0.1.0
domain: org-governance
log-dirs: [sessions, evolution]
---

# SYSTEM — omne-nosce

> Self-evolution engine. Co-designs, validates, and promotes omne distros.

## Stages

| Stage | Entry Gate | Artifacts | Exit Gate |
|---|---|---|---|
| assess | user request or scheduled review | assessment proposal in `log/evolution/<distro>/proposals/` | proposal written |
| design | assessment exists | design doc with agents, stages, skills, hooks | user approval |
| generate | design approved | distro files in `nightly/<distro>/` worktree | all required image/ files exist |
| validate | files generated | gate results in `log/evolution/<distro>/results/` | all gates pass |
| propose | gates pass | diff summary for user review | user approval |
| promote | user approves | merged evolution branch, archived promotion record | merge succeeds, gates pass on merged result |

## Agents

- **architect** — orchestrator, coordinates all agents, talks to user
- **sonder** — domain explorer, generates design proposals
- **negator** — adversarial reviewer, stress-tests designs and artifacts
- **generator** — scaffolder, creates/modifies distro files
- **inspector** — quality gate runner, validates distros against cfg/quality-gates/
- **clerk** — bookkeeper, logs state transitions and generates reports

## Boot Chain

1. Volume `CLAUDE.md` imports `@.omne/MANIFEST.md`
2. MANIFEST imports this file via `@image/SYSTEM.md`
3. This file imports `@context-map.md` below

@context-map.md
