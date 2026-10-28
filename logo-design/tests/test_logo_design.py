#!/usr/bin/env python3
"""Automated Unit & Smoke Tests for Logo Design Skill."""

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
LIB_DIR = SKILL_DIR / "assets" / "library" / "svg"

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

TEST_SYMBOL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>Test symbol</title>
<circle cx="128" cy="128" r="96" fill="#0F7C80"/>
<path d="M80 150 L176 146 L176 170 L80 174 Z" fill="#FFFFFF"/></svg>
"""

TEST_LOCKUP = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 256"><title>Test lockup</title>
<circle cx="128" cy="128" r="96" fill="#0F7C80"/>
<rect x="280" y="100" width="560" height="56" rx="8" fill="#161616"/></svg>
"""


class TestLogoDesignSkillStructure(unittest.TestCase):
    def test_skill_md_frontmatter(self):
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.is_file(), "SKILL.md must exist")
        content = skill_md.read_text(encoding="utf-8")
        m = re.match(r"---\nname: (.+)\ndescription: (.+?)\n---", content, re.DOTALL)
        self.assertIsNotNone(m, "SKILL.md must have valid YAML frontmatter")
        self.assertEqual(m.group(1).strip(), "logo-design")
        self.assertGreater(len(m.group(2).strip()), 20)

    def test_references_completeness(self):
        expected_references = [
            "color.md",
            "critique.md",
            "discovery-brief.md",
            "identity-system.md",
            "library-guide.md",
            "mark-types.md",
            "presentation-delivery.md",
            "principles.md",
            "process.md",
            "redesign.md",
            "svg-construction.md",
            "testing-checklist.md",
            "typography.md",
            "visual-techniques.md",
        ]
        for ref in expected_references:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Missing reference: {ref}")
            self.assertGreater(ref_path.stat().st_size, 500, f"Reference {ref} is empty")

    def test_catalog_assets_exist(self):
        catalog_json = SKILL_DIR / "assets" / "library" / "catalog.json"
        classifications_json = SKILL_DIR / "assets" / "library" / "classifications.json"
        self.assertTrue(catalog_json.is_file())
        self.assertTrue(classifications_json.is_file())


class TestLogoDesignScripts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="logo-test-")
        self.tmp_path = Path(self.tmp)
        self.sym_file = self.tmp_path / "a-symbol.svg"
        self.lock_file = self.tmp_path / "a-lockup.svg"
        self.sym_file.write_text(TEST_SYMBOL, encoding="utf-8")
        self.lock_file.write_text(TEST_LOCKUP, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run_py(self, script_name, args):
        script_path = SCRIPTS_DIR / script_name
        cmd = [sys.executable, "-B", str(script_path)] + args
        res = subprocess.run(cmd, cwd=str(SKILL_DIR), capture_output=True, text=True)
        return res

    def test_build_catalog_check(self):
        res = self._run_py("build_catalog.py", ["--check"])
        self.assertEqual(res.returncode, 0, f"build_catalog failed: {res.stderr}")
        self.assertIn("0 missing", res.stdout + res.stderr)

    def test_svg_audit(self):
        res = self._run_py("svg_audit.py", [str(self.sym_file), str(self.lock_file)])
        self.assertEqual(res.returncode, 0, f"svg_audit failed: {res.stderr}")
        self.assertIn("production-readiness score", res.stdout)

    def test_svg_audit_json(self):
        res = self._run_py("svg_audit.py", ["--json", str(self.sym_file)])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIsInstance(data, list)
        self.assertIn("score", data[0])

    def test_search_library_summary(self):
        res = self._run_py("search_library.py", ["--technique", "negative-space", "--summary"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("logos match", res.stdout)

    def test_search_library_json(self):
        res = self._run_py("search_library.py", ["--type", "letterform", "--format", "json", "--limit", "2"])
        self.assertEqual(res.returncode, 0)
        out = res.stdout.strip()
        start = out.index("[")
        data = json.loads(out[start:])
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_search_library_list_values(self):
        res = self._run_py("search_library.py", ["--list-values"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("mark_type:", res.stdout)

    def test_concept_sheet_generation(self):
        out_svg = self.tmp_path / "concepts.svg"
        res = self._run_py(
            "concept_sheet.py",
            [
                str(self.sym_file), str(self.sym_file),
                "--lockups", str(self.lock_file), str(self.lock_file),
                "--names", "Concept A", "Concept B",
                "--notes", "First.", "Second.",
                "--recommend", "1",
                "-o", str(out_svg)
            ]
        )
        self.assertEqual(res.returncode, 0, f"concept_sheet failed: {res.stderr}")
        self.assertTrue(out_svg.is_file(), "concepts.svg must be created")

    def test_preview_sheet_html(self):
        out_html = self.tmp_path / "preview.html"
        res = self._run_py(
            "preview_sheet.py",
            [
                str(self.sym_file), str(self.lock_file),
                "--refs-industry", "finance-banking",
                "-o", str(out_html)
            ]
        )
        self.assertEqual(res.returncode, 0, f"preview_sheet failed: {res.stderr}")
        self.assertTrue(out_html.is_file(), "preview.html must be created")

    def test_export_variants_svg(self):
        export_dir = self.tmp_path / "exports"
        res = self._run_py(
            "export_variants.py",
            [
                str(self.sym_file),
                "--out-dir", str(export_dir),
                "--mono", "#0F7C80",
                "--icon-bg", "#0F7C80"
            ]
        )
        self.assertEqual(res.returncode, 0, f"export_variants failed: {res.stderr}")
        self.assertTrue((export_dir / "a-symbol-black.svg").is_file() or (export_dir / "a-symbol-mono.svg").is_file())


if __name__ == "__main__":
    unittest.main()
