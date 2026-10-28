#!/usr/bin/env python3
"""Interactive & CLI Tailored README Generator & Scaffolder.

Zero-dependency Python tool to scaffold tailored, professional GitHub READMEs
based on 6 proven project archetypes:
  - standard: All-purpose baseline (Standard Readme specification)
  - ai-ml: AI/ML, Data Science, HuggingFace models, PyTorch pipelines
  - backend-infra: APIs, microservices, Docker compose, ports, Kubernetes
  - cli-tool: Command-line utilities, Homebrew/cargo/go install, flags, exit codes
  - library: Reusable npm/PyPI/Cargo packages, API cheat sheets, compatibility
  - web-app: Next.js/React full-stack apps, live demo, scripts, local dev
"""

import argparse
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
TEMPLATES_DIR = SKILL_DIR / "templates"

ARCHETYPES = {
    "standard": "Standard Readme compliant all-purpose baseline",
    "ai-ml": "AI/ML, Data Science, Model weights, evaluation, CUDA/hardware",
    "backend-infra": "Backend service, Docker compose, ports, env, health checks",
    "cli-tool": "CLI tool, binary install, syntax, flags, exit codes",
    "library": "Reusable package/SDK, package managers, minimal import snippet",
    "web-app": "Frontend/Fullstack web app, live demo, scripts, dev setup",
}


def load_template(archetype: str) -> str:
    template_file = TEMPLATES_DIR / f"{archetype}.md"
    if not template_file.is_file():
        template_file = TEMPLATES_DIR / "standard.md"
    return template_file.read_text(encoding="utf-8")


def render_template(content: str, metadata: dict) -> str:
    name = metadata.get("name", "MyProject")
    owner = metadata.get("owner", "username")
    repo = metadata.get("repo", name.lower().replace(" ", "-"))
    desc = metadata.get("description", "A concise value proposition explaining what the project does.")
    license_type = metadata.get("license", "MIT")

    rendered = content.replace("[Project Name]", name)
    rendered = rendered.replace("[Model / Pipeline Name]", name)
    rendered = rendered.replace("[Service / Infrastructure Name]", name)
    rendered = rendered.replace("[CLI Tool Name]", name)
    rendered = rendered.replace("[Package / Library Name]", name)
    rendered = rendered.replace("[Application Name]", name)
    rendered = rendered.replace("[owner]", owner)
    rendered = rendered.replace("[org]", owner)
    rendered = rendered.replace("[repo]", repo)
    rendered = rendered.replace("[pkg]", repo)
    rendered = rendered.replace("[tool]", repo)
    rendered = rendered.replace("[model]", repo)
    rendered = rendered.replace("[model-name]", repo)
    rendered = rendered.replace("[crate]", repo)
    rendered = rendered.replace("[image]", repo)
    rendered = rendered.replace("[package-name]", repo)
    rendered = rendered.replace("[LICENSE]", license_type)
    rendered = rendered.replace("[A clear, compelling one-sentence value proposition explaining what the project does and why it matters.]", desc)
    rendered = rendered.replace("[Concise summary: What problem does this model/pipeline solve? State accuracy/benchmark score, architecture, and primary task.]", desc)
    rendered = rendered.replace("[High-level summary: What does this service do? Which protocols does it expose (REST/gRPC/GraphQL)? What is its SLA or throughput target?]", desc)
    rendered = rendered.replace("[One-line hook: What does this CLI tool automate or solve? e.g. \"Blazing-fast zero-dependency log sanitizer with streaming regex replacement.\"]", desc)
    rendered = rendered.replace("[Concise value statement: What functionality does this library export? e.g. \"Lightweight, zero-dependency resilient retry mechanism with exponential backoff and jitter.\"]", desc)
    rendered = rendered.replace("[Engaging elevator pitch: What does this web application do? e.g. \"Real-time collaborative markdown editor with live peer-to-peer sync and offline persistence.\"]", desc)

    return rendered


def interactive_wizard() -> dict:
    print("=" * 72)
    print("           README Scaffolder: The 5 Foundational Questions")
    print("=" * 72)
    print("\n1. What kind of project are you documenting?\n")
    arch_keys = list(ARCHETYPES.keys())
    for idx, k in enumerate(arch_keys, 1):
        print(f"  {idx}) {k:<15} - {ARCHETYPES[k]}")

    choice = input("\nSelect archetype [1-6] (default: 1): ").strip() or "1"
    try:
        archetype = arch_keys[int(choice) - 1]
    except (ValueError, IndexError):
        archetype = "standard"

    print(f"\n▶ Selected archetype: {archetype}\n")

    name = input("2. Project Name: ").strip() or "MyProject"
    owner = input("3. GitHub Username / Org (default: owner): ").strip() or "owner"
    repo = input(f"4. Repository Name (default: {name.lower().replace(' ', '-')}): ").strip() or name.lower().replace(" ", "-")
    description = input("5. One-sentence value proposition / hook:\n> ").strip()
    if not description:
        description = "A high-performance modular solution designed for production reliability."

    license_type = input("6. License (default: MIT): ").strip() or "MIT"

    return {
        "archetype": archetype,
        "name": name,
        "owner": owner,
        "repo": repo,
        "description": description,
        "license": license_type,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate tailored GitHub READMEs.")
    parser.add_argument("-a", "--archetype", choices=list(ARCHETYPES.keys()), help="Project archetype")
    parser.add_argument("-n", "--name", help="Project name")
    parser.add_argument("-d", "--description", help="One-sentence value hook")
    parser.add_argument("-u", "--owner", default="owner", help="GitHub username/org")
    parser.add_argument("-r", "--repo", help="Repository slug (e.g. my-tool)")
    parser.add_argument("-l", "--license", default="MIT", help="License type (default: MIT)")
    parser.add_argument("-o", "--output", help="Output path (default: stdout)")
    parser.add_argument("--list", action="store_true", help="List available archetypes")

    args = parser.parse_args()

    if args.list:
        print("Available Archetypes:")
        for k, v in ARCHETYPES.items():
            print(f"  • {k:<16} - {v}")
        sys.exit(0)

    if not args.archetype and not args.name and sys.stdin.isatty():
        metadata = interactive_wizard()
        archetype = metadata["archetype"]
    else:
        archetype = args.archetype or "standard"
        metadata = {
            "archetype": archetype,
            "name": args.name or "MyProject",
            "owner": args.owner,
            "repo": args.repo or (args.name.lower().replace(" ", "-") if args.name else "my-project"),
            "description": args.description or "A concise value proposition explaining what the project does.",
            "license": args.license,
        }

    raw = load_template(archetype)
    rendered = render_template(raw, metadata)

    if args.output:
        out_path = Path(args.output).resolve()
        out_path.write_text(rendered, encoding="utf-8")
        print(f"\n[OK] Successfully generated {archetype} README at: {out_path}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
