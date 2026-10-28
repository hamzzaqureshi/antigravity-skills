#!/usr/bin/env python3
"""Automated Unit Tests for Rigor Skill & Engine (Antigravity Suite)."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
BIN_DIR = SKILL_DIR / "bin"
REFERENCES_DIR = SKILL_DIR / "references"

sys.path.insert(0, str(SCRIPTS_DIR))
import rigor_engine


class TestRigor(unittest.TestCase):
    """Comprehensive test suite covering the 4 Rigor gates, ledger, and CLI."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_skill_and_references_exist(self):
        """Verify SKILL.md and all 4 reference specifications exist."""
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md missing")
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("name: rigor", content)
        self.assertIn("Completion Gate", content)
        self.assertIn("Grounding Protocol", content)

        expected_refs = [
            "completion-gate-table.md",
            "grounding-ladder.md",
            "cross-model-brief.md",
            "task-ledger-spec.md",
        ]
        for ref in expected_refs:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.exists(), f"Reference file missing: {ref}")
            self.assertGreater(ref_path.stat().st_size, 100)

    def test_02_workspace_initialization(self):
        """Verify cmd_workspace creates directory structure and gitignore."""
        plan_path = Path(self.temp_dir) / "demo-plan.md"
        plan_path.write_text("# Demo Plan\n\n## Task 1\nDo something.\n", encoding="utf-8")

        ws = rigor_engine.cmd_workspace(str(plan_path))
        ws_path = Path(ws)
        self.assertTrue(ws_path.is_dir())
        self.assertTrue((ws_path / "plan-path").exists())
        self.assertEqual((ws_path / "plan-path").read_text(encoding="utf-8").strip(), str(plan_path))

    def test_03_brief_extraction_success(self):
        """Verify extracting tasks from plan markdown."""
        plan_content = """# Feature Plan

## Task 1: Initialize Database
Create schema migrations.
### Step 1.1: Add Users Table
Run migration.

## Task 2: Implement Endpoints
Add REST handlers.

## Task 12: Performance Profiling
Run benchmark tests.

## Appendix
Out of scope.
"""
        plan_path = Path(self.temp_dir) / "plan.md"
        plan_path.write_text(plan_content, encoding="utf-8")

        ws = rigor_engine.cmd_workspace(str(plan_path))
        brief_1 = rigor_engine.cmd_brief(str(plan_path), "1", ws)
        content_1 = Path(brief_1).read_text(encoding="utf-8")

        self.assertIn("Task 1: Initialize Database", content_1)
        self.assertIn("Step 1.1: Add Users Table", content_1)
        self.assertNotIn("Task 2: Implement Endpoints", content_1)

        brief_12 = rigor_engine.cmd_brief(str(plan_path), "12", ws)
        content_12 = Path(brief_12).read_text(encoding="utf-8")
        self.assertIn("Task 12: Performance Profiling", content_12)
        self.assertNotIn("Appendix", content_12)

    def test_04_brief_fence_and_nested_headings(self):
        """Verify headings inside fenced code blocks are not treated as task boundaries."""
        plan_content = """# Complex Plan

## Task 1: Setup Documentation
Write the following markdown documentation:
```markdown
## Task 2: This is a fake heading in a code block
Do not break on this.
```
Follow up on documentation.

## Task 2: Actual Second Task
Real task content.
"""
        plan_path = Path(self.temp_dir) / "fenced_plan.md"
        plan_path.write_text(plan_content, encoding="utf-8")

        ws = rigor_engine.cmd_workspace(str(plan_path))
        brief_1 = rigor_engine.cmd_brief(str(plan_path), "1", ws)
        content_1 = Path(brief_1).read_text(encoding="utf-8")

        self.assertIn("This is a fake heading in a code block", content_1)
        self.assertIn("Follow up on documentation", content_1)
        self.assertNotIn("Actual Second Task", content_1)

    def test_05_brief_boundary_and_missing_task(self):
        """Verify invalid or missing task numbers raise descriptive errors."""
        plan_path = Path(self.temp_dir) / "mini_plan.md"
        plan_path.write_text("## Task 1: Hello\nWorld\n", encoding="utf-8")

        with self.assertRaises(ValueError):
            rigor_engine.cmd_brief(str(plan_path), "not_a_number")

        with self.assertRaises(ValueError):
            rigor_engine.cmd_brief(str(plan_path), "99")

    def test_06_ledger_and_status(self):
        """Verify progress ledger appending, header creation, and status computation."""
        plan_path = Path(self.temp_dir) / "ledger_plan.md"
        plan_path.write_text("## Task 1\nTest\n", encoding="utf-8")
        ws = rigor_engine.cmd_workspace(str(plan_path))

        rigor_engine.cmd_ledger(ws, "Task 1: complete (SHA: 111111)")
        rigor_engine.cmd_ledger(ws, "Ruling: approve architecture change")
        rigor_engine.cmd_ledger(ws, "Task 2: in_progress")

        status_text = rigor_engine.cmd_status(ws, as_json=False)
        self.assertIn("complete: 1", status_text)
        self.assertIn("next task: 2", status_text)
        self.assertIn("rulings: 1", status_text)

        status_json = rigor_engine.cmd_status(ws, as_json=True)
        self.assertIn('"completed_tasks": [\n    1\n  ]', status_json)
        self.assertIn('"next_task": 2', status_json)

    def test_07_review_package_git(self):
        """Verify git review package generation with commits, stats, and unified diff."""
        git_dir = Path(self.temp_dir) / "repo"
        git_dir.mkdir()
        subprocess.check_call(["git", "init", "-q", str(git_dir)])
        subprocess.check_call(["git", "-C", str(git_dir), "config", "user.name", "TestUser"])
        subprocess.check_call(["git", "-C", str(git_dir), "config", "user.email", "test@example.com"])

        file_a = git_dir / "sample.py"
        file_a.write_text("def test():\n    return 1\n", encoding="utf-8")
        subprocess.check_call(["git", "-C", str(git_dir), "add", "."])
        subprocess.check_call(["git", "-C", str(git_dir), "commit", "-qm", "initial commit"])
        base_sha = subprocess.check_output(["git", "-C", str(git_dir), "rev-parse", "HEAD"], text=True).strip()

        file_a.write_text("def test():\n    return 42\n", encoding="utf-8")
        subprocess.check_call(["git", "-C", str(git_dir), "commit", "-qam", "update test return value"])

        cwd_prev = os.getcwd()
        try:
            os.chdir(str(git_dir))
            pkg_path = rigor_engine.cmd_review_package(base_sha, "HEAD", str(git_dir / ".ws"))
            pkg_content = Path(pkg_path).read_text(encoding="utf-8")
            self.assertIn("## Commits", pkg_content)
            self.assertIn("## Files changed", pkg_content)
            self.assertIn("## Diff", pkg_content)
            self.assertIn("+    return 42", pkg_content)
        finally:
            os.chdir(cwd_prev)

    def test_08_review_package_error_cases(self):
        """Verify review package rejects empty commit range or invalid revisions."""
        git_dir = Path(self.temp_dir) / "repo_err"
        git_dir.mkdir()
        subprocess.check_call(["git", "init", "-q", str(git_dir)])
        subprocess.check_call(["git", "-C", str(git_dir), "config", "user.name", "TestUser"])
        subprocess.check_call(["git", "-C", str(git_dir), "config", "user.email", "test@example.com"])
        (git_dir / "f.txt").write_text("ok\n", encoding="utf-8")
        subprocess.check_call(["git", "-C", str(git_dir), "add", "."])
        subprocess.check_call(["git", "-C", str(git_dir), "commit", "-qm", "init"])

        cwd_prev = os.getcwd()
        try:
            os.chdir(str(git_dir))
            with self.assertRaises(ValueError):
                rigor_engine.cmd_review_package("HEAD", "HEAD")
        finally:
            os.chdir(cwd_prev)

    def test_09_verify_gate_claims_and_evidence(self):
        """Verify completion gate accepts supported claims and flags bare assertions."""
        # Bare claim without evidence -> Fail
        unsupported = "I have fixed the issue and all tests pass."
        res1 = rigor_engine.cmd_verify_gate(unsupported)
        self.assertFalse(res1["passed"])
        self.assertGreater(len(res1["claims"]), 0)

        # Supported claim with evidence output -> Pass
        supported = """I have resolved the bug.
Verification output:
```
pytest tests/
...
14 passed in 0.15s
exit 0
```
"""
        res2 = rigor_engine.cmd_verify_gate(supported)
        self.assertTrue(res2["passed"])
        self.assertGreater(res2["evidence_count"], 0)

    def test_10_verify_gate_evidence_table(self):
        """Verify strict mode enforcement for markdown evidence table."""
        text_with_table = """
| Claim | Command or check | Result |
|---|---|---|
| Tests pass | `pytest` | 10 passed, exit 0 |
All tests pass.
"""
        res_strict = rigor_engine.cmd_verify_gate(text_with_table, strict=True)
        self.assertTrue(res_strict["passed"])
        self.assertTrue(res_strict["evidence_table_present"])

        text_without_table = "All tests pass. 10 passed, exit 0."
        res_fail_strict = rigor_engine.cmd_verify_gate(text_without_table, strict=True)
        self.assertFalse(res_fail_strict["passed"])

    def test_11_ground_local_tool(self):
        """Verify grounding probe against local python binary."""
        info = rigor_engine.cmd_ground("python3")
        self.assertEqual(info["target"], "python3")
        self.assertGreater(len(info["findings"]), 0)
        has_cli = any(f.get("type") == "cli_binary" for f in info["findings"])
        self.assertTrue(has_cli)

    def test_12_cli_binary_execution(self):
        """Verify bin/rigor wrapper executes commands via CLI."""
        bin_path = BIN_DIR / "rigor"
        self.assertTrue(bin_path.exists())
        out = subprocess.check_output([str(bin_path), "--help"], text=True)
        self.assertIn("Rigor Engine", out)
        self.assertIn("workspace", out)
        self.assertIn("verify-gate", out)


if __name__ == "__main__":
    unittest.main()

