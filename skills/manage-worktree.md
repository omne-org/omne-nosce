---
name: manage-worktree
agent: architect
stage: generate
---

# Manage Worktree

## Purpose

Create and remove nightly worktrees for distro evolution cycles.

## Create Worktree

```bash
cd <distro-repo>
git worktree add ../nightly/<distro-name> -b evolve/<distro-name>/<YYYY-MM-DD>
```

## Remove Worktree

```bash
cd <distro-repo>
git worktree remove ../nightly/<distro-name>
```

## State Tracking

After creating worktree, Clerk writes `log/evolution/<distro>/current.md`:

```markdown
---
distro: <distro-name>
stage: generate
branch: evolve/<distro-name>/<YYYY-MM-DD>
nightly-path: nightly/<distro-name>
---
```
