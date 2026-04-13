---
name: generate-distro
description: Create or modify distro image files in the nightly worktree from an approved design. Use during the generate stage.
agent: generator
stage: generate
---

# Generate Distro

## Purpose

Create or modify distro image files in the nightly worktree based on an approved design.

## Inputs

- Approved design document from `log/evolution/<distro>/proposals/`
- `cfg/quality-gates/` — structural requirements to follow
- Nightly worktree at `nightly/<distro>/`

## Outputs

- Complete distro image files in `nightly/<distro>/`

## Procedure

1. Read approved design document
2. Create SYSTEM.md with YAML frontmatter (distro, distro-version, domain) and stage/agent tables
3. Create context-map.md with agent access matrix
4. For each agent: create agents/<name>.md with frontmatter (name, role, stages)
5. For each skill: create skills/<name>/SKILL.md with frontmatter (name, description, agent, stage) — Claude Code skill layout
6. For each hook: create hooks/<name>.md with frontmatter (name, from-stage, to-stage)
7. Create README.md
8. Commit all files in nightly worktree
