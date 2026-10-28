#!/usr/bin/env python3
"""Automated Unit & Smoke Tests for Reverse Engineer Anything (REA) Skill."""

import json
import os
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

sys.path.insert(0, str(SCRIPTS_DIR))
import rea_helper  # noqa: E402


class TestREASkillStructure(unittest.TestCase):
    def test_skill_md_exists_and_valid(self):
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.is_file(), "SKILL.md must exist")
        content = skill_md.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter")
        self.assertIn("name: rev-engineer", content)
        self.assertIn("description:", content)
        self.assertIn("metadata:", content)

    def test_all_references_exist(self):
        expected_refs = [
            "android-applications.md",
            "connection-and-recovery.md",
            "evidence-workflows.md",
            "javascript-applications.md",
            "native-and-artifacts.md",
            "runtime-observation.md",
        ]
        for ref in expected_refs:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Reference manual missing: {ref}")
            self.assertGreater(ref_path.stat().st_size, 100, f"Reference manual empty: {ref}")


class TestREAHelperRouting(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_route_elf_binary(self):
        elf_file = self.tmp_path / "test.elf"
        elf_file.write_bytes(b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 60)
        res = rea_helper.detect_file_type(elf_file)
        self.assertEqual(res["type"], "binary")
        self.assertIn("ELF", res["format"])
        self.assertEqual(res["recommended_tool"], "open_binary")
        self.assertEqual(res["alternative_tool"], "inspect_binary_layout")

    def test_route_wasm_binary(self):
        wasm_file = self.tmp_path / "test.wasm"
        wasm_file.write_bytes(b"\x00asm\x01\x00\x00\x00")
        res = rea_helper.detect_file_type(wasm_file)
        self.assertEqual(res["type"], "binary")
        self.assertIn("WASM", res["format"])
        self.assertEqual(res["recommended_tool"], "inspect_wasm_artifact")

    def test_route_asar_archive(self):
        asar_file = self.tmp_path / "app.asar"
        asar_file.write_bytes(b"dummy asar content")
        res = rea_helper.detect_file_type(asar_file)
        self.assertEqual(res["type"], "archive")
        self.assertIn("ASAR", res["format"])
        self.assertEqual(res["recommended_tool"], "analyze_javascript_application")

    def test_route_apk_package(self):
        apk_file = self.tmp_path / "app.apk"
        apk_file.write_bytes(b"PK\x03\x04" + b"\x00" * 30)
        res = rea_helper.detect_file_type(apk_file)
        self.assertEqual(res["type"], "package")
        self.assertIn("APK", res["format"])
        self.assertEqual(res["recommended_tool"], "inspect_android_package")

    def test_route_evm_bytecode(self):
        evm_file = self.tmp_path / "contract.bin"
        evm_file.write_bytes(b"0x608060405234801561001057600080fd5b50")
        res = rea_helper.detect_file_type(evm_file)
        self.assertEqual(res["type"], "bytecode")
        self.assertIn("EVM", res["format"])
        self.assertEqual(res["recommended_tool"], "inspect_evm_interface")

    def test_route_js_project_directory(self):
        pkg_file = self.tmp_path / "package.json"
        pkg_file.write_text('{"name": "test-app"}', encoding="utf-8")
        res = rea_helper.detect_file_type(self.tmp_path)
        self.assertEqual(res["type"], "directory")
        self.assertTrue(res["is_js_project"])
        self.assertEqual(res["recommended_tool"], "analyze_javascript_application")


class TestREAEnvironmentReadiness(unittest.TestCase):
    def test_readiness_structure(self):
        readiness = rea_helper.check_readiness()
        self.assertIn("node", readiness)
        self.assertIn("npm", readiness)
        self.assertIn("ghidra", readiness)
        self.assertIn("wabt", readiness)
        self.assertIn("installed", readiness["node"])
        self.assertIn("compatible", readiness["node"])

    def test_mcp_config_schema(self):
        cfg = rea_helper.get_mcp_config()
        self.assertIn("mcpServers", cfg)
        self.assertIn("rea", cfg["mcpServers"])
        self.assertEqual(cfg["mcpServers"]["rea"]["command"], "npx")


class TestREAHelperCLI(unittest.TestCase):
    def test_cli_readiness(self):
        cli = SCRIPTS_DIR / "rea_helper.py"
        res = subprocess.run([sys.executable, "-B", str(cli), "readiness", "--json"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIn("node", data)
        self.assertIn("compatible", data["node"])
        if data["node"]["installed"]:
            self.assertIn("version", data["node"])
            major = int(data["node"]["version"].lstrip("v").split(".")[0])
            self.assertEqual(data["node"]["compatible"], major >= 22)

    def test_cli_mcp_config(self):
        cli = SCRIPTS_DIR / "rea_helper.py"
        res = subprocess.run([sys.executable, "-B", str(cli), "mcp-config", "--json"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIn("rea", data["mcpServers"])


if __name__ == "__main__":
    unittest.main()
