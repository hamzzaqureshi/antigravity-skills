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
import taste  # noqa: E402


class TestTasteSkill(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_clean_html_passes_audit(self):
        clean_file = os.path.join(self.tmp, "clean.tsx")
        with open(clean_file, "w", encoding="utf-8") as f:
            f.write("""export default function Hero() {
  return (
    <section className="min-h-[100dvh] pt-16 max-w-7xl mx-auto px-6">
      <h1 className="text-5xl font-sans tracking-tight text-zinc-900 dark:text-zinc-50">
        Deterministic Telemetry Streaming
      </h1>
      <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400 max-w-xl">
        Ingest and aggregate distributed events in under 4ms with zero overhead.
      </p>
      <button className="mt-6 px-5 py-2.5 bg-zinc-900 text-white rounded-lg">
        Deploy Engine
      </button>
    </section>
  );
}""")
        with open(clean_file, "r", encoding="utf-8") as f:
            content = f.read()
        res = taste.audit_content(content, clean_file)
        self.assertEqual(res["score"], 100)
        self.assertTrue(res["passed"])
        self.assertEqual(len(res["violations"]), 0)

    def test_em_dash_triggers_critical_failure(self):
        slop_file = os.path.join(self.tmp, "em_dash.tsx")
        with open(slop_file, "w", encoding="utf-8") as f:
            f.write("""export default function Headline() {
  return <h1>Fast—and reliable—cloud workflows</h1>;
}""")
        with open(slop_file, "r", encoding="utf-8") as f:
            content = f.read()
        res = taste.audit_content(content, slop_file)
        self.assertFalse(res["passed"])
        rule_ids = {v["rule"] for v in res["violations"]}
        self.assertIn("em-dash-ban", rule_ids)

    def test_lila_and_banned_hexes_detected(self):
        slop_file = os.path.join(self.tmp, "slop.tsx")
        with open(slop_file, "w", encoding="utf-8") as f:
            f.write("""export default function BadHero() {
  return (
    <div className="bg-[#f5f1ea] pt-36">
      <div className="radial-gradient bg-purple-500/20 blur-3xl" />
      <h1 className="bg-gradient-to-r from-purple-500 to-blue-500 font-serif">
        Fraunces Heading
      </h1>
    </div>
  );
}""")
        with open(slop_file, "r", encoding="utf-8") as f:
            content = f.read()
        res = taste.audit_content(content, slop_file)
        self.assertFalse(res["passed"])
        rule_ids = {v["rule"] for v in res["violations"]}
        self.assertIn("lila-purple-glow-ban", rule_ids)
        self.assertIn("banned-warm-craft-palette", rule_ids)
        self.assertIn("banned-fonts-as-default", rule_ids)
        self.assertIn("hero-top-padding-cap", rule_ids)

    def test_brief_inference_minimalist(self):
        res = taste.infer_brief("Build a Linear-style minimalist devtool landing page")
        self.assertEqual(res["dials"]["DESIGN_VARIANCE"], 5)
        self.assertEqual(res["dials"]["MOTION_INTENSITY"], 3)
        self.assertEqual(res["dials"]["VISUAL_DENSITY"], 2)
        self.assertIn("Minimalist", res["style"])
        self.assertIn("Geist", res["foundation"])

    def test_brief_inference_brutalist(self):
        res = taste.infer_brief("Create a raw Swiss industrial brutalist portfolio")
        self.assertEqual(res["dials"]["DESIGN_VARIANCE"], 9)
        self.assertEqual(res["dials"]["VISUAL_DENSITY"], 7)
        self.assertIn("Brutalist", res["style"])


if __name__ == "__main__":
    unittest.main()
