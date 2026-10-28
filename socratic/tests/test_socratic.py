#!/usr/bin/env python3
"""Automated Unit Tests for Socratic Skill (Antigravity Suite)."""

import os
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
QUESTIONS_DIR = SKILL_DIR / "questions"
PACKS_DIR = SKILL_DIR / "packs"
GRADES_DIR = SKILL_DIR / "grades"


class TestSocratic(unittest.TestCase):
    """Test suite covering Socratic domain detection, pack routing, gates, and CLI."""

    def test_01_all_15_domain_files_exist(self):
        """Verify all 15 full and core domain files exist."""
        expected_domains = [
            "00-requirements", "01-frontend", "02-backend", "03-data",
            "04-api", "05-security", "06-infra", "07-testing",
            "08-observability", "09-ai-llm", "10-mobile", "11-product-ux",
            "12-cost-performance", "13-compliance", "14-team-maintenance",
        ]
        self.assertEqual(len(expected_domains), 15)
        for dom in expected_domains:
            full_path = QUESTIONS_DIR / f"{dom}.md"
            core_path = QUESTIONS_DIR / "core" / f"{dom}.md"
            self.assertTrue(full_path.exists(), f"Missing full domain: {full_path}")
            self.assertTrue(core_path.exists(), f"Missing core domain: {core_path}")
            self.assertGreater(full_path.stat().st_size, 100)
            self.assertGreater(core_path.stat().st_size, 50)

    def test_02_all_10_specialized_packs_exist(self):
        """Verify all 10 specialized packs exist with core cards."""
        expected_packs = [
            "software-design", "domain-modeling", "data-systems", "operations",
            "threat-modeling", "ai-engineering", "agent-design", "legacy-change",
            "testing-design", "product-discovery"
        ]
        self.assertEqual(len(expected_packs), 10)
        for p in expected_packs:
            core_path = PACKS_DIR / p / "core.md"
            self.assertTrue(core_path.exists(), f"Missing pack core: {core_path}")
            content = core_path.read_text(encoding="utf-8")
            self.assertIn("Default answer pattern", content)
            self.assertIn("Tradeoffs", content)
            self.assertIn("Anti-patterns", content)

    def test_03_readiness_grades_exist(self):
        """Verify mvp, production, and enterprise grade gate specifications."""
        for g in ("mvp", "production", "enterprise"):
            gate_path = GRADES_DIR / f"{g}.md"
            self.assertTrue(gate_path.exists(), f"Missing grade gate: {gate_path}")
            content = gate_path.read_text(encoding="utf-8")
            self.assertIn("The bar:", content)

    def test_04_domain_signal_detection(self):
        """Verify dynamic domain scanning extracts relevant engineering concerns."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        import socratic_engine

        # Web fullstack
        matched = socratic_engine.detect_domains("Build a React dashboard with Postgres and JWT auth")
        self.assertIn("00-requirements", matched)
        self.assertIn("01-frontend", matched)
        self.assertIn("03-data", matched)
        self.assertIn("05-security", matched)
        self.assertIn("07-testing", matched)

        # AI Agent workflow
        matched_ai = socratic_engine.detect_domains("Design a subagent prompt evaluation framework with RAG")
        self.assertIn("09-ai-llm", matched_ai)
        self.assertIn("07-testing", matched_ai)

    def test_05_pack_trigger_detection(self):
        """Verify trigger detection recommends relevant specialized decision packs."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        import socratic_engine

        packs = socratic_engine.detect_packs("Need circuit breakers, 3am timeouts, and load shedding")
        self.assertIn("operations", packs)

        agent_packs = socratic_engine.detect_packs("Building a multi-agent system with separate subagents and verifiers")
        self.assertIn("agent-design", agent_packs)

    def test_06_socratic_contract_scaffold(self):
        """Verify Socratic Contract formatting."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        import socratic_engine

        contract = socratic_engine.format_contract(
            domains=["00-requirements", "02-backend", "07-testing"],
            highlights=["Decided on SQLite for internal CLI single-user mode"],
            assumed=["File system permissions allow local writes"],
            open_questions=["Target maximum file size?"],
            risks=["Lock contention if called concurrently"],
            plan=["Build storage engine", "Add unit tests"],
        )
        self.assertIn("Socratic Engineering Contract", contract)
        self.assertIn("00-requirements, 02-backend, 07-testing", contract)
        self.assertIn("Decided on SQLite", contract)
        self.assertIn("Target maximum file size?", contract)

    def test_07_cli_scan_and_gate_subprocesses(self):
        """Verify socratic_engine CLI execution via subprocess."""
        cli = SCRIPTS_DIR / "socratic_engine.py"

        # Scan
        res_scan = subprocess.run(
            [sys.executable, "-B", str(cli), "scan", "Build Redis queue worker with Docker deployment"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_scan.returncode, 0, f"scan failed: {res_scan.stderr}")
        self.assertIn("03-data", res_scan.stdout)
        self.assertIn("06-infra", res_scan.stdout)

        # Gate
        res_gate = subprocess.run(
            [sys.executable, "-B", str(cli), "gate", "production"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_gate.returncode, 0, f"gate failed: {res_gate.stderr}")
        self.assertIn("Production grade", res_gate.stdout)


if __name__ == "__main__":
    unittest.main()

