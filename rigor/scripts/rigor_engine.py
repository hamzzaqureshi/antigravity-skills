#!/usr/bin/env python3
"""Rigor Engine: Engineering discipline, grounding, task brief extraction, and completion gates."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def repo_root() -> Path:
    """Find the top-level git repository root or fall back to cwd."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return Path(out).resolve()
    except Exception:
        return Path.cwd().resolve()


def cmd_workspace(plan_path: str) -> str:
    """Initialize or return the run workspace under <root>/.rigor/runs/<slug>/."""
    plan_file = Path(plan_path).resolve()
    if not plan_file.is_file():
        raise FileNotFoundError(f"Plan file not found: {plan_path}")

    root = repo_root()
    slug = plan_file.stem
    ws = root / ".rigor" / "runs" / slug

    rigor_dir = root / ".rigor"
    rigor_dir.mkdir(parents=True, exist_ok=True)
    gitignore = rigor_dir / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("*\n", encoding="utf-8")

    ws.mkdir(parents=True, exist_ok=True)
    marker = ws / "plan-path"
    if marker.exists():
        existing_path = marker.read_text(encoding="utf-8").strip()
        if existing_path != str(plan_file):
            ws = root / ".rigor" / "runs" / f"{slug}-{plan_file.parent.name}"
            ws.mkdir(parents=True, exist_ok=True)
            marker = ws / "plan-path"

    if not marker.exists():
        marker.write_text(str(plan_file) + "\n", encoding="utf-8")

    return str(ws)


def extract_task_brief(content: str, task_n: int) -> str:
    """Extract Task N from markdown content, respecting code fences and sub-headings."""
    lines = content.splitlines()
    in_fence = False
    fence_marker = ""
    collecting = False
    parent_level = 0
    extracted_lines = []

    # Matches '#+ Task N' with word boundary on N
    task_regex = re.compile(rf"^#+\s+Task\s+{task_n}(?:\b|[:\s-])", re.IGNORECASE)
    any_task_regex = re.compile(r"^(#+)\s+Task\s+\d+", re.IGNORECASE)
    heading_regex = re.compile(r"^(#+)\s+(.+)")

    for line in lines:
        stripped = line.strip()

        # Handle fenced code blocks
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            if collecting:
                extracted_lines.append(line)
            continue

        if in_fence:
            if collecting:
                extracted_lines.append(line)
            continue

        # Outside fences, check headings
        h_match = heading_regex.match(line)
        if h_match:
            hashes, title = h_match.groups()
            level = len(hashes)

            if not collecting:
                if task_regex.match(line):
                    collecting = True
                    parent_level = level
                    extracted_lines.append(line)
            else:
                # If we hit another heading at or above the task's heading level, stop
                if level <= parent_level:
                    break
                else:
                    # Sub-heading inside the task (e.g. ### Step 1), keep it
                    extracted_lines.append(line)
        elif collecting:
            extracted_lines.append(line)

    return "\n".join(extracted_lines).strip()


def cmd_brief(plan_path: str, task_n_str: str, ws_path: str = None) -> str:
    """Extract Task N into <ws>/task-N-brief.md and print its path."""
    plan_file = Path(plan_path).resolve()
    if not plan_file.is_file():
        raise FileNotFoundError(f"Plan file not found: {plan_path}")

    try:
        task_n = int(task_n_str)
    except ValueError:
        raise ValueError(f"Task number must be an integer, got '{task_n_str}'")

    if not ws_path:
        ws_path = cmd_workspace(str(plan_file))

    ws = Path(ws_path)
    content = plan_file.read_text(encoding="utf-8")
    brief_content = extract_task_brief(content, task_n)

    if not brief_content:
        raise ValueError(f"Task {task_n} not found in {plan_path}")

    out_file = ws / f"task-{task_n}-brief.md"
    out_file.write_text(brief_content + "\n", encoding="utf-8")
    return str(out_file)


