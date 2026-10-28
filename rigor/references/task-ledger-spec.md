# Rigor: Task Ledger & Workspace Specification

The Task Ledger ensures that execution state survives agent context compaction, tool limits, and subagent boundaries.

---

## 1. Directory Structure

Workspaces are created under the repository root:
```
<repo-root>/
├── .rigor/
│   ├── .gitignore             # Automatically contains '*' to avoid polluting git status
│   └── runs/
│       └── <plan-slug>/
│           ├── plan-path      # Absolute path to the original plan file
│           ├── progress.md    # Surviving execution ledger
│           ├── task-1-brief.md
│           ├── task-2-brief.md
│           └── review-base..head.diff
```

---

## 2. Progress Ledger Format (`progress.md`)

```markdown
# Rigor Ledger: plan /path/to/plan.md

Task 1: complete (SHA: a1b2c3d, 12 unit tests passing)
Task 2: in_progress (subagent-id: conv_12345)
Ruling: rejected suggestion to add redis cache; keep standard library in-memory dict
Task 2: complete (SHA: d4e5f6g, integration test green)
```

---

## 3. CLI Management

Use `rigor` directly from shell or scripts:
```bash
# Initialize workspace
ws=$(rigor workspace docs/plans/2026-auth.md)

# Extract atomic task brief for subagent
brief=$(rigor brief docs/plans/2026-auth.md 2 "$ws")

# Record progress
rigor ledger "$ws" "Task 2: complete (SHA: d4e5f6g)"

# Inspect status
rigor status "$ws"
```

