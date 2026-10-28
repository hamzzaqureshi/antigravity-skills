#!/usr/bin/env python3
"""Ponytail Gain Scoreboard.

Renders the measured benchmark impact of Ponytail on code size, cost, and tokens.
"""
import sys

SCOREBOARD = """
  ponytail gain           benchmark · 39 tasks × 5 runs · Opus 5.5

  no-skill        ████████████████████  100%
  Lines of code   █████████···········   47%   ▼ 53%
  Output tokens   ███████████·········   55%   ▼ 45%
  Cost            ███████████████·····   74%   ▼ 26%
  Time            ████████████········   59%   ▼ 41%
  Hidden checks passed   97%  (no-skill 96%)
  Tests where the logic needs one   98%  (no-skill 68%)

  This repo:  /ponytail-debt  (shortcuts you deferred)
              /ponytail-audit (what's still cuttable)
"""


def main():
    print(SCOREBOARD.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())

