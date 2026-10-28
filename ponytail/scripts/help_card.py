#!/usr/bin/env python3
"""Ponytail Help & Quick Reference."""
import sys

HELP_TEXT = """
# Ponytail Quick Reference

## Intensity Levels
  - lite  : Build what was asked; name the smaller option in one line.
  - full  : (Default) Smallest complete change, test logic that needs it, name skipped work & risks.
  - ultra : Question the request and push back before building anything not strictly justified.

## Core Commands
  - /ponytail [lite|full|ultra|off] : Switch intensity or disable.
  - /ponytail-review                : Senior dev review of recent diff (bugs, load, missing tests, lean).
  - /ponytail-audit                 : Senior dev audit of entire repository, ranked by priority.
  - /ponytail-debt                  : Harvest and list all `shortcut:` comments into a debt ledger.
  - /ponytail-gain                  : Display measured benchmark savings scoreboard.
  - /ponytail-help                  : Show this reference card.

## Golden Rules
  1. YAGNI: The best code is the code you never write.
  2. Leverage what exists: house helpers > stdlib > native elements > installed deps.
  3. Never cut: validation at trust boundaries, error handling, security, accessibility.
  4. Shortest readable diff wins. Every non-trivial change leaves one small test.
"""


def main():
    print(HELP_TEXT.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())

