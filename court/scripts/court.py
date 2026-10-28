#!/usr/bin/env python3
"""Antigravity Court Engine: Adversarial multi-perspective deliberation framework.

Orchestrates a 4-phase trial to combat AI sycophancy:
  1. Opening statements (Prosecution vs. Defense)
  2. Rebuttals (Cross-examination)
  3. Jury deliberation (Independent persona voting)
  4. Presiding Judge (Synthesis & actionable acquittal conditions)

Usage:
  python3 court.py plan [--jury N | --quick]
  python3 court.py init (--case "..." | --case-file PATH) [--jury N | --quick] [--seed S] [--jurors-file PATH]
  python3 court.py prompts <phase> [--all]
  python3 court.py next
  python3 court.py check <phase>
  python3 court.py status
  python3 court.py tally
  python3 court.py render
"""
import argparse
import json
import os
import random
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = ".court"
LATEST = os.path.join(ROOT, "LATEST")
PHASES = ["opening", "rebuttal", "jury", "judge"]
DEFAULT_JURY = 12
QUICK_JURY = 6
CHARGE = "The case fails as stated: it should not go ahead the way it is described."
CREDIT = (
    "_Made with [/court](https://github.com/alexyc9381/court-skill), "
    "adapted for Google Antigravity._"
)

# Embedded default jurors for zero-dependency portability
DEFAULT_JURORS = [
    {"name": "The Accountant", "lens": "You follow the money. You distrust any number that has no source, and you want to know who pays, how much, and when."},
    {"name": "The First-Time Customer", "lens": "You have never heard of this before today. Would you actually buy it, use it or believe it, this week, at this price, over what you already do?"},
    {"name": "The Competitor", "lens": "You run the business this case would compete with. If you saw this tomorrow, how would you beat it, copy it or ignore it?"},
    {"name": "The Retired Judge", "lens": "You care about the burden of proof. Is the evidence actually in the record, or is it hope dressed up as fact?"},
    {"name": "The Teenager", "lens": "You are blunt and easily bored. Would anyone care about this, talk about it, or come back to it next week?"},
    {"name": "The Engineer", "lens": "You build things. Can this actually be made, does it work in the real world, and what breaks first when it grows?"},
    {"name": "The Small-Business Owner", "lens": "You have run a shop for 20 years. Who does the work on Monday morning, where does the cash come from until it pays, and what happens in a slow month?"},
    {"name": "The Statistician", "lens": "You look for base rates, tiny samples and survivorship bias. How often does a plan like this actually work?"},
    {"name": "The Parent", "lens": "You protect your family's time, money and safety. Is it trustworthy, and is it worth the risk to the people involved?"},
    {"name": "The Investor", "lens": "You weigh upside against risk. Would you put your own money into this exactly as described, and why or why not?"},
    {"name": "The Designer", "lens": "You care about clarity. Would a stranger understand what this is and why it matters in five seconds?"},
    {"name": "The Lawyer", "lens": "You look for legal, regulatory and liability traps that the case does not mention."}
]


# ---------- state & configuration ----------

