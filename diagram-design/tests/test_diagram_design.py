#!/usr/bin/env python3
"""Automated Unit Tests for Diagram Design Skill (Antigravity Suite)."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
ASSETS_DIR = SKILL_DIR / "assets"
REFS_DIR = SKILL_DIR / "references"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class TestDiagramDesign(unittest.TestCase):
    """Test suite covering diagram-design extractors, linter, exporter, and helper."""

    def test_01_self_check_templates(self):
        """Verify shipped templates pass self_check.py."""
        self_check = SCRIPTS_DIR / "self_check.py"
        for tpl in ("template.html", "template-full.html"):
            target = ASSETS_DIR / tpl
            self.assertTrue(target.exists(), f"Missing template: {tpl}")
            res = subprocess.run(
                [sys.executable, "-B", str(self_check), str(target)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"self_check failed on {tpl}: {res.stderr or res.stdout}")
            self.assertIn("OK", res.stdout)

    def test_02_drawio_extractor(self):
        """Verify drawio_extract.py processes .drawio fixtures."""
        fixture = FIXTURES_DIR / "sample-architecture.drawio"
        self.assertTrue(fixture.exists(), "Missing sample-architecture.drawio fixture")
        script = SCRIPTS_DIR / "drawio_extract.py"
        res = subprocess.run(
            [sys.executable, "-B", str(script), str(fixture)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"drawio_extract failed: {res.stderr}")
        self.assertIn("# draw.io IR", res.stdout)
        self.assertIn("API Gateway", res.stdout)
        self.assertIn("Core Services", res.stdout)

    def test_03_mermaid_extractor(self):
        """Verify mermaid_extract.py processes .mmd fixtures."""
        fixture = FIXTURES_DIR / "sample-flowchart.mmd"
        self.assertTrue(fixture.exists(), "Missing sample-flowchart.mmd fixture")
        script = SCRIPTS_DIR / "mermaid_extract.py"
        res = subprocess.run(
            [sys.executable, "-B", str(script), str(fixture)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"mermaid_extract failed: {res.stderr}")
        self.assertIn("# Mermaid IR", res.stdout)
        self.assertIn("flowchart", res.stdout)
        self.assertIn("API Gateway", res.stdout)

    def test_04_excalidraw_extractor(self):
        """Verify excalidraw_extract.py processes .excalidraw fixtures."""
        fixture = FIXTURES_DIR / "sample-whiteboard.excalidraw"
        self.assertTrue(fixture.exists(), "Missing sample-whiteboard.excalidraw fixture")
        script = SCRIPTS_DIR / "excalidraw_extract.py"
        res = subprocess.run(
            [sys.executable, "-B", str(script), str(fixture)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"excalidraw_extract failed: {res.stderr}")
        self.assertIn("# Excalidraw IR", res.stdout)
        self.assertIn("Intake API", res.stdout)

    def test_05_export_svg_standalone(self):
        """Verify export_svg.py produces standalone SVG from template."""
        src = ASSETS_DIR / "template.html"
        script = SCRIPTS_DIR / "export_svg.py"
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            res = subprocess.run(
                [sys.executable, "-B", str(script), str(src), str(tmp_path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"export_svg failed: {res.stderr}")
            svg_content = tmp_path.read_text(encoding="utf-8")
            self.assertIn("<svg", svg_content)
            self.assertIn("</svg>", svg_content)
            self.assertIn("<defs>", svg_content)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_06_antigravity_helper_lifecycle(self):
        """Verify antigravity_helper scaffold, theme application, and validation."""
        helper = SCRIPTS_DIR / "antigravity_helper.py"
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            # Scaffold with antigravity-dark theme
            res = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(helper),
                    "scaffold",
                    "architecture",
                    str(tmp_path),
                    "--theme=antigravity-dark",
                    "--title=Unit Test Diagram",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"scaffold failed: {res.stderr}")
            content = tmp_path.read_text(encoding="utf-8")
            self.assertIn("Unit Test Diagram", content)
            self.assertIn("#13141a", content)  # antigravity-dark paper token

            # Validate
            res_val = subprocess.run(
                [sys.executable, "-B", str(helper), "validate", str(tmp_path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_val.returncode, 0, f"validation failed: {res_val.stderr}")
            self.assertIn("VALID", res_val.stdout)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_07_all_45_type_references_exist(self):
        """Verify that all 45 diagram types have markdown specifications."""
        expected_types = [
            "architecture", "architecture-delta", "it-state", "flowchart", "sequence",
            "state", "er", "timeline", "swimlane", "quadrant", "radar", "polar",
            "loop", "nested", "tree", "org-chart", "layers", "exploded",
            "axonometric-plan", "venn", "pyramid", "bar", "waterfall", "treemap",
            "heatmap", "line", "gantt", "scatter", "high-level", "process",
            "medallion", "data-flow", "dp-integration", "dp-security-matrix",
            "sankey", "fishbone", "wardley", "kanban", "journey", "service-blueprint",
            "deployment", "dependency", "uml-class", "story-map", "db-schema",
        ]
        self.assertEqual(len(expected_types), 45)
        for t in expected_types:
            ref = REFS_DIR / f"type-{t}.md"
            self.assertTrue(ref.exists(), f"Missing type reference for {t}: {ref}")

    def test_08_core_references_and_assets(self):
        """Verify semantic patterns, layout budgets, style guides, and gallery assets."""
        for ref_name in ("semantic-patterns.md", "layout-budget.md", "style-guide.md", "primitives-core.md"):
            ref = REFS_DIR / ref_name
            self.assertTrue(ref.exists(), f"Missing core reference: {ref_name}")
            self.assertGreater(ref.stat().st_size, 500, f"Reference too small: {ref_name}")

        self.assertTrue((ASSETS_DIR / "icons.html").exists(), "Missing icons.html")
        self.assertTrue((ASSETS_DIR / "index.html").exists(), "Missing index.html gallery")


if __name__ == "__main__":
    unittest.main()

