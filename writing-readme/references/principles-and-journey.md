# Principles & The Reader's Journey

> "A README is often the first thing someone sees when they open your repository. Good documentation lets them understand and use the project without digging through its implementation."

---

## The Reader's Journey

When an engineer, recruiter, or collaborator arrives at a repository, they progress through four distinct psychological stages. Your README must satisfy each stage in order:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│ 1. Discover  │ ──▶ │2. Understand │ ──▶ │   3. Start   │ ──▶ │ 4. Use or Contribute │
│ What is this?│     │ Why care?    │     │ How to run?  │     │ How to integrate?    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────────────┘
```

### Stage 1: Discover (< 5 seconds)
- **Reader Question:** *"Am I in the right place? What is this project called and what category is it in?"*
- **README Answer:** Crisp title, one-sentence hook/elevator pitch, key tags or badges.
- **Anti-pattern:** Jumping straight into a 50-line installation script or an uncontextualized code diff.

### Stage 2: Understand (< 30 seconds)
- **Reader Question:** *"Does this solve my specific problem? What does it do that alternatives don't?"*
- **README Answer:** Value proposition, problem/solution statement, hero screenshot or terminal recording, feature highlights.
- **Anti-pattern:** Vague buzzwords like *"a powerful enterprise solution for tomorrow's web"*.

### Stage 3: Start (< 2 minutes)
- **Reader Question:** *"Can I actually install and run this on my machine without hidden blockers?"*
- **README Answer:** Explicit prerequisites (versions, OS), clean copy-pasteable installation commands, expected output verification.
- **Anti-pattern:** Assuming dependencies are installed, omitting environment variable setup, broken commands.

### Stage 4: Use or Contribute (< 10 minutes)
- **Reader Question:** *"How do I adapt this for my use case, or how do I submit a bug fix?"*
- **README Answer:** Working minimal code examples, API cheat sheet, test suite invocation, contribution guidelines, license.

---

## Foundational Design Principles

### 1. Lead with Value Before Machinery
Explain the **problem, user, and outcome** before explaining the configuration flags and Docker networks. A reader needs a reason to care before they invest time in setup.

### 2. Respect the Reader's Cognitive Budget
Documentation should minimize friction. Remove unnecessary prose, use scannable bullet points, bold key terms, and format commands in copyable code blocks with language tags.

### 3. README-Driven Development (RDD)
Writing documentation *before* or *during* implementation is a superpower. Drafting the README forces you to design clean APIs, sensible CLI flags, and clear installation steps before you write messy code that is hard to explain. If a feature is awkward to explain in a README, the API design itself is usually flawed.

### 4. Maintain Proportionality
- A single-file utility script needs a 1-page README.
- A multi-tier microservice cluster needs architecture diagrams, port tables, and docker-compose steps.
- Do not bloat a simple package with enterprise ceremony; do not starve a complex system of operational guides.

### 5. Disclose Limitations to Build Trust
Every production system has boundaries (unsupported platforms, rate limits, performance bottlenecks, beta features). State them candidly. A project that honestly documents its edge cases inspires 10x more trust than one that claims to be completely infallible.
