#!/usr/bin/env python3
"""Automated Unit & Smoke Tests for ThreeUI Skill."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(HERE, "..")
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import threeui  # noqa: E402


class TestThreeUICatalogIntegrity(unittest.TestCase):
    def test_catalog_loads_104_components(self):
        catalog = threeui.load_catalog()
        self.assertEqual(len(catalog), 104, f"Expected 104 components, got {len(catalog)}")

    def test_categories_presence(self):
        cats = threeui.list_categories()
        expected = {
            "Backgrounds", "Buttons", "Three.js", "Text Animation",
            "UI Elements", "CSS", "Hero", "Landing Pages", "Sections"
        }
        self.assertTrue(expected.issubset(set(cats.keys())), f"Missing expected categories: {expected - set(cats.keys())}")
        self.assertGreaterEqual(cats["Backgrounds"], 25)
        self.assertGreaterEqual(cats["Buttons"], 15)

    def test_components_have_valid_fields(self):
        catalog = threeui.load_catalog()
        for c in catalog:
            cid = c.get("id")
            self.assertTrue(cid, "Component missing ID")
            self.assertTrue(c.get("label"), f"Component {cid} missing label")
            self.assertTrue(c.get("category"), f"Component {cid} missing category")
            self.assertTrue(c.get("runtime"), f"Component {cid} missing runtime")


class TestThreeUISearch(unittest.TestCase):
    def test_search_liquid(self):
        results = threeui.search_components("liquid")
        self.assertGreater(len(results), 0)
        ids = [c["id"] for c in results]
        self.assertIn("liquid-form", ids)

    def test_search_category_filter(self):
        results = threeui.search_components("button", category="Buttons")
        self.assertGreater(len(results), 0)
        for c in results:
            self.assertEqual(c["category"], "Buttons")

    def test_search_globe(self):
        results = threeui.search_components("globe")
        self.assertGreater(len(results), 0)
        ids = [c["id"] for c in results]
        self.assertIn("energy-orb", ids)


class TestThreeUISourceFiles(unittest.TestCase):
    def test_liquid_form_source_files(self):
        comp = threeui.find_component("liquid-form")
        self.assertIsNotNone(comp)
        files = threeui.get_component_files(comp)
        self.assertGreater(len(files), 0)
        file_names = [f.name for f in files]
        self.assertIn("LiquidFormBackground.tsx", file_names)
        self.assertIn("liquidFormShaders.ts", file_names)

    def test_spark_badge_source_files(self):
        comp = threeui.find_component("spark-badge")
        self.assertIsNotNone(comp)
        files = threeui.get_component_files(comp)
        self.assertGreater(len(files), 0)
        file_names = [f.name for f in files]
        self.assertIn("SparkBadge.tsx", file_names)


class TestThreeUICLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.cli = os.path.join(SCRIPTS_DIR, "threeui.py")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_cli_search(self):
        res = subprocess.run([sys.executable, "-B", self.cli, "search", "liquid"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("liquid-form", res.stdout)

    def test_cli_categories(self):
        import argparse, io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            threeui.cmd_categories(argparse.Namespace(json=False))
        self.assertIn("ThreeUI Component Categories", f.getvalue())
        self.assertIn("Total Components: 104", f.getvalue())

    def test_cli_info(self):
        import argparse, io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            threeui.cmd_info(argparse.Namespace(id="liquid-form", json=False))
        self.assertIn("Liquid Form (liquid-form)", f.getvalue())
        self.assertIn("Controls & Uniforms", f.getvalue())

    def test_cli_export(self):
        import argparse, io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            threeui.cmd_export(argparse.Namespace(id="liquid-form", output_dir=self.tmp, json=True))
        self.assertTrue(os.path.isfile(os.path.join(self.tmp, "LiquidFormBackground.tsx")))
        self.assertTrue(os.path.isfile(os.path.join(self.tmp, "liquidFormShaders.ts")))


if __name__ == "__main__":
    unittest.main()
