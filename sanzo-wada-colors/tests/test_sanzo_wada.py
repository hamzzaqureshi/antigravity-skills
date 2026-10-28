#!/usr/bin/env python3
"""Automated Unit Tests for Sanzo Wada Color Dictionary Skill & Engine."""

import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
DATA_DIR = SKILL_DIR / "data"
BIN_DIR = SKILL_DIR / "bin"
REFERENCES_DIR = SKILL_DIR / "references"

sys.path.insert(0, str(SCRIPTS_DIR))
import color_engine


class TestSanzoWada(unittest.TestCase):
    """Test suite covering the 348 palettes, 159 colors, WCAG metrics, and CLI engine."""

    def test_01_skill_and_data_files_exist(self):
        """Verify SKILL.md, dataset, and reference files exist and are populated."""
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md missing")
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("name: sanzo-wada-colors", content)
        self.assertIn("348", content)

        data_file = DATA_DIR / "colors.json"
        self.assertTrue(data_file.exists(), "colors.json missing")
        self.assertGreater(data_file.stat().st_size, 10000)

        for ref in ["wada-color-index.md", "palette-types-guide.md"]:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.exists(), f"Reference {ref} missing")
            self.assertGreater(ref_path.stat().st_size, 200)

    def test_02_dataset_integrity(self):
        """Verify all 159 colors have valid hex, rgb, and cmyk values."""
        data = color_engine.load_data()
        colors = data["colors"]
        self.assertEqual(len(colors), 159, "Expected exactly 159 unique colors")

        hex_regex = re.compile(r"^#[0-9a-fA-F]{6}$")
        for c in colors:
            self.assertTrue("name" in c and len(c["name"]) > 0)
            self.assertTrue(hex_regex.match(c["hex"]), f"Invalid hex: {c['hex']}")
            self.assertEqual(len(c["rgb"]), 3)
            for val in c["rgb"]:
                self.assertTrue(0 <= val <= 255, f"RGB out of bounds: {val} in {c['name']}")
            self.assertEqual(len(c["cmyk"]), 4)
            for val in c["cmyk"]:
                # Historical note: Dull Violet Black has M=106 from 1930s print plate errata
                self.assertTrue(0 <= val <= 110, f"CMYK out of bounds: {val} in {c['name']}")

    def test_03_combinations_completeness(self):
        """Verify all 348 combinations exist (120 duos, 120 trios, 108 quads)."""
        data = color_engine.load_data()
        combos = data["combinations"]
        self.assertEqual(len(combos), 348, "Expected 348 combination mappings")

        duos = [k for k, v in combos.items() if len(v) == 2]
        trios = [k for k, v in combos.items() if len(v) == 3]
        quads = [k for k, v in combos.items() if len(v) == 4]

        self.assertEqual(len(duos), 120, "Expected 120 duos (#1-#120)")
        self.assertEqual(len(trios), 120, "Expected 120 trios (#121-#240)")
        self.assertEqual(len(quads), 108, "Expected 108 quads (#241-#348)")
        self.assertEqual(len(duos) + len(trios) + len(quads), 348)

    def test_04_get_combination(self):
        """Verify get_combination retrieves valid palettes and flags invalid IDs."""
        combo_1 = color_engine.get_combination(1)
        self.assertEqual(len(combo_1), 2, "Combo 1 should be a duo")

        combo_198 = color_engine.get_combination(198)
        self.assertEqual(len(combo_198), 3, "Combo 198 should be a trio")
        names_198 = [c["name"] for c in combo_198]
        self.assertIn("Burnt Sienna", names_198)

        combo_348 = color_engine.get_combination(348)
        self.assertEqual(len(combo_348), 4, "Combo 348 should be a quad")

        with self.assertRaises(ValueError):
            color_engine.get_combination(0)

        with self.assertRaises(ValueError):
            color_engine.get_combination(349)

    def test_05_search_colors(self):
        """Verify search_colors matches by name and hex code."""
        sienna_matches = color_engine.search_colors("Burnt Sienna")
        self.assertGreaterEqual(len(sienna_matches), 1)
        self.assertEqual(sienna_matches[0]["hex"], "#ae5224")

        hex_matches = color_engine.search_colors("#ae5224")
        self.assertEqual(len(hex_matches), 1)
        self.assertEqual(hex_matches[0]["name"], "Burnt Sienna")

        no_matches = color_engine.search_colors("NonExistentColorNameXYZ")
        self.assertEqual(len(no_matches), 0)

    def test_06_list_combinations(self):
        """Verify list_combinations pagination and size filters."""
        all_first_10 = color_engine.list_combinations(limit=10)
        self.assertEqual(len(all_first_10), 10)

        duos_only = color_engine.list_combinations(size=2, limit=5)
        self.assertEqual(len(duos_only), 5)
        for item in duos_only:
            self.assertEqual(item["size"], 2)

        trios_only = color_engine.list_combinations(size=3, limit=5)
        self.assertEqual(len(trios_only), 5)
        for item in trios_only:
            self.assertEqual(item["size"], 3)

        quads_only = color_engine.list_combinations(size=4, limit=5)
        self.assertEqual(len(quads_only), 5)
        for item in quads_only:
            self.assertEqual(item["size"], 4)

    def test_07_random_combination(self):
        """Verify picking random combinations."""
        cid, colors = color_engine.get_random_combination()
        self.assertTrue(1 <= cid <= 348)
        self.assertIn(len(colors), [2, 3, 4])

        cid_trio, colors_trio = color_engine.get_random_combination(size=3)
        self.assertEqual(len(colors_trio), 3)

    def test_08_wcag_contrast_calculation(self):
        """Verify luminance and WCAG contrast calculations."""
        black = [0, 0, 0]
        white = [255, 255, 255]

        ratio_bw = color_engine.wcag_contrast_ratio(black, white)
        self.assertAlmostEqual(ratio_bw, 21.0, places=1)

        ratio_same = color_engine.wcag_contrast_ratio(white, white)
        self.assertAlmostEqual(ratio_same, 1.0, places=1)

        combo_198 = color_engine.get_combination(198)
        ratio = color_engine.wcag_contrast_ratio(combo_198[0]["rgb"], combo_198[1]["rgb"])
        self.assertGreater(ratio, 1.0)
        self.assertLess(ratio, 21.0)

    def test_09_export_css(self):
        """Verify CSS token export format."""
        css_out = color_engine.export_palette(198, fmt="css")
        self.assertIn(":root {", css_out)
        self.assertIn("--wada-198-color-1: #ae5224;", css_out)
        self.assertIn("--color-burnt-sienna: #ae5224;", css_out)

    def test_10_export_tailwind_scss_json_svg(self):
        """Verify Tailwind, SCSS, JSON, and SVG exports."""
        tw_out = color_engine.export_palette(198, fmt="tailwind")
        tw_data = json.loads(tw_out)
        self.assertIn("wada-198", tw_data)
        self.assertIn("burnt-sienna", tw_data["wada-198"])

        scss_out = color_engine.export_palette(198, fmt="scss")
        self.assertIn("$burnt-sienna: #ae5224;", scss_out)

        json_out = color_engine.export_palette(198, fmt="json")
        json_data = json.loads(json_out)
        self.assertEqual(json_data["combination"], 198)
        self.assertEqual(len(json_data["colors"]), 3)

        svg_out = color_engine.export_palette(198, fmt="svg")
        self.assertTrue(svg_out.startswith("<svg"))
        self.assertTrue(svg_out.endswith("</svg>"))
        self.assertIn("<rect", svg_out)
        self.assertIn("#ae5224", svg_out)

    def test_11_cli_wrapper_execution(self):
        """Verify bin/wada executable works end-to-end via shell."""
        bin_path = BIN_DIR / "wada"
        self.assertTrue(bin_path.exists())

        out = subprocess.check_output([str(bin_path), "combo", "198"], text=True)
        self.assertIn("Sanzo Wada Combination #198", out)
        self.assertIn("Burnt Sienna", out)
        self.assertIn("WCAG Contrast Matrix", out)

        out_search = subprocess.check_output([str(bin_path), "search", "indigo"], text=True)
        self.assertIn("Deep Indigo", out_search)


if __name__ == "__main__":
    unittest.main()
