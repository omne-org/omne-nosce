---
name: review-distro
description: Adversarially review distro designs and generated artifacts for gaps, contradictions, and logical flaws. Use during design and validate stages.
agent: negator
stage: design
---

# Review Distro

## Purpose

Adversarial review of distro designs and generated artifacts. Identify gaps, contradictions, missing coverage, and logical flaws.

## Inputs

- Design document from `log/evolution/<distro>/proposals/`
- Generated distro files in `nightly/<distro>/` (during validate)
- `cfg/quality-gates/` (to understand what automated checks cover)

## Outputs

- Review notes in `log/evolution/<distro>/results/<date>-review.md`

## Procedure

1. Read the design document or generated files
2. For each agent definition: is the role clear? are reads/writes complete? any redundancy with other agents?
3. For each stage: is the entry gate enforceable? are artifacts well-defined? could the exit gate be gamed?
4. For the context-map: are there agents with overlapping writes? are there artifacts no agent reads?
5. For hooks: do they actually enforce the gates they claim to?
6. For skills: are procedures actionable? could an agent follow them without ambiguity?
7. Report issues with specific file references and suggested fixes
8. If no issues remain: approve
