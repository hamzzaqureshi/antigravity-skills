#!/usr/bin/env python3
"""Automated Unit and Smoke Tests for Scrapling Skill and Helper CLI."""

import ast
import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from scrapling_helper import check_readiness, html_to_simple_markdown, mock_extraction, TEMPLATES


class TestScraplingSkill(unittest.TestCase):
    """Test suite for Scrapling skill structure and helper engine."""

    def test_skill_manifest_exists(self):
        skill_md = os.path.join(ROOT, "SKILL.md")
        self.assertTrue(os.path.exists(skill_md), "SKILL.md must exist")
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("name: scrapling", content)
        self.assertIn("description:", content)

    def test_reference_docs_exist(self):
        required_refs = [
            os.path.join(ROOT, "references", "fetching", "choosing.md"),
            os.path.join(ROOT, "references", "fetching", "stealthy.md"),
            os.path.join(ROOT, "references", "parsing", "adaptive.md"),
            os.path.join(ROOT, "references", "spiders", "architecture.md"),
            os.path.join(ROOT, "references", "building-rag-systems.md"),
        ]
        for ref in required_refs:
            self.assertTrue(os.path.exists(ref), f"Missing required reference: {ref}")

    def test_examples_syntax(self):
        examples_dir = os.path.join(ROOT, "examples")
        for f in os.listdir(examples_dir):
            if f.endswith(".py"):
                path = os.path.join(examples_dir, f)
                with open(path, "r", encoding="utf-8") as fp:
                    code = fp.read()
                # Verify Python syntax compiles cleanly
                ast.parse(code, filename=f)

    def test_check_readiness(self):
        status = check_readiness()
        self.assertIn("scrapling_installed", status)
        self.assertIn("install_command", status)
        self.assertIn("pip install", status["install_command"])

    def test_html_to_markdown_converter(self):
        html = "<h1>Test</h1><p>Paragraph with <a href='https://link.com'>Link</a></p>"
        md = html_to_simple_markdown(html)
        self.assertIn("# Test", md)
        self.assertIn("[Link](https://link.com)", md)

    def test_mock_extraction(self):
        res = mock_extraction("https://example.com/api")
        self.assertIn("Scrapling Mock Data", res)
        self.assertIn("Cloudflare bypass", res)

    def test_cli_readiness(self):
        cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "scrapling_helper.py"), "readiness", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertIn("scrapling_installed", data)

    def test_cli_snippet(self):
        for t in ["static", "stealth", "spider", "rag"]:
            cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "scrapling_helper.py"), "snippet", t]
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(proc.returncode, 0)
            self.assertIn("scrapling", proc.stdout)

    def test_cli_extract_mock(self):
        cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "scrapling_helper.py"), "extract", "--mock", "--markdown"]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Scrapling Mock Data", proc.stdout)


if __name__ == "__main__":
    unittest.main()

