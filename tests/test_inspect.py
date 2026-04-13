"""Tests for tools/inspect_tool.py — quality gate inspector."""

import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from inspect_tool import (
    check_structural,
    check_system,
    check_coverage,
    check_stages,
    check_hooks,
    check_skills,
    inspect_distro,
)


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _make_valid_distro(root: Path) -> None:
    (root / "agents").mkdir()
    (root / "skills").mkdir()
    (root / "hooks").mkdir()
    (root / "agents" / "worker.md").write_text(
        "---\nname: worker\nrole: subagent\nstages: [build]\n---\n# Worker\n"
    , encoding="utf-8")
    (root / "skills" / "do-work").mkdir()
    (root / "skills" / "do-work" / "SKILL.md").write_text(
        "---\nname: do-work\ndescription: Do the work for the worker agent\nagent: worker\nstage: build\n---\n# Do Work\n"
    , encoding="utf-8")
    (root / "hooks" / "pre-build.md").write_text(
        "---\nname: pre-build\nfrom-stage: plan\nto-stage: build\n---\n# Pre-Build\n"
    , encoding="utf-8")
    (root / "context-map.md").write_text(
        "# Context Map\n\n| Agent | Reads | Writes |\n|---|---|---|\n| worker | src/ | build/ |\n"
    , encoding="utf-8")
    (root / "SYSTEM.md").write_text(
        "---\ndistro: test-distro\ndistro-version: 0.1.0\ndomain: testing\n---\n"
        "# SYSTEM\n\n## Stages\n\n"
        "| Stage | Entry Gate | Artifacts | Exit Gate |\n"
        "|---|---|---|---|\n"
        "| plan | user request | plan doc | plan approved |\n"
        "| build | plan approved | built artifact | tests pass |\n\n"
        "## Agents\n\n- **worker** — does the work\n"
    , encoding="utf-8")


# ---------------------------------------------------------------------------
# Structural checks (8 tests)
# ---------------------------------------------------------------------------

class TestCheckStructural(unittest.TestCase):

    def test_valid_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            issues = check_structural(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")

    def test_missing_agents_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            import shutil
            shutil.rmtree(root / "agents")
            issues = check_structural(root)
            self.assertTrue(any("agents" in i for i in issues), issues)

    def test_missing_skills_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            import shutil
            shutil.rmtree(root / "skills")
            issues = check_structural(root)
            self.assertTrue(any("skills" in i for i in issues), issues)

    def test_missing_hooks_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            import shutil
            shutil.rmtree(root / "hooks")
            issues = check_structural(root)
            self.assertTrue(any("hooks" in i for i in issues), issues)

    def test_missing_context_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "context-map.md").unlink()
            issues = check_structural(root)
            self.assertTrue(any("context-map.md" in i for i in issues), issues)

    def test_missing_system_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "SYSTEM.md").unlink()
            issues = check_structural(root)
            self.assertTrue(any("SYSTEM.md" in i for i in issues), issues)

    def test_empty_agents_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "agents" / "worker.md").unlink()
            issues = check_structural(root)
            self.assertTrue(any("agents" in i for i in issues), issues)

    def test_depth_violation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            # Create a nested subdir inside agents (depth 3 from root)
            nested = root / "agents" / "subgroup" / "deep.md"
            nested.parent.mkdir()
            nested.write_text("# deep\n", encoding="utf-8")
            issues = check_structural(root)
            self.assertTrue(any("depth" in i.lower() or "nested" in i.lower() for i in issues), issues)

    def test_core_submodule_skipped(self):
        """core/ kernel submodule (deep nesting) does not trigger depth violation."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            # Simulate kernel submodule structure at core/cli/lib/
            deep = root / "core" / "cli" / "lib" / "distro.py"
            deep.parent.mkdir(parents=True)
            deep.write_text("# kernel module\n", encoding="utf-8")
            issues = check_structural(root)
            self.assertEqual(issues, [], f"core/ should be skipped, got: {issues}")

    def test_valid_without_core(self):
        """Distro without core/ submodule still passes structural check."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            # No core/ dir — backward compat
            issues = check_structural(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")


# ---------------------------------------------------------------------------
# System checks (5 tests)
# ---------------------------------------------------------------------------

class TestCheckSystem(unittest.TestCase):

    def test_valid_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            issues = check_system(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")

    def test_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "SYSTEM.md").write_text("# SYSTEM\n\n## Agents\n\n- **worker** — works\n", encoding="utf-8")
            issues = check_system(root)
            self.assertTrue(any("frontmatter" in i.lower() for i in issues), issues)

    def test_missing_distro_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "SYSTEM.md").write_text(
                "---\ndistro: test-distro\ndomain: testing\n---\n"
                "# SYSTEM\n\n## Stages\n\n"
                "| Stage | Entry Gate | Artifacts | Exit Gate |\n"
                "|---|---|---|---|\n"
                "| plan | req | plan | approved |\n\n"
                "## Agents\n\n- **worker** — does the work\n"
            , encoding="utf-8")
            issues = check_system(root)
            self.assertTrue(any("distro-version" in i for i in issues), issues)

    def test_missing_agents_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "SYSTEM.md").write_text(
                "---\ndistro: test-distro\ndistro-version: 0.1.0\ndomain: testing\n---\n"
                "# SYSTEM\n\n## Stages\n\n"
                "| Stage | Entry Gate | Artifacts | Exit Gate |\n"
                "|---|---|---|---|\n"
                "| plan | req | plan | approved |\n"
            , encoding="utf-8")
            issues = check_system(root)
            self.assertTrue(any("## Agents" in i or "Agents" in i for i in issues), issues)

    def test_agent_not_listed_in_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            # Add a second agent file not listed in SYSTEM.md
            (root / "agents" / "rogue.md").write_text(
                "---\nname: rogue\nrole: subagent\nstages: [build]\n---\n# Rogue\n"
            , encoding="utf-8")
            issues = check_system(root)
            self.assertTrue(any("rogue" in i for i in issues), issues)


