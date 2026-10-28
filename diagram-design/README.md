# Diagram Design

[![Tests](https://img.shields.io/badge/tests-8%20passed-22c55e?style=flat-square)](tests/)
[![Types](https://img.shields.io/badge/types-45%20diagrams-38bdf8?style=flat-square)](SKILL.md)
[![Zero-Dependencies](https://img.shields.io/badge/dependencies-pure%20HTML%2BSVG-0ea5e9?style=flat-square)](scripts/antigravity_helper.py)
[![License](https://img.shields.io/badge/license-MIT-64748b?style=flat-square)](LICENSE)

> **Editorial diagram design for AI coding agents: 45 diagram types, pure self-contained HTML + SVG, zero drop-shadows, and zero Mermaid slop.**

---

## Overview

`diagram-design` produces publication-grade architectural schematics, sequence flows, state machines, and data pipelines without relying on brittle external rendering daemons. Every diagram renders natively as self-contained HTML and inline SVG with crisp typography, restrained line weights, and high-contrast color coding.

---

## 45 Diagram Types Across 9 Categories

- **Architecture & Systems**: Monolith-to-Microservices, C4 Container, Hexagonal/Ports-and-Adapters, Medallion Architecture.
- **Data & Pipelines**: ETL Data Flow, CDC Streaming, Medallion Lakehouse, Entity-Relationship (ER).
- **Security & Infrastructure**: Zero Trust Network, OAuth2 Token Exchange, VPC Network Topology.
- **Process & Sequencing**: Distributed Saga, Event-Driven Choreography, State Transitions.
- **Strategy & Strategy Maps**: Wardley Maps, Value Stream Chains, Capability Hierarchies.

---

## Quickstart & CLI

```bash
# Scaffold an editorial architecture diagram
python3 diagram-design/scripts/antigravity_helper.py scaffold architecture diagram.html --theme=antigravity-dark

# Validate diagram styling and constraints
python3 diagram-design/scripts/antigravity_helper.py validate diagram.html

# Convert Mermaid to Diagram IR
python3 diagram-design/scripts/antigravity_helper.py convert flow.mmd --out=diagram_ir.md

# Export standalone SVG
python3 diagram-design/scripts/antigravity_helper.py export-svg diagram.html diagram.svg
```

---

## Automated Verification

Run unit tests via standard Python `unittest`:
```bash
python3 -B -m unittest discover -s tests
```

