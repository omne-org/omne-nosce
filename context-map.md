# Context Map

## Agent Access Matrix

| Agent | Reads | Writes |
|---|---|---|
| architect | MANIFEST.md, cfg/, log/ | log/ (stage transitions) |
| sonder | cfg/quality-gates/, nightly/ target distro | log/evolution/\<distro\>/proposals/ |
| negator | cfg/quality-gates/, nightly/ target distro | log/evolution/\<distro\>/results/ (review notes) |
| generator | approved design from log/evolution/, nightly/ | nightly/ distro files |
| inspector | cfg/quality-gates/ (read-only), nightly/ (read-only) | log/evolution/\<distro\>/results/ |
| clerk | log/ | log/sessions/, log/evolution/\<distro\>/ |

## Nightly Worktree Convention

- Path: `nightly/<distro-name>/` (relative to volume root)
- Source: `git worktree add` from the stable distro repo
- Branch: `evolve/<distro-name>/<YYYY-MM-DD>`
- Lifecycle: created at `generate`, removed after `promote` or abandon

## Log Structure

```
log/
  sessions/                          # per-session orchestrator logs
  evolution/
    <distro-name>/
      current.md                     # active evolution state (stage, branch, path)
      proposals/                     # design proposals awaiting approval
      results/                       # quality gate run results
      promotions/                    # promotion records (date, branch, gate results)
```
