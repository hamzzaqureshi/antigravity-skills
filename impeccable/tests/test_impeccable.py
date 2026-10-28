import json
import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(HERE, "..")
LAUNCHER = os.path.join(SKILL_ROOT, "scripts", "impeccable")


class TestImpeccableSkill(unittest.TestCase):
    def test_launcher_help(self):
        self.assertTrue(os.path.exists(LAUNCHER), "Launcher not found: %s" % LAUNCHER)
        res = subprocess.run([LAUNCHER, "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("impeccable", res.stdout)

    def test_detect_command(self):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write("<!DOCTYPE html><html><body><h1>Clean Title</h1></body></html>")
            path = f.name
        try:
            res = subprocess.run([LAUNCHER, "detect", path], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_command_metadata(self):
        meta_path = os.path.join(SKILL_ROOT, "scripts", "command-metadata.json")
        self.assertTrue(os.path.exists(meta_path))
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cmd_names = set(data.keys())
        for expected in ["init", "polish", "audit", "critique", "overdrive", "distill"]:
            self.assertIn(expected, cmd_names)

    def test_creative_stack_reference(self):
        ref_path = os.path.join(SKILL_ROOT, "reference", "creative-stack.md")
        self.assertTrue(os.path.exists(ref_path))
        with open(ref_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ShaderGradient", content)
        self.assertIn("Liquid Glass", content)
        self.assertIn("Liquid Logo", content)
        self.assertIn("React Three Fiber", content)


if __name__ == "__main__":
    unittest.main()
