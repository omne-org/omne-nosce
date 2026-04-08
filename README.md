# omne-nosce

Self-evolution engine for the omne ecosystem. This distro governs the `omne-org/` volume and manages the lifecycle of all other distros.

## What This Repo Contains

This repo's root IS the distro image. When installed into a volume via `omne init`, the contents land in `.omne/image/`.

- `SYSTEM.md` — distro metadata, stage declarations, agent roster
- `context-map.md` — agent access matrix
- `agents/` — agent role definitions
- `skills/` — skill definitions per agent
- `hooks/` — stage transition enforcement
- `tools/` — automated quality gate runner (`inspect.py`)
- `defaults/` — default cfg/ content installed into volumes

## Stages

assess → design → generate → validate → propose → promote

## Usage

Installed into `omne-org/` as the governing distro:

```bash
cd omne-org
python omne/cli/omne.py init omne-org/omne-nosce
```

Run quality gates against a distro:

```bash
python .omne/image/tools/inspect_tool.py <target-distro-dir>
```
