# The Arena Skill

> When an AI assistant keeps giving you bad answers, make 100 versions fight to the death in a single-elimination tournament bracket. Zero dependencies, pure Python standard library.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-zero%20(stdlib)-success.svg)](#prerequisites-and-installation)
[![Bracket](https://img.shields.io/badge/tournament-100--agent%20bracket-orange.svg)](#how-it-works)

---

## Table of Contents

- [What Problem This Solves](#what-problem-this-solves)
- [Prerequisites and Installation](#prerequisites-and-installation)
- [Quickstart and Usage](#quickstart-and-usage)
- [How It Works: The 5-Phase Tournament](#how-it-works-the-5-phase-tournament)
- [Bracket Architecture and Progression](#bracket-architecture-and-progression)
- [What It Costs (Token and Wave Matrix)](#what-it-costs-token-and-wave-matrix)
- [Command-Line Reference (bracket.py)](#command-line-reference-bracketpy)
- [Strategy Cards and Diversity](#strategy-cards-and-diversity)
- [Scoring Rubric and Fatal Rule](#scoring-rubric-and-fatal-rule)
- [Testing](#testing)
- [Credits and License](#credits-and-license)

---

## What Problem This Solves

When an AI assistant produces a weak, incomplete, or broken response, prompting it repeatedly often leads to sycophantic variations of the same flawed logic.

The Arena skill solves this by turning solution generation into a rigorous adversarial competition:
1. **100 Diverse Competitors:** 100 sub-agents receive the exact same task text, byte for byte. Each receives a unique strategy card combining 15 reasoning modes, 12 workflows, and 12 strategies (2,160 possible cards).
2. **Adversarial Critique:** In pairs, each agent attacks the opponent's solution with concrete counterexamples, missed constraints, and logic errors.
3. **Defend and Revise:** Each agent defends its work, concedes valid criticisms, and rewrites its solution.
4. **Independent Judges:** A separate blind judge evaluates both revised solutions against a strict 100-point rubric. The loser is eliminated.
5. **Survival of the Fittest:** 100 becomes 50, then 25, 13, 7, 4, 2, and finally 1 surviving champion.

**Files remain untouched:** Sub-agents write only inside `.arena/`. The winning solution is presented for your review before any changes are applied.

---

## Prerequisites and Installation

### Prerequisites
- **Python:** `>= 3.8` (Standard library only; zero pip packages required)
- **Environment:** Antigravity IDE or Claude Code CLI

### Setup
Clone or place this skill in your skills folder:

```bash
# Antigravity IDE global discovery path
cp -r arena ~/.gemini/config/skills/

# Or project-local installation
mkdir -p .agents/skills
cp -r arena .agents/skills/
```

Verify the installation by running the test suite:

```bash
python3 -B -m unittest discover -s tests -v
# Output: Ran 28 tests in 0.67s ... OK
```

---

## Quickstart and Usage

### Natural Chat Triggers
Trigger the skill in Antigravity chat:
- `"/arena write the headline for our pricing page"`
- `"/arena --quick fix the flaky test in tests/test_api.py"`
- `"/arena --agents 32 plan our launch week, 6 hours per day budget"`
- `"That answer is bad. Make them compete in the arena."`

### Available Flags

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--agents N` | Number of competing sub-agents | `100` |
| `--quick` | Fast everyday tournament (16 agents, 4 rounds) | `16` |
| `--seed S` | Deterministic seed for reproducible cards and pairings | Random |
| `--wave W` | Concurrent sub-agents per wave | `10` |

---

## How It Works: The 5-Phase Tournament

1. **Spawn:** N sub-agents receive the exact same task text plus an assigned strategy card. Each writes an independent candidate solution.
2. **Attack:** Solutions are paired. Each side attacks the opponent's solution looking for fatal bugs, broken edge cases, or missed constraints (up to 7 ranked attacks).
3. **Defend:** Each competitor reviews the attacks it received, concedes genuine flaws or rebuts with evidence, and writes a standalone revised solution.
4. **Judge:** An independent judge scores both revised solutions against the rubric (Correctness 30, Completeness 25, Robustness 20, Specificity 15, Clarity 10). The fatal flaw rule prevents broken solutions from winning.
5. **Repeat and Champion:** The survivors advance to the next round until one champion remains. If a baseline rejected answer was provided, a final blind judge compares the champion against the baseline.

---

## Bracket Architecture and Progression

The tournament progression for 100 competitors:

```text
[100 Competitors] ──▶ Spawn Phase (100 solutions, 10 waves)
        │
        ▼
   [Round 1] ──▶ 50 matches (100 -> 50 survivors)
        │
        ▼
   [Round 2] ──▶ 25 matches (50 -> 25 survivors)
        │
        ▼
   [Round 3] ──▶ 12 matches + 1 bye (25 -> 13 survivors)
        │
        ▼
   [Round 4] ──▶ 6 matches + 1 bye (13 -> 7 survivors)
        │
        ▼
   [Round 5] ──▶ 3 matches + 1 bye (7 -> 4 survivors)
        │
        ▼
   [Round 6] ──▶ 2 matches (4 -> 2 survivors)
        │
        ▼
   [Round 7] ──▶ 1 championship match (2 -> 1 champion)
        │
        ▼
 [Final Check] ──▶ Blind check against rejected baseline
```

---

## What It Costs (Token and Wave Matrix)

The skill and tools are free and open source. Token costs scale with the number of competitors and rounds:

| Competitors | Rounds | Sub-Agent Calls | Waves of 10 | Recommended Use Case |
| :--- | :---: | :---: | :---: | :--- |
| **100 (Default)** | 7 | 595 | 70 | High-stakes architectural or strategic decisions |
| **64** | 6 | 379 | 49 | Complex algorithmic or multi-file refactoring |
| **32** | 5 | 187 | 28 | Hard debugging and race condition fixes |
| **16 (`--quick`)** | 4 | 91 | 16 | Everyday prompt improvements and copy writing |
| **8** | 3 | 43 | 10 | Quick sanity checks |

Plan your token budget anytime without writing files:

```bash
python3 bracket.py plan --agents 100
# Output: rounds: 7, calls: 595, waves: 70
```

---

## Command-Line Reference (bracket.py)

The state machine manages all tournament data inside `.arena/<run>/arena.json`:

```bash
# 1. Preview tournament size and calls
python3 bracket.py plan --agents 100

# 2. Initialize a tournament run
python3 bracket.py init --agents 100 --seed 7 --task-file task.md --baseline-file old.md

# 3. Check what to do next
python3 bracket.py next

# 4. Generate prompt briefs for a phase
python3 bracket.py prompts attack

# 5. Check missing outputs
python3 bracket.py check attack

# 6. View current round pairings
python3 bracket.py pairings

# 7. Collect judge verdicts and advance round
python3 bracket.py collect
python3 bracket.py advance

# 8. Check tournament status
python3 bracket.py status

# 9. Read the winning survivor
python3 bracket.py winner
```

---

## Strategy Cards and Diversity

Every competitor receives a distinct card dealt without repeats from `strategies.json`:
- **15 Reasoning Modes:** First principles, inversion, analogy, adversarial, constraint first, worked example, Socratic, contrarian, systems thinking, decomposition, working backwards, Pareto 80/20, premortem, dialectic, design thinking.
- **12 Workflows:** Draft-critique-rewrite, outline first, test first, research then synthesize, three drafts pick one, modular bottom-up, skeleton then muscle, checklist driven, assumption challenging, step-by-step verification, benchmark against gold standard, minimum viable then iterate.
- **12 Strategies:** Simplest thing that works, maximal rigour, user empathy first, edge cases first, speed and brevity, maintainability first, defensiveness and paranoia, zero assumptions, practical over clever, comprehensive coverage, elegance and polish, fail-safe defaults.

Total unique combinations: `15 x 12 x 12 = 2,160 cards`. Up to 144 agents, no two competitors share even two of their three dimensions.

---

## Scoring Rubric and Fatal Rule

All matches are scored against `rubric.md`:

| Criterion | Weight | Evaluation Question |
| :--- | :---: | :--- |
| **Correctness** | 30% | Is the solution accurate? Zero bugs, logic errors, or false claims. |
| **Completeness** | 25% | Does it address every requirement stated in the task? |
| **Robustness** | 20% | Does it survive attacks raised in the match, with valid rebuttals or fixes? |
| **Specificity** | 15% | Can the user act immediately without guessing missing details? |
| **Clarity** | 10% | Is the output well structured and proportional to the task? |

### The Fatal Flaw Rule
If a solution contains a verified fatal flaw (code that cannot run, broken core constraint, or severe safety issue), it cannot defeat a non-fatal solution regardless of point totals.

---

## Testing

Run the automated test suite across all 28 verification cases:

```bash
python3 -B -m unittest discover -s tests -v
```

All tests execute in under 1 second, require zero external dependencies, and leave zero bytecode residue.

---

## Credits and License

- **Original Author:** Jake Schincariol ([opusjake.ai](https://opusjake.ai))
- **License:** [MIT License](LICENSE) (Free to use, modify, and distribute)
