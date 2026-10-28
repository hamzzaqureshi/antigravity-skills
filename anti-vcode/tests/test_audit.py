import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)
import audit  # noqa: E402


class TestAntiVibecodingAudit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_clean_html_scores_100(self):
        clean_file = os.path.join(self.tmp, "index.html")
        with open(clean_file, "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
  <title>Intentional Tool</title>
  <link rel="stylesheet" href="style.css">
</head>
<body class="bg-stone-100 text-stone-900">
  <main class="max-w-4xl mx-auto p-8">
    <h1 class="text-3xl font-serif">Deterministic Compiler</h1>
    <p class="text-base text-stone-700">Compiles raw telemetry in 4ms with zero network calls.</p>
  </main>
</body>
</html>""")
        findings = audit.scan_path(clean_file)
        score = audit.compute_score(findings)
        self.assertEqual(len(findings), 0)
        self.assertEqual(score, 100)

    def test_vibecoded_html_detected(self):
        slop_file = os.path.join(self.tmp, "slop.jsx")
        with open(slop_file, "w", encoding="utf-8") as f:
            f.write("""export default function Hero() {
  return (
    <div className="bg-black text-white relative">
      <div className="radial-gradient blur-3xl rounded-full bg-purple-500/20" />
      <h1 className="bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-blue-500">
        Transform your workflow with the future of intelligent collaboration
      </h1>
      <button className="backdrop-blur-md rounded-3xl">
        <Sparkles className="w-4 h-4" /> Get Started
      </button>
      <p>Trusted by 10,000+ teams worldwide</p>
    </div>
  );
}""")
        findings = audit.scan_path(slop_file)
        rule_ids = {f["rule_id"] for f in findings}
        self.assertIn("purple-blue-gradient", rule_ids)
        self.assertIn("gradient-text-hero", rule_ids)
        self.assertIn("radial-gradient-orb", rule_ids)
        self.assertIn("excessive-glassmorphism", rule_ids)
        self.assertIn("sparkle-ai-icon", rule_ids)
        self.assertIn("generic-buzzword-copy", rule_ids)
        self.assertIn("fake-social-proof", rule_ids)
        score = audit.compute_score(findings)
        self.assertLess(score, 70)


if __name__ == "__main__":
    unittest.main()
