import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(HERE, "..")
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)
import design_system  # noqa: E402


class TestDesignSystemsRegistry(unittest.TestCase):
    def test_registry_contains_67_themes(self):
        index = design_system.load_index()
        self.assertEqual(len(index), 67, f"Expected 67 themes, got {len(index)}")

    def test_all_themes_have_valid_files(self):
        index = design_system.load_index()
        for slug in index:
            skill_md, design_md = design_system.get_skill_files(slug)
            self.assertIsNotNone(skill_md, f"Missing SKILL.md for {slug}")
            self.assertTrue(os.path.isfile(skill_md), f"Not a file: {skill_md}")
            self.assertGreater(os.path.getsize(skill_md), 0, f"Empty SKILL.md: {slug}")

            self.assertIsNotNone(design_md, f"Missing DESIGN.md for {slug}")
            self.assertTrue(os.path.isfile(design_md), f"Not a file: {design_md}")
            self.assertGreater(os.path.getsize(design_md), 0, f"Empty DESIGN.md: {slug}")

    def test_tokens_extraction(self):
        skill_file, design_file = design_system.get_skill_files("glassmorphism")
        self.assertTrue(os.path.isfile(design_file))
        with open(design_file, "r", encoding="utf-8") as f:
            content = f.read()
        fm, _ = design_system.parse_frontmatter(content)
        self.assertEqual(fm.get("name"), "Glassmorphism")
        colors = fm.get("colors", {})
        self.assertEqual(colors.get("primary"), "#1856FF")

    def test_search_functionality(self):
        index = design_system.load_index()
        self.assertIn("glassmorphism", index)
        self.assertIn("brutalism", index)
        self.assertIn("neobrutalism", index)
        self.assertIn("claymorphism", index)
        self.assertIn("editorial", index)

    def test_cli_export_css(self):
        cli = os.path.join(SCRIPTS_DIR, "design_system.py")
        res = subprocess.run([sys.executable, "-B", cli, "export-css", "glassmorphism"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("--color-primary: #1856FF;", res.stdout)
        self.assertIn("--radius-md: 8px;", res.stdout)


if __name__ == "__main__":
    unittest.main()
