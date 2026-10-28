#!/usr/bin/env python3
"""Comprehensive Unit and Smoke Tests for last30days and CrowdPulse Fast-Lane."""

import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from pulse import fetch_pulse, format_pulse_markdown, mock_pulse


class TestCrowdPulseFastLane(unittest.TestCase):
    """Test suite for the zero-dependency CrowdPulse micro-sensor."""

    def test_mock_pulse_structure(self):
        data = mock_pulse("claude-code")
        self.assertEqual(data["query"], "claude-code")
        self.assertEqual(data["mode"], "mock")
        self.assertIn("reddit", data)
        self.assertIn("hackernews", data)
        self.assertIn("github", data)
        self.assertIn("polymarket", data)
        self.assertGreater(len(data["reddit"]), 0)
        self.assertGreater(len(data["hackernews"]), 0)
        self.assertGreater(len(data["github"]), 0)
        self.assertGreater(len(data["polymarket"]), 0)

    def test_fetch_pulse_mock_flag(self):
        res = fetch_pulse("antigravity", mock=True)
        self.assertEqual(res["query"], "antigravity")
        self.assertIn("r/technology", res["reddit"][0]["community"])
        self.assertIn("GitHub", res["github"][0]["source"])
        self.assertIn("Polymarket", res["polymarket"][0]["source"])

    def test_format_pulse_markdown(self):
        data = mock_pulse("system-design")
        md = format_pulse_markdown(data)
        self.assertIn("CrowdPulse: system-design", md)
        self.assertIn("Reddit Community Consensus", md)
        self.assertIn("Hacker News Developer Takes", md)
        self.assertIn("GitHub Open Source Activity", md)
        self.assertIn("Polymarket Real-Money Odds", md)

    def test_pulse_cli_json(self):
        cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "pulse.py"), "test-query", "--mock", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"pulse.py failed: {proc.stderr}")
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed["query"], "test-query")
        self.assertEqual(parsed["mode"], "mock")

    def test_pulse_cli_markdown(self):
        cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "pulse.py"), "test-query", "--mock"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("CrowdPulse: test-query", proc.stdout)


@unittest.skipIf(sys.version_info < (3, 12), "last30days v3 engine requires Python 3.12+")
class TestLast30DaysEngine(unittest.TestCase):
    """Test suite for the flagship last30days v3 engine."""

    def test_engine_preflight(self):
        cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "last30days.py"), "--preflight"]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, f"preflight failed: {proc.stderr}")
        self.assertIn("last30days preflight", proc.stdout)
        self.assertIn("Status: Ready to research", proc.stdout)

    def test_engine_mock_compact(self):
        cmd = [
            sys.executable, "-B", os.path.join(SCRIPTS_DIR, "last30days.py"),
            "react 19", "--mock", "--emit=compact"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, f"mock search failed: {proc.stderr}")
        self.assertIn("last30days v3", proc.stdout)
        self.assertIn("Ranked Evidence Clusters", proc.stdout)
        self.assertIn("All agents reported back", proc.stdout)

    def test_engine_mock_json(self):
        cmd = [
            sys.executable, "-B", os.path.join(SCRIPTS_DIR, "last30days.py"),
            "react 19", "--mock", "--emit=json"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, f"mock json search failed: {proc.stderr}")
        parsed = json.loads(proc.stdout)
        self.assertIn("query", parsed)
        self.assertEqual(parsed["query"], "react 19")
        self.assertIn("clusters", parsed)


if __name__ == "__main__":
    unittest.main()
