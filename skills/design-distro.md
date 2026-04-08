---
name: design-distro
agent: sonder
stage: design
---

# Design Distro

## Purpose

Co-design a complete distro specification with the user, incorporating Negator feedback.

## Inputs

- Assessment document from `log/evolution/<distro>/proposals/`
- User feedback and decisions
- Negator review notes (during iteration)

## Outputs

- Design document in `log/evolution/<distro>/proposals/<date>-design.md`

## Procedure

1. Present assessment summary and proposed agents/stages to user
2. For each proposed agent: define role, responsibilities, reads, writes, skills
3. For each proposed stage: define entry gate, artifacts produced, exit gate
4. For each stage transition: define what hook should enforce
5. Define context-map: which agent reads/writes what
6. Submit design to Negator for adversarial review
7. Iterate on Negator feedback until stable
8. Present final design to user for approval
