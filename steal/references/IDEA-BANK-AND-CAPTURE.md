# Idea Bank & Capture Protocols

> Systematic workflows for capturing, tagging, curating, and retrieving creative ideas without falling into bookmark hoarding.

---

## 1. Collectors vs Hoarders (Section 2.2)

- **The Hoarder**: Saves hundreds of URLs, bookmarks, and screenshots into unindexed folders. Rarely reviews them; knowledge decays into digital landfill.
- **The Artist / Engineer**: Captures ideas through an interpretive lens. Extracts the *mechanism*, notes *why it matters*, tags it with *project applicability*, and attributes the *creator*.

---

## 2. The Idea Card Schema (Section 33)

Every captured item in `.artist/ideas.json` contains:

```yaml
id: "unique-kebab-slug"
title: "Descriptive name of the borrowed concept"
problem: "The friction or challenge this addresses"
inspiration: "The creative spark or observation"
source: "Original author, repository, book, or product"
source_type: "book | software | paper | ui | architecture | hardware | workflow"
mechanism: "The fundamental engine or rule making it work"
interesting_detail: "The subtle nuance that makes it delightful"
gap: "What the original source missed or failed to do"
adaptation: "How we repurpose or transform it for our project"
project_context: "Specific target file, module, or user journey"
constraint: "Limiting factor keeping the adaptation sharp"
prototype: "Minimal 30-minute test or sketch"
expected_value: "Concrete improvement in speed, clarity, or feel"
risk: "Potential failure mode or cognitive overhead"
evidence_needed: "What metric or test will validate success"
attribution: "Full formal attribution text"
status: "captured | prototyping | adopted | discarded"
tags: ["cli", "design-system", "caching", "ux"]
```

---

## 3. The Daily Logbook Protocol (Section 25)

A low-friction daily logbook preserves momentum and tracks skill growth over months:

```markdown
### 2026-10-06: Daily Log
- **WORKED ON:** Refactoring the telemetry ingest pipeline.
- **LEARNED:** Buffer pools prevent heap fragmentation under sustained 10k req/sec loads.
- **BUILT:** Zero-copy parser in 80 lines of C.
- **READ / WATCHED:** Austin Kleon's essay on analog scratchpads.
- **INTERESTING OBSERVATION:** Mechanical keyboards force deliberate keying, reducing hasty typos.
- **PROBLEM:** High memory footprint in legacy JSON deserializer.
- **NEXT STEP:** Replace dynamic reflection with static code generation.
```
