#!/usr/bin/env python3
"""Automated Unit & Smoke Tests for Writing-README Skill."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
REFERENCES_DIR = SKILL_DIR / "references"
TEMPLATES_DIR = SKILL_DIR / "templates"

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(SCRIPTS_DIR))
import readme_audit  # noqa: E402
import generate_readme  # noqa: E402


class TestWritingReadmeSkillStructure(unittest.TestCase):
    def test_skill_md_frontmatter(self):
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.is_file(), "SKILL.md must exist")
        content = skill_md.read_text(encoding="utf-8")
        m = re.match(r"---\nname: (.+)\ndescription: (.+?)\n---", content, re.DOTALL)
        self.assertIsNotNone(m, "SKILL.md must have valid YAML frontmatter")
        self.assertEqual(m.group(1).strip(), "writing-readme")
        self.assertGreater(len(m.group(2).strip()), 20)

    def test_references_completeness(self):
        expected_references = [
            "principles-and-journey.md",
            "archetypes-and-tailoring.md",
            "reproducibility-and-setup.md",
            "architecture-and-visuals.md",
            "quality-scorecard.md",
            "maintenance-and-evolution.md",
        ]
        for ref in expected_references:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Missing reference: {ref}")
            self.assertGreater(ref_path.stat().st_size, 300, f"Reference {ref} is empty")

    def test_templates_completeness(self):
        expected_templates = [
            "standard.md",
            "ai-ml.md",
            "backend-infra.md",
            "cli-tool.md",
            "library.md",
            "web-app.md",
        ]
        for tmpl in expected_templates:
            tmpl_path = TEMPLATES_DIR / tmpl
            self.assertTrue(tmpl_path.is_file(), f"Missing template: {tmpl}")
            content = tmpl_path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("# "), f"Template {tmpl} must begin with H1 title")


class TestReadmeAuditEngine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="readme-test-")
        self.tmp_path = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_audit_pristine_readme(self):
        pristine = self.tmp_path / "README.md"
        pristine.write_text("""# AwesomeApp

> High-performance real-time telemetry processor.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview
AwesomeApp solves the problem of high-throughput log processing with zero latency.

## Prerequisites
- Python >= 3.10

## Installation
```bash
pip install awesomeapp
```

## Usage
```bash
awesomeapp run --config config.yaml
# Output: [INFO] Server started on port 8080
```

## Architecture
```text
[Input Stream] ──▶ [Processor] ──▶ [Dashboard]
```

## Testing
```bash
pytest tests/
```

## License
MIT
""", encoding="utf-8")

        result = readme_audit.audit_readme(pristine, check_links=False)
        self.assertGreaterEqual(result["total_score"], 35)
        self.assertTrue(result["passed"])
        self.assertEqual(len(result["critical_defects"]), 0)

    def test_audit_defective_readme(self):
        broken = self.tmp_path / "BROKEN.md"
        broken.write_text("""# App

TODO: write description. Replace this with your-username.
""", encoding="utf-8")

        result = readme_audit.audit_readme(broken, check_links=False)
        self.assertLess(result["total_score"], 30)
        self.assertFalse(result["passed"])
        self.assertIn("accuracy", result["feedback"])
        self.assertIn("installation", result["feedback"])


class TestGenerateReadmeEngine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gen-test-")
        self.tmp_path = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generate_all_archetypes(self):
        for archetype in generate_readme.ARCHETYPES:
            raw = generate_readme.load_template(archetype)
            rendered = generate_readme.render_template(raw, {
                "name": "TestProject",
                "owner": "testuser",
                "repo": "test-repo",
                "description": "A high-performance modular pipeline.",
                "license": "MIT",
            })
            self.assertIn("# TestProject", rendered)
            self.assertIn("testuser", rendered)
            self.assertIn("test-repo", rendered)

    def test_generate_cli_tool_file(self):
        out_file = self.tmp_path / "CLI_README.md"
        raw = generate_readme.load_template("cli-tool")
        rendered = generate_readme.render_template(raw, {
            "name": "FastPurge",
            "owner": "ops-team",
            "repo": "fastpurge",
            "description": "Zero-dependency log trimmer.",
            "license": "Apache-2.0",
        })
        out_file.write_text(rendered, encoding="utf-8")
        self.assertTrue(out_file.is_file())
        self.assertIn("fastpurge", out_file.read_text(encoding="utf-8"))


class TestReadmeCLIExecution(unittest.TestCase):
    def test_audit_cli_smoke(self):
        cli = SCRIPTS_DIR / "readme_audit.py"
        target = SKILL_DIR / "README.md"
        res = subprocess.run([sys.executable, "-B", str(cli), str(target), "--json"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"readme_audit CLI failed: {res.stderr}")
        data = json.loads(res.stdout)
        self.assertIn("total_score", data)
        self.assertTrue(data["passed"])

    def test_generate_cli_smoke(self):
        cli = SCRIPTS_DIR / "generate_readme.py"
        res = subprocess.run([sys.executable, "-B", str(cli), "--archetype", "library", "--name", "QuickMath"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("# QuickMath", res.stdout)


if __name__ == "__main__":
    unittest.main()
