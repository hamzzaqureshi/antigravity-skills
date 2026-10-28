# [CLI Tool Name]

> [One-line hook: What does this CLI tool automate or solve? e.g. "Blazing-fast zero-dependency log sanitizer with streaming regex replacement."]

[![Release](https://img.shields.io/github/v/release/[owner]/[repo])](https://github.com/[owner]/[repo]/releases)
[![Crates.io](https://img.shields.io/crates/v/[crate].svg)](https://crates.io/crates/[crate])
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 10-Second Installation

### Homebrew (macOS / Linux)
```bash
brew install [owner]/tap/[tool]
```

### Cargo (Rust)
```bash
cargo install [tool]
```

### Go
```bash
go install github.com/[owner]/[tool]@latest
```

### Standalone Precompiled Binary
```bash
curl -fsSL https://raw.githubusercontent.com/[owner]/[repo]/main/install.sh | bash
```

---

## Quickstart & Examples

### Basic Usage
```bash
[tool] input.txt --output clean.txt
```

### Pipe & UNIX Stream Support
```bash
cat server.log | [tool] --filter error --format json | jq .
```

<!-- Add terminal demo GIF / SVG recording if available -->
<!-- ![CLI Demo](assets/demo.svg) -->

---

## Command Line Options & Flags

```text
Usage: [tool] [OPTIONS] <COMMAND>

Arguments:
  <INPUT>    Path to input file or '-' for stdin

Options:
  -c, --config <FILE>    Custom configuration file
  -o, --output <PATH>    Output destination (default: stdout)
  -v, --verbose          Enable detailed telemetry logs
  -q, --quiet            Silence all non-error output
  -h, --help             Print help information
  -V, --version          Print version information

Commands:
  scan       Audit directory for violations
  fix        Automatically apply remediations
  serve      Run in daemon background mode
```

---

## Exit Codes

For scripting and CI/CD pipelines, `[tool]` guarantees deterministic exit statuses:

| Exit Code | Meaning |
| :---: | :--- |
| `0` | Success / All checks passed cleanly |
| `1` | Violations or warnings detected |
| `2` | Configuration error or invalid flags |
| `127` | Target file or directory not found |

---

## Development & Testing

```bash
# Clone and build locally
git clone https://github.com/[owner]/[repo].git
cd [repo]

# Run test suite
cargo test # or: go test ./... / pytest
```
