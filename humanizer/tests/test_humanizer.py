#!/usr/bin/env python3
"""Automated Unit & Smoke Tests for Humanizer Skill and Audit Scanner."""

import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from humanize_audit import audit_text, PATTERNS


class TestHumanizerSkill(unittest.TestCase):
    """Test suite for Humanizer skill and 26-tell prose auditor."""

    def test_skill_manifest_exists(self):
        skill_md = os.path.join(ROOT, "SKILL.md")
        self.assertTrue(os.path.exists(skill_md), "SKILL.md must exist")
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("name: humanizer", content)
        self.assertIn("description:", content)

    def test_package_validator(self):
        val_script = os.path.join(SCRIPTS_DIR, "validate-package.py")
        proc = subprocess.run([sys.executable, "-B", val_script], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, f"validate-package.py failed: {proc.stderr}")
        self.assertIn("valid", proc.stdout)

    def test_detect_not_x_but_y(self):
        text = "It's not just a framework, it's a paradigm shift."
        res = audit_text(text)
        self.assertGreater(res["findings_count"], 0)
        self.assertTrue(any(f["pattern_name"] == "Not X but Y contrast" for f in res["findings"]))
        self.assertLess(res["score"], 100)

    def test_detect_closer_and_buzzwords(self):
        text = "We will delve into this landscape. Let that sink in."
        res = audit_text(text)
        self.assertGreater(res["findings_count"], 0)
        names = [f["pattern_name"] for f in res["findings"]]
        self.assertIn("One-line dramatic closer", names)
        self.assertIn("Stock AI buzzwords", names)

    def test_clean_human_text_scores_100(self):
        clean_text = "The server returned a 404 error because the endpoint path changed in v2."
        res = audit_text(clean_text)
        self.assertEqual(res["score"], 100)
        self.assertEqual(res["findings_count"], 0)
        self.assertIn("Clean Human Prose", res["grade"])

    def test_cli_json_output(self):
        cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "humanize_audit.py"), "--json"]
        sample_input = "Honestly? It depends. It's not just fast, it's revolutionary."
        proc = subprocess.run(cmd, input=sample_input, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        parsed = json.loads(proc.stdout)
        self.assertIn("score", parsed)
        self.assertIn("findings", parsed)
        self.assertGreater(len(parsed["findings"]), 0)


if __name__ == "__main__":
    unittest.main()

