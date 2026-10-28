# Originality Audit & Attribution Protocol

> A rigorous framework for distinguishing between plagiarism, imitation, and transformation, with a 6-dimension scoring rubric and the 10 Creative Anti-Patterns.

---

## 1. The Definitional Triad

To prevent ethical compromises and derivative mediocrity, maintain strict boundaries:

```text
┌─────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────────┐
│   PLAGIARISM    │    │    IMITATION / PRACTICE   │    │        TRANSFORMATION         │
│                 │    │                           │    │                               │
│ Copying someone │    │ Recreating a technique in │    │ Combining multiple mechanisms │
│ else's work and │    │ private to learn its inner│    │ across domains to solve a new │
│ claiming it as  │    │ mechanics and structure.  │    │ problem under novel project   │
│ your own.       │    │ (Educational stepping     │    │ constraints with full credit. │
│                 │    │ stone).                   │    │                               │
│ UNACCEPTABLE │    │ PRACTICE ONLY          │    │ PRODUCTION GOAL            │
└─────────────────┘    └───────────────────────────┘    └───────────────────────────────┘
```

---

## 2. The 6-Dimension Originality Audit Rubric (Section 29)

Evaluate any candidate proposal, UI component, feature, or architecture across these 6 criteria (each scored 0-10, threshold for originality ≥ 45/60):

### 1. Source Awareness (0-10)
- **Low (0-3)**: Claims idea came from nowhere; ignorant of existing precedents or existing market solutions.
- **Medium (4-7)**: Aware of 1-2 obvious mainstream competitors or popular blog posts.
- **High (8-10)**: Traced lineage to primary literature, historical forebears, and edge-case implementations.

### 2. Transformation Depth (0-10)
- **Low (0-3)**: Superficial reskinning (changed variable names or color palette).
- **Medium (4-7)**: Adapted logic to a new programming language or framework without changing mechanics.
- **High (8-10)**: Extracted underlying conceptual primitive and completely re-engineered it to solve a fundamentally distinct friction point.

### 3. Synthesis & Combination (0-10)
- **Low (0-3)**: 1:1 clone of a single product/repo.
- **Medium (4-7)**: Blended 2 adjacent tools in the same vertical.
- **High (8-10)**: Fused 3+ orthogonal influences (e.g. game design progression + Unix piping + Swiss typography).

### 4. Contextual Fit (0-10)
- **Low (0-3)**: Cargo-culted feature that has no business being in this application (e.g., adding bento boxes to a terminal calculator).
- **Medium (4-7)**: Fits general user expectation but contains superfluous features copied from elsewhere.
- **High (8-10)**: Tailored precisely to project domain, constraints, and target users.

### 5. Attribution & Provenance (0-10)
- **Low (0-3)**: Attribution scrubbed to look "original" or innovative.
- **Medium (4-7)**: Casual mention buried in git commit messages.
- **High (8-10)**: Explicitly documented in README, code docstrings, and design lineage notes.

### 6. Independent Utility / Delta (0-10)
- **Low (0-3)**: Adds zero new value; worse or identical to the original.
- **Medium (4-7)**: Marginal quality-of-life improvements.
- **High (8-10)**: Substantially faster, cleaner, zero-dependency, more accessible, or uniquely capable.

---

## 3. The 10 Creative Anti-Patterns (Section 30)

| Anti-Pattern | Tell / Symptom | Corrective Operating Heuristic |
| :--- | :--- | :--- |
| **1. Waiting for Inspiration** | "I'll start when the plan is 100% clear." | **Start immediately.** Build a rough prototype. Making produces information. |
| **2. Consuming Without Making** | 50 browser tabs, endless tutorial videos, zero code written. | **Enforce 1:1 ratio.** Every 30 minutes of reading must yield 1 code experiment or note. |
| **3. Monolithic Copying** | "Let's copy Notion's exact workspace layout." | **Influence matrix.** Borrow Notion's block concept, Unix's composition, and TeX's typography. |
| **4. Bookmark Hoarding** | 2,000 unread bookmarks in Chrome folders. | **Active idea cards.** Delete linkdumps; convert high-signal items into structured YAML cards. |
| **5. The Genius Fallacy** | Refusing to look at existing tools to stay "pure". | **Study the giants.** You aren't original; you're just poorly read. Embrace the lineage. |
| **6. Sycophancy / Validation Trap**| Pivoting roadmap based on 1 Twitter reply or Reddit critic. | **Filter for patterns.** Require repeated corroborating evidence before altering course. |
| **7. Infinite Scope Paralysis** | "We are building an AI operating system that does everything." | **Subtract to the bone.** Pick 1 acute friction point and solve it with ruthless constraints. |
| **8. Monetization Compulsion** | Forcing every weekend hobby into a SaaS startup. | **Preserve playgrounds.** Keep exploratory sandbox experiments free from business metrics. |
| **9. Compulsive Broadcast** | Tweeting/posting before anything actually works. | **Embrace obscurity.** Polish quietly in early phases; share process artifacts when substance exists. |
| **10. Attribution-as-Excuse** | Copy-pasting 500 lines of proprietary code with a comment `// from repo X`. | **Transform, don't smuggle.** Attribution is respect, not a license to plagiarize verbatim. |
