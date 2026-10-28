#!/usr/bin/env python3
"""Automated Unit and Smoke Tests for Ponytail Skill."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import debt  # noqa: E402
import gain  # noqa: E402
import help_card  # noqa: E402


class TestPonytailStructure(unittest.TestCase):
    def test_skill_md_frontmatter(self):
        skill_md = os.path.join(SKILL_DIR, "SKILL.md")
        self.assertTrue(os.path.isfile(skill_md))
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"---\nname:\s*([^\n]+)\ndescription:\s*>-\s*\n(.*?)\n---", content, re.DOTALL)
        self.assertIsNotNone(m, "SKILL.md must have valid YAML frontmatter")
        self.assertEqual(m.group(1).strip(), "ponytail")
        desc = m.group(2).strip()
        self.assertIn("lazy senior dev", desc.lower())
        self.assertIn("yagni", desc.lower())

    def test_references_exist(self):
        rev = os.path.join(SKILL_DIR, "references", "review.md")
        aud = os.path.join(SKILL_DIR, "references", "audit.md")
        self.assertTrue(os.path.isfile(rev))
        self.assertTrue(os.path.isfile(aud))


class TestPonytailDebtScanner(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ponytail-test-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_parse_shortcut_text(self):
        text = "in-memory list, ceiling: 100 items, upgrade: move to redis"
        parsed = debt.parse_shortcut_text(text)
        self.assertEqual(parsed["summary"], "in-memory list")
        self.assertEqual(parsed["ceiling"], "100 items")
        self.assertEqual(parsed["upgrade"], "move to redis")
        self.assertFalse(parsed["no_trigger"])

    def test_parse_shortcut_no_trigger(self):
        text = "simple dict cache without eviction"
        parsed = debt.parse_shortcut_text(text)
        self.assertTrue(parsed["no_trigger"])
        self.assertEqual(parsed["ceiling"], "unspecified")

    def test_scan_directory_hits(self):
        src_file = os.path.join(self.tmp, "service.py")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write("# Standard header\n")
            f.write("def process():\n")
            f.write("    # shortcut: hardcoded exchange rate, ceiling: 1 currency, upgrade: fetch live API\n")
            f.write("    return 1.25\n")
            f.write("// ponytail: quick fallback, when: db fails\n")

        hits = debt.scan_directory(self.tmp)
        self.assertEqual(len(hits), 2)
        self.assertEqual(hits[0]["line"], 3)
        self.assertIn("hardcoded exchange rate", hits[0]["summary"])
        self.assertEqual(hits[0]["ceiling"], "1 currency")
        self.assertFalse(hits[0]["no_trigger"])

        formatted = debt.format_ledger(hits)
        self.assertIn("Ponytail Debt Ledger", formatted)
        self.assertIn("hardcoded exchange rate", formatted)

    def test_clean_ledger_when_empty(self):
        hits = debt.scan_directory(self.tmp)
        self.assertEqual(len(hits), 0)
        formatted = debt.format_ledger(hits)
        self.assertEqual(formatted, "No shortcut debt. Clean ledger.")


class TestPonytailScripts(unittest.TestCase):
    def test_gain_scoreboard(self):
        self.assertIn("Lines of code", gain.SCOREBOARD)
        self.assertIn("Output tokens", gain.SCOREBOARD)
        self.assertIn("53%", gain.SCOREBOARD)

    def test_help_card_content(self):
        self.assertIn("Ponytail Quick Reference", help_card.HELP_TEXT)
        self.assertIn("/ponytail-review", help_card.HELP_TEXT)
        self.assertIn("YAGNI", help_card.HELP_TEXT)


if __name__ == "__main__":
    unittest.main()

