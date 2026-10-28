#!/usr/bin/env python3
"""Steal Like an Artist CLI - Reusable Creative Operating System Engine.

A zero-dependency Python tool for managing creative lineages, capturing idea
thefts, auditing originality, enforcing constraints, and tracking creative logs.
Conforms strictly to Austin Kleon's "Steal Like an Artist" operational model.
"""
import argparse
import datetime
import json
import os
import re
import sys

ARTIST_DIR = ".artist"


def get_artist_path(base_path=None):
    base = base_path or os.getcwd()
    return os.path.join(base, ARTIST_DIR)


def ensure_init(base_path=None):
    artist_path = get_artist_path(base_path)
    if not os.path.isdir(artist_path):
        os.makedirs(artist_path, exist_ok=True)
    ideas_file = os.path.join(artist_path, "ideas.json")
    if not os.path.isfile(ideas_file):
        with open(ideas_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0", "ideas": []}, f, indent=2)
    lineage_file = os.path.join(artist_path, "lineage.json")
    if not os.path.isfile(lineage_file):
        with open(lineage_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0", "lineage": []}, f, indent=2)
    logbook_file = os.path.join(artist_path, "logbook.md")
    if not os.path.isfile(logbook_file):
        with open(logbook_file, "w", encoding="utf-8") as f:
            f.write("# Creative Logbook\n\nDaily entries tracking work, learnings, and experiments.\n\n---\n")
    return artist_path


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)[:48]


# --- COMMAND: init ---
def cmd_init(args):
    artist_path = ensure_init(args.path)
    if args.json:
        print(json.dumps({"status": "initialized", "path": artist_path}))
    else:
        print(f"[OK] Initialized Steal Like an Artist OS in: {artist_path}")
        print("  - Ideas Bank:    .artist/ideas.json")
        print("  - Lineage Graph: .artist/lineage.json")
        print("  - Daily Logbook: .artist/logbook.md")


# --- COMMAND: capture ---
def cmd_capture(args):
    ensure_init()
    ideas_file = os.path.join(get_artist_path(), "ideas.json")
    with open(ideas_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    idea_id = slugify(args.title or f"idea-{len(data['ideas']) + 1}")
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    card = {
        "id": idea_id,
        "title": args.title or "Untitled Idea",
        "problem": args.problem or "Unspecified problem",
        "inspiration": args.inspiration or "",
        "source": args.source or "Unknown source",
        "source_type": args.source_type or "software",
        "mechanism": args.mechanism or "Core operational mechanism",
        "interesting_detail": args.detail or "",
        "gap": args.gap or "What current implementations miss",
        "adaptation": args.adaptation or "How we repurpose it",
        "project_context": args.context or "",
        "constraint": args.constraint or "",
        "prototype": args.prototype or "",
        "expected_value": args.value or "",
        "risk": args.risk or "",
        "evidence_needed": args.evidence or "",
        "attribution": args.attribution or args.source or "",
        "status": "captured",
        "tags": tags,
        "created_at": datetime.datetime.now().isoformat()
    }

    # Upsert by ID
    existing = [i for i in data["ideas"] if i["id"] == idea_id]
    if existing:
        data["ideas"] = [card if i["id"] == idea_id else i for i in data["ideas"]]
        action = "Updated"
    else:
        data["ideas"].append(card)
        action = "Captured"

    with open(ideas_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    if args.json:
        print(json.dumps({"status": "success", "action": action, "card": card}))
    else:
        print(f"[OK] {action} Idea Card [{card['id']}]: '{card['title']}'")
        print(f"  Source:      {card['source']} ({card['source_type']})")
        print(f"  Mechanism:   {card['mechanism']}")
        print(f"  Adaptation:  {card['adaptation']}")
        if card["attribution"]:
            print(f"  Attribution: {card['attribution']}")


# --- COMMAND: audit (Originality Check) ---
def cmd_audit(args):
    content = ""
    target_name = "input"
    if args.file:
        target_name = args.file
        if not os.path.isfile(args.file):
            print(f"Error: Target file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        # If neither provided, check ideas.json
        ideas_file = os.path.join(get_artist_path(), "ideas.json")
        if os.path.isfile(ideas_file):
            target_name = ".artist/ideas.json"
            with open(ideas_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            print("Error: No file or text provided to audit, and no .artist/ideas.json found.", file=sys.stderr)
            sys.exit(2)

    # Section 29 6-Dimension Originality Evaluation
    scores = {}
    feedback = {}
    anti_patterns = []

    # 1. Source Awareness
    source_matches = len(re.findall(r"(?:source|precedent|prior art|inspired by|lineage|referenced|origin)", content, re.I))
    if source_matches >= 3:
        scores["source_awareness"] = 10
        feedback["source_awareness"] = "Strong lineage and precedent awareness."
    elif source_matches >= 1:
        scores["source_awareness"] = 7
        feedback["source_awareness"] = "Basic source awareness indicated."
    else:
        scores["source_awareness"] = 3
        feedback["source_awareness"] = "Low source awareness; risks inventing in a vacuum or claiming isolated originality."
        anti_patterns.append("The Genius Fallacy (acting as if idea emerged from an empty room)")

    # 2. Transformation Depth
    transform_matches = len(re.findall(r"(?:transform|adapt|changed|repurpose|extracted mechanism|adapted|modified|overhauled)", content, re.I))
    if transform_matches >= 3:
        scores["transformation_depth"] = 10
        feedback["transformation_depth"] = "Deep transformation: moves beyond surface styling to structural adaptation."
    elif transform_matches >= 1:
        scores["transformation_depth"] = 7
        feedback["transformation_depth"] = "Moderate transformation noted."
    else:
        scores["transformation_depth"] = 3
        feedback["transformation_depth"] = "Superficial transformation: danger of mere reskinning or shallow copying."
        anti_patterns.append("Monolithic or Surface Copying without structural alteration")

    # 3. Synthesis & Combination
    influences_count = len(re.findall(r"(?:influence|borrowed from|combined with|cross-domain|fusion)", content, re.I))
    if influences_count >= 3:
        scores["synthesis_and_combination"] = 10
        feedback["synthesis_and_combination"] = "Multi-source synthesis combining 3+ distinct influences."
    elif influences_count >= 1:
        scores["synthesis_and_combination"] = 7
        feedback["synthesis_and_combination"] = "Combines 2 influences."
    else:
        scores["synthesis_and_combination"] = 4
        feedback["synthesis_and_combination"] = "Single source dominance: dependent on a single reference point."
        anti_patterns.append("Single Source Copying (risks direct imitation)")

    # 4. Contextual Fit & Specificity
    context_matches = len(re.findall(r"(?:constraint|context|project|domain|target user|audience|specific)", content, re.I))
    if context_matches >= 3:
        scores["contextual_fit"] = 10
        feedback["contextual_fit"] = "Grounded tightly in domain constraints and specific project context."
    elif context_matches >= 1:
        scores["contextual_fit"] = 7
        feedback["contextual_fit"] = "Acceptable project contextualization."
    else:
        scores["contextual_fit"] = 4
        feedback["contextual_fit"] = "Generic or disconnected from specific constraints."

    # 5. Attribution & Provenance
    attr_matches = len(re.findall(r"(?:attribution|credit|author|license|courtesy|originally by|citation)", content, re.I))
    if attr_matches >= 2:
        scores["attribution_and_provenance"] = 10
        feedback["attribution_and_provenance"] = "Formal attribution and provenance documented."
    elif attr_matches >= 1:
        scores["attribution_and_provenance"] = 7
        feedback["attribution_and_provenance"] = "Attribution mentioned."
    else:
        scores["attribution_and_provenance"] = 2
        feedback["attribution_and_provenance"] = "Attribution missing! Never scrub sources to appear original."
        anti_patterns.append("Plagiarism Risk: Missing explicit attribution")

    # 6. Independent Value & Delta
    delta_matches = len(re.findall(r"(?:difference|gap|unique|advantage|faster|lighter|offline|distinct|value)", content, re.I))
    if delta_matches >= 3:
        scores["independent_value"] = 10
        feedback["independent_value"] = "Clear delta and independent utility solving a concrete friction point."
    elif delta_matches >= 1:
        scores["independent_value"] = 7
        feedback["independent_value"] = "Demonstrable improvements over precursors."
    else:
        scores["independent_value"] = 4
        feedback["independent_value"] = "Unclear delta: why should this exist over incumbents?"

    # Check for Infinite Scope Buzzwords
    buzzwords = re.findall(r"(?:all-in-one|revolutionize|disrupt everything|next-gen ai operating system|infinite scale)", content, re.I)
    if buzzwords:
        anti_patterns.append(f"Infinite Scope Buzzwords detected: {', '.join(set(buzzwords))}")
        scores["contextual_fit"] = max(2, scores["contextual_fit"] - 3)

    raw_total = sum(scores.values())
    max_total = 60
    final_percentage = round((raw_total / max_total) * 100)

    passed = final_percentage >= args.threshold

    result = {
        "target": target_name,
        "score": final_percentage,
        "threshold": args.threshold,
        "passed": passed,
        "dimensions": scores,
        "feedback": feedback,
        "anti_patterns": anti_patterns
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status_symbol = "[OK] PASS" if passed else "✖ FAIL"
        print("=" * 64)
        print(f"       STEAL LIKE AN ARTIST - ORIGINALITY AUDIT: {status_symbol}")
        print("=" * 64)
        print(f"Target:    {target_name}")
        print(f"Score:     {final_percentage}/100 (Threshold: {args.threshold})")
        print("-" * 64)
        print(f"{'Dimension':<30} | {'Score':<6} | {'Status'}")
        print("-" * 64)
        for dim, sc in scores.items():
            print(f"{dim.replace('_', ' ').title():<30} | {sc}/10   | {feedback[dim]}")
        print("-" * 64)
        if anti_patterns:
            print("[WARN]  DETECTED ANTI-PATTERNS:")
            for ap in anti_patterns:
                print(f"   • {ap}")
            print("-" * 64)
        if passed:
            print("[OK] Artifact demonstrates healthy transformation and multi-source lineage.")
        else:
            print("✖ Action Required: Deepen transformation, cite sources, and enforce tight constraints.")
        print("=" * 64)

    sys.exit(0 if passed else 1)


# --- COMMAND: lineage ---
def cmd_lineage(args):
    ensure_init()
    lineage_file = os.path.join(get_artist_path(), "lineage.json")
    with open(lineage_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if args.add:
        node_id = slugify(args.add)
        node = {
            "id": node_id,
            "name": args.add,
            "category": args.category or "direct",
            "mechanism": args.mechanism or "",
            "unexpected": bool(args.unexpected),
            "parent_id": args.parent or "root",
            "created_at": datetime.datetime.now().isoformat()
        }
        data["lineage"].append(node)
        with open(lineage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Added lineage node [{node['id']}]: '{node['name']}' ({node['category']})")
        return

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print("=" * 60)
    print("                 PROJECT CREATIVE LINEAGE")
    print("=" * 60)
    if not data["lineage"]:
        print("  (No lineage nodes recorded yet. Add via: artist lineage --add <name>)")
    else:
        print("PROJECT (Root)")
        for n in data["lineage"]:
            cat_badge = f"[{n['category'].upper()}]"
            mech_str = f" - Mechanism: {n['mechanism']}" if n.get("mechanism") else ""
            print(f"  ├── {n['name']} {cat_badge}{mech_str}")
    print("=" * 60)


# --- COMMAND: log ---
def cmd_log(args):
    ensure_init()
    logbook_file = os.path.join(get_artist_path(), "logbook.md")
    today = datetime.date.today().isoformat()

    entry = f"""
### {today}: Daily Creative Log
- **WORKED ON:** {args.worked or 'General implementation'}
- **LEARNED:** {args.learned or 'Practical insights and feedback'}
- **BUILT:** {args.built or 'New artifact or experiment'}
- **READ / WATCHED:** {args.read or 'Reference literature'}
- **INTERESTING OBSERVATION:** {args.observation or 'Pattern noted'}
- **PROBLEM:** {args.problem or 'Active friction point'}
- **NEXT STEP:** {args.next_step or 'Upcoming iteration'}
"""
    with open(logbook_file, "a", encoding="utf-8") as f:
        f.write(entry)

    if args.json:
        print(json.dumps({"status": "logged", "date": today}))
    else:
        print(f"[OK] Appended daily log entry for {today} in .artist/logbook.md")


# --- COMMAND: recommend ---
def cmd_recommend(args):
    title = args.title or "Feature / Idea Synthesis"
    problem = args.problem or "Identified user or architectural friction"
    sources = args.sources.split(",") if args.sources else ["Precedent A", "Precedent B"]
    steals = args.steals.split(",") if args.steals else ["Mechanism 1", "Mechanism 2"]
    change = args.change or "Transformed to fit our local offline architecture"
    constraint = args.constraint or "Zero external dependencies, < 50ms latency"
    prototype = args.prototype or "50-line CLI script in scripts/"

    output = f"""# Creative Recommendation: {title}

### Problem
{problem}

### Existing Influences
{chr(10).join(f"- {s.strip()}" for s in sources)}

### What We Steal
{chr(10).join(f"- {st.strip()}" for st in steals)}

### What We Change
{change}

### Why It Fits
Directly solves our friction without introducing extraneous abstractions.

### Constraint
{constraint}

### Smallest Prototype
{prototype}

### Evidence
Measurable reduction in friction and passing test suites.

### Attribution / Provenance
Influences derived from {', '.join(s.strip() for s in sources)}.

### Next Iteration
Run Section 29 Originality Audit and integrate into production code.
"""
    print(output)


# --- COMMAND: review ---
def cmd_review(args):
    review_template = f"""## Creative Review: Project Phase ({datetime.date.today().isoformat()})

### What influenced us?
- Primary architecture precedents and domain literature.

### What did we learn?
- Action generates information that prolonged speculation cannot.

### What did we imitate for practice?
- Internal test implementations and mock prototypes.

### What did we transform?
- Abstract concepts into concrete, offline, zero-dependency tools.

### What emerged unexpectedly?
- Cross-domain transfers clarifying ergonomics.

### What did we remove?
- Fluff, premature micro-features, and unnecessary dependencies.

### What constraints helped?
- Strict standard library runtime and fast test execution.

### What failed?
- Overly generic initial models; resolved by sharpening scope.

### What feedback mattered?
- Concrete test cases and regression suites.

### What remains unresolved?
- Long-term scaling benchmarks.

### What should enter the idea bank?
- Adjacent CLI utilities and workflow automations.

### What should enter the creative lineage?
- New high-signal engineering and design references.

### What should we build next?
- The next smallest viable artifact.
"""
    print(review_template)


# --- COMMAND: status ---
def cmd_status(args):
    ensure_init()
    ideas_file = os.path.join(get_artist_path(), "ideas.json")
    lineage_file = os.path.join(get_artist_path(), "lineage.json")
    with open(ideas_file, "r", encoding="utf-8") as f:
        ideas_data = json.load(f)
    with open(lineage_file, "r", encoding="utf-8") as f:
        lineage_data = json.load(f)

    print("=" * 60)
    print("             STEAL LIKE AN ARTIST - STATUS")
    print("=" * 60)
    print(f"Ideas Bank:     {len(ideas_data.get('ideas', []))} captured ideas")
    print(f"Lineage Graph:  {len(lineage_data.get('lineage', []))} recorded influences")
    print(f"Logbook:        .artist/logbook.md")
    print("=" * 60)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Steal Like an Artist CLI - Reusable Creative Operating System Engine"
    )
    sub = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # init
    p_init = sub.add_parser("init", help="Initialize .artist workspace")
    p_init.add_argument("--path", help="Target directory (default current dir)")
    p_init.add_argument("--json", action="store_true", help="Output JSON")

    # capture
    p_cap = sub.add_parser("capture", help="Capture an idea card")
    p_cap.add_argument("--title", required=True, help="Idea title")
    p_cap.add_argument("--problem", help="Friction or problem addressed")
    p_cap.add_argument("--source", required=True, help="Origin / creator / tool")
    p_cap.add_argument("--source-type", dest="source_type", help="book/software/ui/workflow")
    p_cap.add_argument("--mechanism", required=True, help="Underlying mechanic")
    p_cap.add_argument("--adaptation", required=True, help="How we adapt it")
    p_cap.add_argument("--inspiration", help="Spark or observation")
    p_cap.add_argument("--detail", help="Interesting subtle detail")
    p_cap.add_argument("--gap", help="What original missed")
    p_cap.add_argument("--context", help="Target project context")
    p_cap.add_argument("--constraint", help="Sharpening constraint")
    p_cap.add_argument("--prototype", help="Minimal test experiment")
    p_cap.add_argument("--value", help="Expected improvement")
    p_cap.add_argument("--risk", help="Known risk")
    p_cap.add_argument("--evidence", help="Validation criteria")
    p_cap.add_argument("--attribution", help="Formal credit text")
    p_cap.add_argument("--tags", help="Comma-separated tags")
    p_cap.add_argument("--json", action="store_true", help="Output JSON")

    # audit
    p_aud = sub.add_parser("audit", help="Run Section 29 Originality Audit")
    p_aud.add_argument("--file", help="File to audit")
    p_aud.add_argument("--text", help="Direct text to audit")
    p_aud.add_argument("--threshold", type=int, default=70, help="Pass threshold (default 70)")
    p_aud.add_argument("--json", action="store_true", help="Output JSON")

    # lineage
    p_lin = sub.add_parser("lineage", help="Manage and display lineage tree")
    p_lin.add_argument("--add", help="Add influence name")
    p_lin.add_argument("--category", choices=["direct", "cross-domain", "negative"], default="direct")
    p_lin.add_argument("--mechanism", help="Transferable mechanism")
    p_lin.add_argument("--unexpected", action="store_true", help="Mark as unexpected domain")
    p_lin.add_argument("--parent", help="Parent node ID")
    p_lin.add_argument("--json", action="store_true", help="Output JSON")

    # log
    p_log = sub.add_parser("log", help="Append daily logbook entry")
    p_log.add_argument("--worked", help="What was worked on")
    p_log.add_argument("--learned", help="What was learned")
    p_log.add_argument("--built", help="What was built")
    p_log.add_argument("--read", help="What was read or watched")
    p_log.add_argument("--observation", help="Interesting observation")
    p_log.add_argument("--problem", help="Active problem")
    p_log.add_argument("--next-step", dest="next_step", help="Next step")
    p_log.add_argument("--json", action="store_true", help="Output JSON")

    # recommend
    p_rec = sub.add_parser("recommend", help="Generate Section 32 recommendation block")
    p_rec.add_argument("--title", help="Idea title")
    p_rec.add_argument("--problem", help="Problem statement")
    p_rec.add_argument("--sources", help="Comma-separated sources")
    p_rec.add_argument("--steals", help="Comma-separated mechanisms stolen")
    p_rec.add_argument("--change", help="Transformation details")
    p_rec.add_argument("--constraint", help="Sharpening constraint")
    p_rec.add_argument("--prototype", help="Smallest prototype")

    # review
    p_rev = sub.add_parser("review", help="Generate Section 34 creative review")

    # status
    p_stat = sub.add_parser("status", help="Print overall creative status")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    handlers = {
        "init": cmd_init,
        "capture": cmd_capture,
        "audit": cmd_audit,
        "lineage": cmd_lineage,
        "log": cmd_log,
        "recommend": cmd_recommend,
        "review": cmd_review,
        "status": cmd_status
    }
    handlers[args.subcommand](args)


if __name__ == "__main__":
    main()
