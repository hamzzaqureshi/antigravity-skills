import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(HERE, "..")
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)
import artist  # noqa: E402


class TestStealLikeAnArtist(unittest.TestCase):
    def setUp(self):
        self.old_cwd = os.getcwd()
        self.tmp = tempfile.mkdtemp()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp)

    def test_init_creates_files(self):
        artist.ensure_init()
        artist_dir = os.path.join(self.tmp, ".artist")
        self.assertTrue(os.path.isdir(artist_dir))
        self.assertTrue(os.path.isfile(os.path.join(artist_dir, "ideas.json")))
        self.assertTrue(os.path.isfile(os.path.join(artist_dir, "lineage.json")))
        self.assertTrue(os.path.isfile(os.path.join(artist_dir, "logbook.md")))

    def test_capture_idea_card(self):
        parser = artist.build_parser()
        args = parser.parse_args([
            "capture",
            "--title", "Monospace HUD",
            "--problem", "Cluttered UI obscures terminal telemetry",
            "--source", "Bloomberg Terminal & Quake HUD",
            "--source-type", "ui",
            "--mechanism", "High contrast fixed-width text overlay",
            "--adaptation", "Adapt into an unobtrusive status banner",
            "--tags", "ui,hud,telemetry"
        ])
        artist.cmd_capture(args)

        ideas_file = os.path.join(self.tmp, ".artist", "ideas.json")
        with open(ideas_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data["ideas"]), 1)
        card = data["ideas"][0]
        self.assertEqual(card["title"], "Monospace HUD")
        self.assertEqual(card["source"], "Bloomberg Terminal & Quake HUD")
        self.assertIn("telemetry", card["tags"])

    def test_lineage_tracking(self):
        parser = artist.build_parser()
        args = parser.parse_args([
            "lineage",
            "--add", "Unix Pipeline",
            "--category", "direct",
            "--mechanism", "Composable standard streams"
        ])
        artist.cmd_lineage(args)

        lineage_file = os.path.join(self.tmp, ".artist", "lineage.json")
        with open(lineage_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data["lineage"]), 1)
        node = data["lineage"][0]
        self.assertEqual(node["name"], "Unix Pipeline")
        self.assertEqual(node["category"], "direct")

    def test_logbook_entry(self):
        parser = artist.build_parser()
        args = parser.parse_args([
            "log",
            "--worked", "Refactored lineage parser",
            "--learned", "Pure standard library eliminates environment drift",
            "--built", "Zero-dependency CLI tool"
        ])
        artist.cmd_log(args)

        logbook_file = os.path.join(self.tmp, ".artist", "logbook.md")
        with open(logbook_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Daily Creative Log", content)
        self.assertIn("Refactored lineage parser", content)
        self.assertIn("Pure standard library", content)

    def test_audit_high_score_multi_influence(self):
        # Text with multiple influences, attribution, transformation, context, and clear delta
        text = """
        Idea: Fast Telemetry Parser
        Precedents & Prior Art: Inspired by the Redis event loop, Unix pipes, and NGINX buffer pools.
        Attribution: Original buffer ring concept by Igor Sysoev; pipeline mechanics from Ken Thompson.
        Mechanism Stolen: Fixed-size circular buffer and zero-copy slicing.
        Transformation: Repurposed from network sockets to local IPC file streaming under strict memory constraints.
        Project Context & Constraint: Limited to Python 3 standard library with zero external pip dependencies.
        Independent Value & Delta: 10x faster execution than legacy parser, zero network calls, completely offline.
        """
        parser = artist.build_parser()
        args = parser.parse_args(["audit", "--text", text, "--threshold", "70", "--json"])

        with self.assertRaises(SystemExit) as cm:
            artist.cmd_audit(args)
        self.assertEqual(cm.exception.code, 0)

    def test_audit_low_score_derivative_buzzwords(self):
        # Monolithic copy without transformation, no attribution, full of buzzwords
        bad_text = """
        Our product is an all-in-one revolutionary next-gen AI operating system that will disrupt everything.
        We copied the exact layout of Notion without changes.
        """
        parser = artist.build_parser()
        args = parser.parse_args(["audit", "--text", bad_text, "--threshold", "70", "--json"])

        with self.assertRaises(SystemExit) as cm:
            artist.cmd_audit(args)
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
