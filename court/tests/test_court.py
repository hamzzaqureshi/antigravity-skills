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
import court  # noqa: E402


class CourtTest(unittest.TestCase):
    def setUp(self):
        self.old = os.getcwd()
        self.tmp = tempfile.mkdtemp()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self.old)
        shutil.rmtree(self.tmp)

    def open_trial(self, *extra):
        court.main(["init", "--case", "Quit my job to sell candles on Etsy. $8,000 saved.", "--seed", "7"] + list(extra))
        return court.load_state()

    def write_all(self, state, phase, text):
        for j in court.jobs(state, phase):
            with open(j["output"], "w", encoding="utf-8") as f:
                f.write(text)

    def test_jurors_embedded_fallback(self):
        jurors = court.load_jurors("/nonexistent/path/jurors.json")
        self.assertEqual(len(jurors), 12)
        self.assertEqual(len({j["name"] for j in jurors}), 12)

    def test_quick_jury(self):
        state = self.open_trial("--quick")
        self.assertEqual(len(state["jury"]), 6)

    def test_inline_case_initialization(self):
        state = self.open_trial("--jury", "3")
        case_file = os.path.join(state["dir"], "case.md")
        self.assertTrue(os.path.exists(case_file))
        with open(case_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Quit my job", content)

    def test_parse_vote_tolerant(self):
        variants = [
            ("VOTE: NOT GUILTY\nREASON: valid\nDECIDING FACT: savings\nWOULD FLIP IF: none", "NOT GUILTY"),
            ("**VOTE:** **GUILTY**\nREASON: high risk\nDECIDING FACT: no sales\nWOULD FLIP IF: sales", "GUILTY"),
            ("- VOTE: [NOT GUILTY]\nREASON: fine\nDECIDING FACT: margin\nWOULD FLIP IF: x", "NOT GUILTY"),
            ("### VOTE: guilty\nREASON: no\nDECIDING FACT: loss\nWOULD FLIP IF: profit", "GUILTY"),
            ("* **VOTE:** NOT GUILTY\n**REASON:** sound numbers", "NOT GUILTY"),
        ]
        for text, expected in variants:
            v = court.parse_vote(text)
            self.assertIsNotNone(v, "Failed on: %s" % text)
            self.assertEqual(v["vote"], expected)

    def test_full_trial_tally_and_render(self):
        state = self.open_trial("--jury", "5")
        self.write_all(state, "opening", "1. Point")
        self.write_all(state, "rebuttal", "1. Counter")
        votes = ["GUILTY", "GUILTY", "NOT GUILTY", "GUILTY", "NO VOTE"]
        for j, v in zip(court.jobs(state, "jury"), votes):
            with open(j["output"], "w", encoding="utf-8") as f:
                if v == "NO VOTE":
                    f.write("NO VOTE")
                else:
                    f.write("VOTE: %s\nREASON: because | reason\nDECIDING FACT: fact\nWOULD FLIP IF: change" % v)
        
        t = court.tally(state)
        self.assertEqual((t["verdict"], t["guilty"], t["not_guilty"], t["no_vote"]), ("GUILTY", 3, 1, 1))
        self.assertEqual(court.verdict_line(t), "GUILTY, 3 to 1")

        self.write_all(state, "judge", "## The sentence\nKeep the job.")
        text = court.render(state)
        self.assertIn("# The Verdict: GUILTY, 3 to 1", text)
        self.assertIn("Quit my job to sell candles", text)
        self.assertIn("because / reason", text)
        self.assertIn("## The sentence", text)

    def test_hung_jury(self):
        state = self.open_trial("--jury", "4")
        for j, v in zip(court.jobs(state, "jury"), ["GUILTY", "NOT GUILTY", "GUILTY", "NOT GUILTY"]):
            with open(j["output"], "w", encoding="utf-8") as f:
                f.write("VOTE: %s\n" % v)
        self.assertEqual(court.verdict_line(court.tally(state)), "HUNG JURY, 2 to 2")

    def test_next_phase_progression(self):
        state = self.open_trial("--jury", "3")
        self.assertTrue(court.missing(state, "opening"))
        self.write_all(state, "opening", "done")
        self.assertFalse(court.missing(state, "opening"))
        self.assertTrue(court.missing(state, "rebuttal"))


if __name__ == "__main__":
    unittest.main()
