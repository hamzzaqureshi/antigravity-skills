# REA: Reverse Engineer Anything

> One Model Context Protocol (MCP) skill to reverse engineer applications, binaries, and runtime behavior. See a feature you like? Understand how it works down to the binary level, show the evidence, and build a clean version for your project.

---

## What You Can Analyze

| Target Format | What REA Returns | Analysis Provider | REA MCP Tool Route |
| :--- | :--- | :--- | :--- |
| **Native Binaries (ELF / Mach-O / PE)** | Pseudocode, assembly, symbols, references, and strings | Hopper, Ghidra, or IDA | `open_binary`, `binary_overview` |
| **JavaScript / Electron Apps** | Modules, imports, source maps, routes, IPC channels, preload bridges | Built-in Node (zero native engine needed) | `analyze_javascript_application` |
| **Android APKs** | Manifest declarations, classes, decompiled methods, resource strings | Headless JADX + JDK | `inspect_android_package` |
| **.NET Assemblies** | Metadata, CIL instructions, native dependencies | Static PE/CLI reader | `inspect_managed_artifact` |
| **WebAssembly (WASM)** | Sections, imports/exports, decoded WAT representation | WABT (wasm2wat) | `inspect_wasm_artifact` |
| **EVM Bytecode** | Dispatch selectors, byte offsets, inferred function signatures | Offline EVM parser | `inspect_evm_interface` |
| **Firmware Images** | Memory regions, extraction results, native handoffs | Binwalk / Unblob | `inspect_firmware_regions` |
| **Network Captures** | Requests, responses, source locations, exposed payloads | HAR / mitmproxy | `inspect_web_network_capture` |
| **Linux ELF Diagnostics** | Sections, relocations, original symbols, mitigations | pwntools | `inspect_binary_layout` |

---

## Quick Start: Register REA with Your Agent

REA connects to your AI agent as an MCP server.

### 1. Requirements
- Node.js >= 22.19 (Run `python3 scripts/rea_helper.py readiness` to verify your environment)
- npm

### 2. Configure MCP in Antigravity IDE
Add the REA server entry into your global Antigravity MCP configuration:
`~/.gemini/config/mcp_config.json`

```json
{
  "mcpServers": {
    "rea": {
      "command": "npx",
      "args": ["-y", "rea-agents@latest", "mcp"]
    }
  }
}
```

Or run the interactive setup tool:
```bash
npx rea-agents setup
```

---

## Bundled Helper Tool (`rea_helper.py`)

A zero-dependency CLI tool is included in `scripts/`:

```bash
# 1. Audit local environment readiness
python3 scripts/rea_helper.py readiness

# 2. Inspect an artifact and get the exact REA tool routing
python3 scripts/rea_helper.py route /path/to/app.asar
python3 scripts/rea_helper.py route ./target/release/my_binary

# 3. Output MCP configuration block
python3 scripts/rea_helper.py mcp-config
```

---

## How to Trigger REA in Conversation

Trigger the skill naturally by providing a target path or binary:

- **Electron App Inspection:**
  > *"Inspect the Slack desktop ASAR at `/opt/slack/resources/app.asar` and trace how it handles deep links."*

- **Binary Feature Reconstruction:**
  > *"Look at this native audio panning function in `libsound.so`. Recover the algorithm and rewrite it in clean C."*

- **Android APK Analysis:**
  > *"Inspect `app.apk` and show me all exported activities and network endpoints."*

- **WASM Analysis:**
  > *"Decode `module.wasm` into WAT and explain what functions are exported."*

- **Offline ELF Layout:**
  > *"Inspect the section layout and static security mitigations for `my_binary`."*

---

## Reference Guides

For deep-dive workflows, read the progressive disclosure guides:
- [native-and-artifacts.md](./references/native-and-artifacts.md) — Hopper, Ghidra, and IDA decompilation.
- [javascript-applications.md](./references/javascript-applications.md) — ASAR extraction and Electron IPC tracing.
- [android-applications.md](./references/android-applications.md) — JADX decompilation and APK manifests.
- [evidence-workflows.md](./references/evidence-workflows.md) — Evidence paging, bundle export, and audit trails.
- [connection-and-recovery.md](./references/connection-and-recovery.md) — Troubleshooting MCP timeouts and engine paths.
- [runtime-observation.md](./references/runtime-observation.md) — Passive browser and Electron runtime observation.

---

## ⚖License & Disclaimer

MIT License. REA provides tools for lawful reverse-engineering research, software interoperability, and feature reconstruction.
