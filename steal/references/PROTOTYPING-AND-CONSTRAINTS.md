# Prototyping, Subtraction & Constraint Engineering

> Principles for turning vague visions into testable low-cost artifacts through deliberate constraints and gap-finding heuristics.

---

## 1. Small Artifact > Prolonged Speculation (Section 6)

When paralyzed by uncertainty or design debates, immediately halt theoretical discussion and produce a disposable artifact:

```text
Debate / Blocked Thought
          │
          ▼
Smallest Viable Artifact (in < 60 minutes)
   ├── Toy CLI script (50 lines)
   ├── Single HTML/CSS mockup (no framework)
   ├── Static markdown table
   └── 3-step ASCII workflow
          │
          ▼
Observable Reality
   ├── Reveals what actually works
   ├── Exposes unexpected friction
   └── Decides the architectural question with facts
```

---

## 2. The Gap-Finding Heuristic (Section 9)

Build the tool, feature, or document you desperately wish someone else had already built.

### The 8 Gap-Finding Questions:
1. **What do incumbent solutions aggressively ignore or treat as edge cases?**
2. **Where do current users suffer repetitive papercuts, extra clicks, or manual conversions?**
3. **What is bloated with 80% unnecessary enterprise complexity that could be a single CLI flag?**
4. **What missing metadata or intermediate representation would make existing tools 10x more powerful?**
5. **What would I want to reach for every single morning if it existed right now on my local machine?**
6. **What does the ideal zero-latency version look like without network roundtrips?**
7. **What technical obstacle or mental barrier prevents that ideal version from existing?**
8. **Can I build a working miniature proof-of-concept in an hour?**

---

## 3. The Power of Subtraction (Section 26)

Creativity flourishes under tight boundaries. When a project feels unfocused or overwhelming, execute a **Subtraction Pass**:

```text
Infinite Possibility ───► Decision Paralysis ───► Sluggish, generic output
                               ▲
                        Deliberate Cuts
                               ▼
Ruthless Constraints ───► Narrow Search Space ───► Sharp, distinctive craft
```

### The 7 Essential Constraint Injectors:

1. **Tooling Constraint**: "Use only standard library Python (no external pip dependencies)."
2. **Interface Constraint**: "Zero buttons; everything driven by a single text prompt or CLI command."
3. **Temporal Constraint**: "Must complete execution and print output in under 50 milliseconds."
4. **Volume Constraint**: "Explain the entire operational concept in under 120 lines of markdown."
5. **Format Constraint**: "Zero databases; persistent state stored exclusively in human-readable plain text / JSON."
6. **Styling Constraint**: "Maximum 2 font families, 3 type sizes, and 1 accent color."
7. **Scope Constraint**: "Do one thing with extraordinary precision; reject all adjacent feature requests."

---

## 4. Analog & Low-Friction Thinking (Section 10)

Digital text boxes encourage premature editing, syntax obsession, and premature optimization.
- **Physical Whiteboards / Scratchpad**: Use for conceptual arrangement, sequence ordering, and node mapping.
- **Terminal Scratch Files**: Write raw markdown lists or pseudocode before structuring formal classes or schema models.
- **Separation of Modes**: Keep the *Generation Mode* (unfiltered idea capture) strictly separated from the *Editing Mode* (rigorous code linting and refactoring).