# ---------------------------------------------------------------------------
# Coverage checks (3 tests)
# ---------------------------------------------------------------------------

class TestCheckCoverage(unittest.TestCase):

    def test_valid_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            issues = check_coverage(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")

    def test_agent_missing_from_context_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            # Add agent not in context-map
            (root / "agents" / "ghost.md").write_text(
                "---\nname: ghost\nrole: subagent\nstages: [build]\n---\n# Ghost\n"
            , encoding="utf-8")
            # Also list ghost in SYSTEM.md so system check passes
            (root / "SYSTEM.md").write_text(
                "---\ndistro: test-distro\ndistro-version: 0.1.0\ndomain: testing\n---\n"
                "# SYSTEM\n\n## Stages\n\n"
                "| Stage | Entry Gate | Artifacts | Exit Gate |\n"
                "|---|---|---|---|\n"
                "| plan | user request | plan doc | plan approved |\n"
                "| build | plan approved | built artifact | tests pass |\n\n"
                "## Agents\n\n- **worker** — does the work\n- **ghost** — haunts\n"
            , encoding="utf-8")
            issues = check_coverage(root)
            self.assertTrue(any("ghost" in i for i in issues), issues)

    def test_missing_context_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "context-map.md").unlink()
            issues = check_coverage(root)
            self.assertTrue(any("context-map" in i.lower() for i in issues), issues)


# ---------------------------------------------------------------------------
# Stages checks (3 tests)
# ---------------------------------------------------------------------------

class TestCheckStages(unittest.TestCase):

    def test_valid_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            issues = check_stages(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")

    def test_missing_stages_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "SYSTEM.md").write_text(
                "---\ndistro: test-distro\ndistro-version: 0.1.0\ndomain: testing\n---\n"
                "# SYSTEM\n\n## Agents\n\n- **worker** — does the work\n"
            , encoding="utf-8")
            issues = check_stages(root)
            self.assertTrue(any("Stages" in i or "stages" in i.lower() for i in issues), issues)

    def test_empty_stages_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "SYSTEM.md").write_text(
                "---\ndistro: test-distro\ndistro-version: 0.1.0\ndomain: testing\n---\n"
                "# SYSTEM\n\n## Stages\n\n"
                "| Stage | Entry Gate | Artifacts | Exit Gate |\n"
                "|---|---|---|---|\n\n"
                "## Agents\n\n- **worker** — does the work\n"
            , encoding="utf-8")
            issues = check_stages(root)
            self.assertTrue(any("empty" in i.lower() or "row" in i.lower() or "stage" in i.lower() for i in issues), issues)


# ---------------------------------------------------------------------------
# Hooks checks (3 tests)
# ---------------------------------------------------------------------------

class TestCheckHooks(unittest.TestCase):

    def test_valid_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            issues = check_hooks(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")

    def test_hook_missing_from_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "hooks" / "pre-build.md").write_text(
                "---\nname: pre-build\nto-stage: build\n---\n# Pre-Build\n"
            , encoding="utf-8")
            issues = check_hooks(root)
            self.assertTrue(any("from-stage" in i for i in issues), issues)

    def test_hook_references_invalid_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            (root / "hooks" / "pre-build.md").write_text(
                "---\nname: pre-build\nfrom-stage: nonexistent\nto-stage: build\n---\n# Pre-Build\n"
            , encoding="utf-8")
            issues = check_hooks(root)
            self.assertTrue(any("nonexistent" in i for i in issues), issues)


# ---------------------------------------------------------------------------
# Skills checks (2 tests)
# ---------------------------------------------------------------------------

class TestCheckSkills(unittest.TestCase):

    def test_valid_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            issues = check_skills(root)
            self.assertEqual(issues, [], f"Expected no issues, got: {issues}")

    def test_agent_with_no_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            # Add agent with no matching skill
            (root / "agents" / "lonely.md").write_text(
                "---\nname: lonely\nrole: subagent\nstages: [build]\n---\n# Lonely\n"
            , encoding="utf-8")
            # Also list lonely in SYSTEM.md
            (root / "SYSTEM.md").write_text(
                "---\ndistro: test-distro\ndistro-version: 0.1.0\ndomain: testing\n---\n"
                "# SYSTEM\n\n## Stages\n\n"
                "| Stage | Entry Gate | Artifacts | Exit Gate |\n"
                "|---|---|---|---|\n"
                "| plan | user request | plan doc | plan approved |\n"
                "| build | plan approved | built artifact | tests pass |\n\n"
                "## Agents\n\n- **worker** — does the work\n- **lonely** — has no skills\n"
            , encoding="utf-8")
            issues = check_skills(root)
            self.assertTrue(any("lonely" in i for i in issues), issues)


# ---------------------------------------------------------------------------
# inspect_distro orchestrator (2 tests)
# ---------------------------------------------------------------------------

class TestInspectDistro(unittest.TestCase):

    def test_valid_all_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            results = inspect_distro(root)
            for gate, issues in results.items():
                self.assertEqual(issues, [], f"Gate '{gate}' failed: {issues}")

    def test_returns_dict_with_expected_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_valid_distro(root)
            results = inspect_distro(root)
            expected_keys = {"structural", "system", "coverage", "stages", "hooks", "skills"}
            self.assertEqual(set(results.keys()), expected_keys)


if __name__ == "__main__":
    unittest.main()