def load_jurors(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        with open(custom_path, "r", encoding="utf-8") as f:
            return json.load(f)
    candidates = [
        os.path.join(HERE, "..", "resources", "jurors.json"),
        os.path.join(HERE, "jurors.json"),
        os.path.join(HERE, "resources", "jurors.json"),
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return DEFAULT_JURORS


def run_dir():
    if not os.path.exists(LATEST):
        sys.exit("court: no active trial found. Run: python3 court.py init --case '...'")
    with open(LATEST, "r", encoding="utf-8") as f:
        path = f.read().strip()
    if not os.path.isdir(path):
        sys.exit("court: invalid trial directory in .court/LATEST: %s" % path)
    return path


def load_state(rd=None):
    rd = rd or run_dir()
    state_file = os.path.join(rd, "state.json")
    if not os.path.exists(state_file):
        sys.exit("court: state.json not found in %s" % rd)
    with open(state_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    state_file = os.path.join(state["dir"], "state.json")
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def jury_size(args):
    if getattr(args, "quick", False):
        return QUICK_JURY
    n = getattr(args, "jury", None) or DEFAULT_JURY
    if n < 3 or n > 12:
        sys.exit("court: jury size must be between 3 and 12.")
    return n


# ---------- jobs & paths ----------

def jobs(state, phase):
    d = state["dir"]
    if phase in ("opening", "rebuttal"):
        ids = ["prosecution", "defense"]
    elif phase == "jury":
        ids = ["juror-%02d" % (i + 1) for i in range(len(state["jury"]))]
    elif phase == "judge":
        ids = ["judge"]
    else:
        sys.exit("court: unknown phase %r (supported: %s)" % (phase, ", ".join(PHASES)))
    
    return [
        {
            "id": jid,
            "brief": os.path.abspath(os.path.join(d, "briefs", "%s-%s.md" % (phase, jid))),
            "output": os.path.abspath(os.path.join(d, phase, "%s.md" % jid)),
        }
        for jid in ids
    ]


def done(job):
    p = job["output"]
    return os.path.exists(p) and os.path.getsize(p) > 0


def missing(state, phase):
    return [j for j in jobs(state, phase) if not done(j)]


def _abs(state, *parts):
    return os.path.abspath(os.path.join(state["dir"], *parts))


# ---------- briefs ----------

def brief_text(state, phase, job):
    case = _abs(state, "case.md")
    head = (
        "You are participating in an adversarial trial orchestrated by the Antigravity court skill.\n"
        "You cannot see earlier conversation context: everything you know is in the files named below.\n"
        "Use ONLY what is in the record. Never invent facts, numbers, quotes, or sources.\n"
        "Where the record is silent, explicitly state what is missing and why it matters.\n"
        "Write your output to EXACTLY this file path:\n\n"
        "    %s\n\n"
        "The Charge: %s\n"
        "The Case File: %s\n\n"
        % (job["output"], CHARGE, case)
    )

    if phase == "opening":
        if job["id"] == "prosecution":
            return head + (
                "ROLE: PROSECUTOR\n"
                "Build the strongest honest case that the charge holds (the idea/proposal fails as stated).\n\n"
                "Requirements:\n"
                "- 3 to 5 numbered charges. Each names one concrete way the case fails, cites/quotes evidence from the case file, and explains the cost.\n"
                "- Attack the case as the user actually wrote it, never a strawman.\n"
                "- No insults, no hedging, no praise. Maximum 350 words.\n"
            )
        return head + (
            "ROLE: DEFENSE\n"
            "Build the strongest honest case that the charge does NOT hold (the idea/proposal works as stated).\n\n"
            "Requirements:\n"
            "- 3 to 5 numbered points. Each names one concrete strength, cites/quotes evidence from the case file, and explains why it outweighs the obvious objection.\n"
            "- Defend the case as actually written. Concede undefendable flaws in one honest line instead of spinning.\n"
            "- Maximum 350 words.\n"
        )

    if phase == "rebuttal":
        side, other = ("prosecution", "defense") if job["id"] == "prosecution" else ("defense", "prosecution")
        other_opening = _abs(state, "opening", other + ".md")
        return head + (
            "ROLE: %s (REBUTTAL)\n"
            "Read the other side's opening statement:\n\n"
            "    %s\n\n"
            "Requirements:\n"
            "- Address each of their numbered points in order: state whether it survives scrutiny and why, in 1-2 clear sentences each.\n"
            "- Identify the single decisive issue the jury must resolve.\n"
            "- Maximum 250 words.\n"
            % (side.upper(), other_opening)
        )

    if phase == "jury":
        idx = int(job["id"].split("-")[1]) - 1
        juror = state["jury"][idx]
        record = "\n".join("    " + _abs(state, p, s + ".md")
                           for p in ("opening", "rebuttal") for s in ("prosecution", "defense"))
        return head + (
            "ROLE: JUROR %d of %d: %s\n"
            "YOUR LENS: %s\n\n"
            "Read the case file and all 4 prior statements:\n\n%s\n\n"
            "Decide independently through your designated lens. Voting to be polite or tough is contempt of court.\n\n"
            "Output EXACTLY these 4 lines and nothing else:\n\n"
            "VOTE: GUILTY or NOT GUILTY\n"
            "REASON: one clear sentence in your own persona voice\n"
            "DECIDING FACT: the one specific fact or omission from the record that decided your vote\n"
            "WOULD FLIP IF: the single specific change to the case that would flip your vote\n"
            % (idx + 1, len(state["jury"]), juror["name"], juror["lens"], record)
        )

    if phase == "judge":
        return head + (
            "ROLE: PRESIDING JUDGE\n"
            "The jury has voted and you cannot overturn their vote.\n"
            "Review the record: %s, %s, votes in %s, and tally in %s.\n\n"
            "Write the following sections clearly and concisely:\n\n"
            "## Charges that stuck\n"
            "The 3 objections the jurors cited most frequently, each in 1 sentence, stating how many jurors cited it.\n\n"
            "## What the defense got right\n"
            "The 2 strongest points in favor of the proposal that survived scrutiny.\n\n"
            "## Conditions for acquittal\n"
            "The 3 specific, actionable changes that would flip the most votes (synthesized from 'WOULD FLIP IF' entries).\n\n"
            "## The sentence\n"
            "One short paragraph in an authoritative judicial voice: the definitive next action for the user.\n\n"
            "Maximum 250 words. Do not repeat the numerical vote tally.\n"
            % (_abs(state, "opening"), _abs(state, "rebuttal"), _abs(state, "jury"), _abs(state, "tally.json"))
        )

    raise ValueError(phase)


# ---------- vote parsing & tally ----------

VOTE_RE = re.compile(r"^\s*[-*#]*\s*\**\s*VOTE\s*:?\s*\**\s*:?\s*\[?\**\s*(NOT\s+GUILTY|GUILTY)\b", re.I | re.M)
FIELD_RE = r"^\s*[-*#]*\s*\**\s*%s\s*:?\s*\**\s*:?\s*(.+)$"


def parse_vote(text):
    if not text:
        return None
    m = VOTE_RE.search(text)
    if not m:
        return None
    vote = "NOT GUILTY" if "NOT" in m.group(1).upper() else "GUILTY"
    out = {"vote": vote}
    for key, name in (("reason", "REASON"), ("fact", "DECIDING FACT"), ("flip", "WOULD FLIP IF")):
        f = re.search(FIELD_RE % name, text, re.I | re.M)
        out[key] = f.group(1).strip().strip("[]*").strip() if f else ""
    return out


def tally(state):
    rows = []
    for j, juror in zip(jobs(state, "jury"), state["jury"]):
        text = ""
        if done(j):
            with open(j["output"], "r", encoding="utf-8") as f:
                text = f.read()
        v = parse_vote(text)
        rows.append({
            "juror": juror["name"],
            "vote": v["vote"] if v else "NO VOTE",
            "reason": v["reason"] if v else "",
            "fact": v["fact"] if v else "",
            "flip": v["flip"] if v else ""
        })
    guilty = sum(1 for r in rows if r["vote"] == "GUILTY")
    not_guilty = sum(1 for r in rows if r["vote"] == "NOT GUILTY")
    if guilty > not_guilty:
        verdict = "GUILTY"
    elif not_guilty > guilty:
        verdict = "NOT GUILTY"
    else:
        verdict = "HUNG JURY"
    
    result = {
        "verdict": verdict,
        "guilty": guilty,
        "not_guilty": not_guilty,
        "no_vote": len(rows) - guilty - not_guilty,
        "jurors": rows
    }
    with open(os.path.join(state["dir"], "tally.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return result


def verdict_line(t):
    if t["verdict"] == "HUNG JURY":
        return "HUNG JURY, %d to %d" % (t["guilty"], t["not_guilty"])
    big, small = (t["guilty"], t["not_guilty"]) if t["verdict"] == "GUILTY" else (t["not_guilty"], t["guilty"])
    return "%s, %d to %d" % (t["verdict"], big, small)


def render(state):
    t = tally(state)
    case_path = os.path.join(state["dir"], "case.md")
    case = "(empty case)"
    if os.path.exists(case_path):
        with open(case_path, "r", encoding="utf-8") as f:
            case = f.read().strip()
    first = case.splitlines()[0].lstrip("# ").strip() if case else "(empty case)"
    judge = jobs(state, "judge")[0]
    judgment = "_The judge has not ruled yet._"
    if done(judge):
        with open(judge["output"], "r", encoding="utf-8") as f:
            judgment = f.read().strip()

    lines = [
        "# The Verdict: %s" % verdict_line(t),
        "",
        "**The Case:** %s" % first,
        "",
        "**The Charge:** %s" % CHARGE,
        "",
        "## How the Jury Voted",
        "",
        "| Juror | Vote | Reason | Deciding Fact / Condition |",
        "|---|---|---|---|",
    ]
    for r in t["jurors"]:
        lines.append("| %s | **%s** | %s | %s |" % (
            r["juror"],
            r["vote"],
            r["reason"].replace("|", "/"),
            r["flip"].replace("|", "/")
        ))
    lines += [
        "",
        judgment,
        "",
        "---",
        "_Trial archived in `%s`._" % os.path.abspath(state["dir"]),
        "",
        CREDIT
    ]
    text = "\n".join(lines) + "\n"
    with open(os.path.join(state["dir"], "VERDICT.md"), "w", encoding="utf-8") as f:
        f.write(text)
    return text


# ---------- CLI Commands ----------

def cmd_plan(args):
    n = jury_size(args)
    print("Trial Plan: Jury of %d independent personas" % n)
    print("Total perspectives: %d (2 Opening, 2 Rebuttal, %d Jurors, 1 Judge)" % (5 + n, n))


def cmd_init(args):
    n = jury_size(args)
    if args.case:
        case = args.case.strip()
    elif args.case_file:
        if not os.path.exists(args.case_file):
            sys.exit("court: case file not found: %s" % args.case_file)
        with open(args.case_file, "r", encoding="utf-8") as f:
            case = f.read().strip()
    else:
        sys.exit("court: either --case '...' or --case-file PATH is required.")

    if not case:
        sys.exit("court: case is empty.")

    seed = args.seed if args.seed is not None else random.randrange(1, 10 ** 6)
    jurors = load_jurors(getattr(args, "jurors_file", None))
    rng = random.Random(seed)
    jury = jurors[:] if n == len(jurors) else rng.sample(jurors, n)

    rd = os.path.join(ROOT, time.strftime("%Y%m%d-%H%M%S"))
    for sub in ("briefs", "opening", "rebuttal", "jury", "judge"):
        os.makedirs(os.path.join(rd, sub), exist_ok=True)

    with open(os.path.join(rd, "case.md"), "w", encoding="utf-8") as f:
        f.write(case + "\n")

    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, "case.md"), "w", encoding="utf-8") as f:
        f.write(case + "\n")

    state = {
        "dir": os.path.abspath(rd),
        "seed": seed,
        "jury": jury,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    save_state(state)
    with open(LATEST, "w", encoding="utf-8") as f:
        f.write(os.path.abspath(rd))

    print("Court: Trial opened in %s (Jury: %d, Seed: %d)" % (rd, n, seed))
    print("Next step: python3 %s prompts opening" % os.path.abspath(__file__))


def cmd_prompts(args):
    state = load_state()
    all_jobs = jobs(state, args.phase)
    for j in all_jobs:
        with open(j["brief"], "w", encoding="utf-8") as f:
            f.write(brief_text(state, args.phase, j))

    todo = missing(state, args.phase)
    if not todo:
        print("court: phase '%s' is complete. Run `python3 court.py next`" % args.phase)
        return

    print("=== Phase: %s (%d pending job(s)) ===" % (args.phase.upper(), len(todo)))
    # Output briefs directly to eliminate unnecessary view_file turns
    if args.phase in ("opening", "rebuttal", "judge") or getattr(args, "all", False):
        for j in todo:
            print("\n--- JOB: %s | OUTPUT: %s ---" % (j["id"], j["output"]))
            with open(j["brief"], "r", encoding="utf-8") as f:
                print(f.read().strip())
    else:  # Jury phase: display concise table of jurors and instructions
        print("\nRequired format for each juror output (write to target file):")
        print("  VOTE: GUILTY (or NOT GUILTY)")
        print("  REASON: <one sentence in persona voice>")
        print("  DECIDING FACT: <key fact or omission from record>")
        print("  WOULD FLIP IF: <single actionable change that would reverse vote>\n")
        print("| Job ID | Juror Name | Lens | Target Output File |")
        print("|---|---|---|---|")
        for j in todo:
            idx = int(j["id"].split("-")[1]) - 1
            juror = state["jury"][idx]
            print("| %s | %s | %s | %s |" % (j["id"], juror["name"], juror["lens"], j["output"]))


def cmd_check(args):
    state = load_state()
    todo = missing(state, args.phase)
    if not todo:
        print("court: phase '%s' is complete." % args.phase)
    else:
        print("court: phase '%s' has %d missing output(s):" % (args.phase, len(todo)))
        for j in todo:
            print("  missing: %s -> %s" % (j["id"], j["output"]))


def cmd_next(args):
    state = load_state()
    for phase in PHASES:
        todo = missing(state, phase)
        if todo:
            if phase == "judge":
                t = tally(state)
                print("court: jury vote: %s" % verdict_line(t))
            print("Next phase: '%s' (%d pending). Run: python3 %s prompts %s" % (phase, len(todo), os.path.abspath(__file__), phase))
            return
    print("court: all trial phases complete. Run: python3 %s render" % os.path.abspath(__file__))


def cmd_status(args):
    state = load_state()
    print("Trial: %s | Jury: %d" % (state["dir"], len(state["jury"])))
    for phase in PHASES:
        all_j = jobs(state, phase)
        done_cnt = sum(1 for j in all_j if done(j))
        print("  - %-9s: %d/%d done" % (phase, done_cnt, len(all_j)))


def cmd_tally(args):
    state = load_state()
    print(verdict_line(tally(state)))


def cmd_render(args):
    state = load_state()
    sys.stdout.write(render(state))


def main(argv=None):
    p = argparse.ArgumentParser(prog="court.py", description="Antigravity Court Engine")
    sub = p.add_subparsers(dest="cmd")

    pl = sub.add_parser("plan", help="Estimate trial size")
    pl.add_argument("--jury", type=int, help="Jury size (3-12)")
    pl.add_argument("--quick", action="store_true", help="Quick jury (6 jurors)")

    pi = sub.add_parser("init", help="Open trial")
    pi.add_argument("--case", help="Inline case description")
    pi.add_argument("--case-file", help="Path to markdown case file")
    pi.add_argument("--jury", type=int, help="Jury size (3-12)")
    pi.add_argument("--quick", action="store_true", help="Quick jury (6 jurors)")
    pi.add_argument("--seed", type=int, help="Random seed")
    pi.add_argument("--jurors-file", help="Custom jurors JSON file")

    for name in ("prompts", "check"):
        sp = sub.add_parser(name)
        sp.add_argument("phase", choices=PHASES)
        if name == "prompts":
            sp.add_argument("--all", action="store_true", help="Print full text for all briefs")

    sub.add_parser("next", help="Advance to next phase")
    sub.add_parser("status", help="Trial status")
    sub.add_parser("tally", help="Tally votes")
    sub.add_parser("render", help="Render VERDICT.md")

    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 1

    actions = {
        "plan": cmd_plan,
        "init": cmd_init,
        "prompts": cmd_prompts,
        "check": cmd_check,
        "next": cmd_next,
        "status": cmd_status,
        "tally": cmd_tally,
        "render": cmd_render,
    }
    actions[args.cmd](args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
