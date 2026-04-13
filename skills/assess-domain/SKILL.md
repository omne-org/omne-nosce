---
name: assess-domain
description: Explore a target domain (workflows, roles, artifacts) to inform a distro proposal. Use during the assess stage.
agent: sonder
stage: assess
---

# Assess Domain

## Purpose

Explore a target domain to understand what a distro for that domain needs.

## Inputs

- Domain name or description from user
- `cfg/quality-gates/` — structural requirements for valid distros
- Existing distro repos — for cross-reference

## Outputs

- Assessment document in `log/evolution/<distro>/proposals/<date>-assessment.md`

## Procedure

1. Research the domain: core workflows, roles people play
2. Map domain activities to potential agent roles
3. Map domain lifecycle to potential stages
4. Identify domain-specific artifacts produced at each stage
5. Note constraints, conventions, or tools specific to the domain
6. Write assessment: domain summary, proposed agents, proposed stages, open questions