def cmd_ledger(ws_path: str, *line_parts: str) -> str:
    """Append one line to <ws>/progress.md and return the line."""
    ws = Path(ws_path)
    marker = ws / "plan-path"
    if not marker.exists():
        raise ValueError(f"Not a plan workspace (missing plan-path): {ws_path}")

    ledger_file = ws / "progress.md"
    if not ledger_file.exists():
        plan_ref = marker.read_text(encoding="utf-8").strip()
        ledger_file.write_text(f"# Rigor Ledger: plan {plan_ref}\n\n", encoding="utf-8")

    line = " ".join(line_parts).strip()
    with open(ledger_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")

    return line


def cmd_status(ws_path: str, as_json: bool = False) -> str:
    """Inspect progress ledger and compute next task and rulings."""
    ws = Path(ws_path)
    ledger_file = ws / "progress.md"
    if not ledger_file.is_file():
        raise FileNotFoundError(f"No ledger found at: {ledger_file}")

    lines = ledger_file.read_text(encoding="utf-8").splitlines()
    completed = []
    rulings_count = 0
    last_task_line = "none"

    for line in lines:
        stripped = line.strip()
        m_comp = re.match(r"^Task\s+(\d+):\s*complete\b", stripped, re.IGNORECASE)
        if m_comp:
            completed.append(int(m_comp.group(1)))
        if re.match(r"^Task\s+\d+:", stripped, re.IGNORECASE):
            last_task_line = stripped
        if stripped.startswith("Ruling") or stripped.startswith("Ruling:"):
            rulings_count += 1

    completed_sorted = sorted(list(set(completed)))
    next_task = 1
    for t in completed_sorted:
        if t >= next_task:
            next_task = t + 1

    data = {
        "workspace": str(ws),
        "completed_tasks": completed_sorted,
        "last_task_line": last_task_line,
        "next_task": next_task,
        "rulings": rulings_count,
    }

    if as_json:
        return json.dumps(data, indent=2)

    comp_str = " ".join(str(x) for x in completed_sorted) if completed_sorted else "none"
    output = [
        f"complete: {comp_str}",
        f"last task line: {last_task_line}",
        f"next task: {next_task}",
        f"rulings: {rulings_count}",
    ]
    return "\n".join(output)


def cmd_review_package(base: str, head: str = "HEAD", ws_path: str = None) -> str:
    """Generate git review package: commits, file stats, and unified diff."""
    # Verify git repository
    try:
        subprocess.check_call(["git", "rev-parse", "--verify", f"{base}^{{commit}}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["git", "rev-parse", "--verify", f"{head}^{{commit}}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise ValueError(f"Invalid git revisions: base='{base}', head='{head}'")

    # Verify base is an ancestor of head
    is_ancestor = subprocess.call(["git", "merge-base", "--is-ancestor", base, head]) == 0
    if not is_ancestor:
        raise ValueError(f"Head '{head}' is not built on base '{base}'")

    # Count commits
    count_str = subprocess.check_output(["git", "rev-list", "--count", f"{base}..{head}"], text=True).strip()
    if int(count_str) == 0:
        raise ValueError(f"Empty commit range: {base}..{head}")

    base_short = subprocess.check_output(["git", "rev-parse", "--short", base], text=True).strip()
    head_short = subprocess.check_output(["git", "rev-parse", "--short", head], text=True).strip()

    if not ws_path:
        ws_path = str(Path.cwd())
    ws = Path(ws_path)
    ws.mkdir(parents=True, exist_ok=True)

    out_file = ws / f"review-{base_short}..{head_short}.diff"

    log_out = subprocess.check_output(["git", "log", "--oneline", f"{base}..{head}"], text=True)
    stat_out = subprocess.check_output(["git", "diff", "--stat", f"{base}..{head}"], text=True)
    diff_out = subprocess.check_output(["git", "diff", "-U10", f"{base}..{head}"], text=True)

    content = [
        f"# Review package {base}..{head}",
        "",
        "## Commits",
        log_out.strip(),
        "",
        "## Files changed",
        stat_out.strip(),
        "",
        "## Diff",
        diff_out.strip(),
    ]

    out_file.write_text("\n".join(content) + "\n", encoding="utf-8")
    return str(out_file)


def cmd_verify_gate(text_or_file: str, strict: bool = False) -> dict:
    """
    Verify completion gate criteria:
    - Flags completion claims ('fixed', 'done', 'passing', 'complete', 'working', 'ready')
    - Checks for verifiable evidence: command output, exit codes, test counts, or Evidence Table
    """
    path_cand = Path(text_or_file)
    if path_cand.is_file():
        content = path_cand.read_text(encoding="utf-8")
    else:
        content = text_or_file

    claim_patterns = [
        r"\b(?:all\s+tests?\s+pass(?:ing|ed)?)\b",
        r"\b(?:bug|issue|defect|error)\s+(?:is\s+)?(?:fixed|resolved)\b",
        r"\b(?:task|work|feature|implementation)\s+(?:is\s+)?(?:done|complete(?:d)?|ready)\b",
        r"\b(?:build\s+(?:succeeds|passed|clean))\b",
        r"\b(?:everything\s+works)\b",
    ]

    evidence_patterns = [
        r"\|\s*Claim\s*\|\s*Command(?:\s+or\s+check)?\s*\|\s*Result\s*\|",
        r"\bexit\s+0\b",
        r"\b\d+\s+passed\b",
        r"\bOK\s+\(tests=\d+\)",
        r"\b0\s+failed\b",
        r"\b(?:tests?\s+passed|build\s+success)\b",
        r"Command exited with code 0",
    ]

    claims_found = []
    for pat in claim_patterns:
        matches = re.findall(pat, content, re.IGNORECASE)
        claims_found.extend(matches)

    has_evidence_table = bool(re.search(r"\|\s*Claim\s*\|\s*Command(?:\s+or\s+check)?\s*\|\s*Result\s*\|", content, re.IGNORECASE))
    
    evidence_found = []
    for pat in evidence_patterns:
        m = re.findall(pat, content, re.IGNORECASE)
        evidence_found.extend(m)

    # If there are no claims made, gate trivially passes
    if not claims_found:
        return {
            "passed": True,
            "claims": [],
            "evidence_table_present": has_evidence_table,
            "evidence_count": len(evidence_found),
            "reason": "No ungrounded completion claims detected",
        }

    # If claims are made, evidence must accompany them
    passed = len(evidence_found) > 0
    if strict and not has_evidence_table:
        passed = False

    reason = "Claims supported by fresh verification output" if passed else "Unsupported completion claims detected without verifiable execution output"
    return {
        "passed": passed,
        "claims": list(set(claims_found)),
        "evidence_table_present": has_evidence_table,
        "evidence_count": len(evidence_found),
        "reason": reason,
    }


def cmd_ground(tool_or_package: str) -> dict:
    """Grounding tool: inspect local CLI, binary, Python package, or npm module."""
    results = {"target": tool_or_package, "findings": []}

    # 1. Check CLI binary in PATH
    bin_path = shutil.which(tool_or_package)
    if bin_path:
        entry = {"type": "cli_binary", "path": bin_path}
        for flag in ["--version", "-V", "version"]:
            try:
                out = subprocess.check_output([bin_path, flag], stderr=subprocess.STDOUT, text=True, timeout=2).strip()
                if out:
                    entry["version_output"] = out.splitlines()[0]
                    break
            except Exception:
                continue
        results["findings"].append(entry)

    # 2. Check Python module
    try:
        py_cmd = f"import {tool_or_package}; print(getattr({tool_or_package}, '__file__', 'builtin')); print(getattr({tool_or_package}, '__version__', 'unknown'))"
        out = subprocess.check_output([sys.executable, "-c", py_cmd], stderr=subprocess.DEVNULL, text=True, timeout=2).strip().splitlines()
        results["findings"].append({
            "type": "python_module",
            "file": out[0] if len(out) > 0 else "unknown",
            "version": out[1] if len(out) > 1 else "unknown",
        })
    except Exception:
        pass

    # 3. Check npm / node package
    try:
        npm_path = shutil.which("npm")
        if npm_path:
            out = subprocess.check_output(["npm", "list", tool_or_package, "--depth=0"], stderr=subprocess.DEVNULL, text=True, timeout=3).strip()
            if tool_or_package in out:
                results["findings"].append({"type": "npm_package", "info": out.splitlines()[-1].strip()})
    except Exception:
        pass

    return results


def main():
    parser = argparse.ArgumentParser(description="Rigor Engine: Engineering discipline, grounding, and completion gates.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # workspace
    sp_ws = subparsers.add_parser("workspace", help="Print and create plan workspace")
    sp_ws.add_argument("plan", help="Path to plan.md")

    # brief
    sp_brief = subparsers.add_parser("brief", help="Extract Task N into task-N-brief.md")
    sp_brief.add_argument("plan", help="Path to plan.md")
    sp_brief.add_argument("task_n", help="Task number integer")
    sp_brief.add_argument("workspace", nargs="?", default=None, help="Workspace directory")

    # ledger
    sp_ledger = subparsers.add_parser("ledger", help="Append line to progress.md")
    sp_ledger.add_argument("workspace", help="Workspace directory")
    sp_ledger.add_argument("line", nargs="+", help="Line content to append")

    # status
    sp_status = subparsers.add_parser("status", help="Show completed tasks and next to run")
    sp_status.add_argument("workspace", help="Workspace directory")
    sp_status.add_argument("--json", action="store_true", help="Output as JSON")

    # review-package
    sp_rev = subparsers.add_parser("review-package", help="Generate review commits and diff")
    sp_rev.add_argument("base", help="Base commit / branch")
    sp_rev.add_argument("head", nargs="?", default="HEAD", help="Head commit / branch")
    sp_rev.add_argument("workspace", nargs="?", default=None, help="Output workspace directory")

    # verify-gate
    sp_gate = subparsers.add_parser("verify-gate", help="Verify completion gate evidence")
    sp_gate.add_argument("target", help="File path or text string to verify")
    sp_gate.add_argument("--strict", action="store_true", help="Require markdown evidence table")

    # ground
    sp_ground = subparsers.add_parser("ground", help="Ground tool, CLI, or package against primary sources")
    sp_ground.add_argument("target", help="Executable name, Python package, or npm library")

    args = parser.parse_args()

    try:
        if args.command == "workspace":
            print(cmd_workspace(args.plan))
        elif args.command == "brief":
            print(cmd_brief(args.plan, args.task_n, args.workspace))
        elif args.command == "ledger":
            print(cmd_ledger(args.workspace, *args.line))
        elif args.command == "status":
            print(cmd_status(args.workspace, as_json=args.json))
        elif args.command == "review-package":
            print(cmd_review_package(args.base, args.head, args.workspace))
        elif args.command == "verify-gate":
            res = cmd_verify_gate(args.target, strict=args.strict)
            if args.strict or not res["passed"]:
                print(json.dumps(res, indent=2))
                sys.exit(0 if res["passed"] else 1)
            else:
                print(json.dumps(res, indent=2))
        elif args.command == "ground":
            print(json.dumps(cmd_ground(args.target), indent=2))
    except Exception as exc:
        print(f"rigor error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

