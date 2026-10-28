#!/usr/bin/env python3
"""Automated Unit and Smoke Tests for UI/UX Pro Max Skill."""

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

from core import search, search_stack, AVAILABLE_STACKS, CSV_CONFIG  # noqa: E402
from design_system import generate_design_system  # noqa: E402


class TestUIUXProMaxCore(unittest.TestCase):
    def test_domain_search_style(self):
        res = search("glassmorphism", domain="style")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "style")
        self.assertGreater(len(res["results"]), 0)
        first = res["results"][0]
        self.assertIn("Style ID", first)

    def test_domain_search_color(self):
        res = search("fintech banking", domain="color")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "color")
        self.assertGreater(len(res["results"]), 0)
        first = res["results"][0]
        self.assertIn("Primary", first)
        self.assertIn("Background", first)

    def test_domain_search_typography(self):
        res = search("editorial serif", domain="typography")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "typography")
        self.assertGreater(len(res["results"]), 0)
        first = res["results"][0]
        self.assertIn("Heading Font", first)

    def test_domain_search_charts(self):
        res = search("analytics dashboard metrics", domain="chart")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "chart")
        self.assertGreater(len(res["results"]), 0)
        first = res["results"][0]
        self.assertIn("Best Chart Type", first)

    def test_domain_search_ux(self):
        res = search("error summary validation", domain="ux")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "ux")
        self.assertGreater(len(res["results"]), 0)
        first = res["results"][0]
        self.assertIn("Do", first)
        self.assertIn("Don't", first)

    def test_domain_search_icons(self):
        res = search("shield security", domain="icons")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "icons")
        self.assertGreater(len(res["results"]), 0)
        first = res["results"][0]
        self.assertIn("Icon Name", first)

    def test_domain_search_motion(self):
        res = search("stagger reveal", domain="gsap")
        self.assertNotIn("error", res)
        self.assertEqual(res["domain"], "gsap")
        self.assertGreater(len(res["results"]), 0)


class TestUIUXProMaxStacks(unittest.TestCase):
    def test_available_stacks_count(self):
        self.assertGreaterEqual(len(AVAILABLE_STACKS), 22)

    def test_stack_search_react(self):
        res = search_stack("form validation", "react")
        self.assertNotIn("error", res)
        self.assertEqual(res["stack"], "react")
        self.assertGreater(len(res["results"]), 0)

    def test_stack_search_tailwind(self):
        res = search_stack("responsive container", "html-tailwind")
        self.assertNotIn("error", res)
        self.assertEqual(res["stack"], "html-tailwind")
        self.assertGreater(len(res["results"]), 0)

    def test_stack_search_swiftui(self):
        res = search_stack("navigation sheet", "swiftui")
        self.assertNotIn("error", res)
        self.assertEqual(res["stack"], "swiftui")
        self.assertGreater(len(res["results"]), 0)


class TestUIUXProMaxDesignSystem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_design_system_generation_dict(self):
        res = generate_design_system("beauty spa wellness", "Serenity Spa")
        self.assertNotIn("error", res)
        sys_data = res["design_system"]
        self.assertIn("pattern", sys_data)
        self.assertIn("style", sys_data)
        self.assertIn("colors", sys_data)
        self.assertIn("typography", sys_data)
        self.assertIn("anti_patterns", sys_data)

    def test_design_system_text_output(self):
        res = generate_design_system("fintech banking", "FinSecure")
        self.assertIn("TARGET: FinSecure", res["text"])
        self.assertIn("RECOMMENDED DESIGN SYSTEM", res["text"])

    def test_design_system_dials(self):
        res = generate_design_system(
            "developer analytics dashboard",
            "DevOps Pro",
            variance=9,
            motion=8,
            density=9
        )
        self.assertNotIn("error", res)
        sys_data = res["design_system"]
        self.assertIn("motion_snippet", sys_data)
        self.assertIsNotNone(sys_data["motion_snippet"])
        self.assertEqual(sys_data.get("dials", {}).get("density"), 9)

    def test_design_system_persistence(self):
        res = generate_design_system(
            "SaaS project manager",
            "TaskFlow",
            persist=True,
            output_dir=self.tmp
        )
        self.assertNotIn("error", res)
        master_file = os.path.join(self.tmp, "design-system", "taskflow", "MASTER.md")
        self.assertTrue(os.path.isfile(master_file))
        with open(master_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("# Design System Master File", content)
        self.assertIn("**Project:** TaskFlow", content)
        self.assertIn("## Color Palette", content)

    def test_design_system_page_override(self):
        res = generate_design_system(
            "SaaS project manager",
            "TaskFlow",
            persist=True,
            output_dir=self.tmp,
            page="billing"
        )
        self.assertNotIn("error", res)
        page_file = os.path.join(self.tmp, "design-system", "taskflow", "pages", "billing.md")
        self.assertTrue(os.path.isfile(page_file))
        with open(page_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Billing Page Overrides", content)
        self.assertIn("**PROJECT:** TaskFlow", content)


class TestUIUXProMaxCLI(unittest.TestCase):
    def test_cli_search_domain(self):
        cli = os.path.join(SCRIPTS_DIR, "search.py")
        res = subprocess.run(
            [sys.executable, "-B", cli, "glassmorphism", "--domain", "style"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("UI Pro Max Search Results", res.stdout)
        self.assertIn("glassmorphism", res.stdout.lower())

    def test_cli_search_markdown_design_system(self):
        import search
        res = search.search("fintech banking")
        formatted = search.format_output(res, full=True)
        self.assertIn("UI Pro Max Search Results", formatted)

    def test_data_integrity_validation(self):
        import validate_data
        problems = validate_data.validate()
        self.assertEqual(problems, [], f"Data validation issues: {problems}")


if __name__ == "__main__":
    unittest.main()
