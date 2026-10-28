#!/usr/bin/env python3
"""REA (Reverse Engineer Anything) Assistant & Target Routing Helper.

Zero-dependency tool to:
  1. Detect binary/artifact file types (ELF, Mach-O, PE, ASAR, APK, WASM, EVM, etc.)
  2. Output the exact recommended REA MCP tool call & invocation parameters
  3. Audit local environment readiness (Node >=22.19, npm, rea CLI, Ghidra, etc.)
  4. Generate ready-to-use MCP configuration blocks for Antigravity & other agents
"""

import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path


def detect_file_type(file_path: Path) -> dict:
    if not file_path.exists():
        return {"error": f"File does not exist: {file_path}"}

    if file_path.is_dir():
        # Check for extracted Electron/JS or package tree
        has_pkg = (file_path / "package.json").is_file()
        return {
            "type": "directory",
            "is_js_project": has_pkg,
            "target_format": "JavaScript/Electron Tree" if has_pkg else "Directory Tree",
            "recommended_tool": "analyze_javascript_application" if has_pkg else "open_binary",
            "description": "Extracted directory or application source/resource tree",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    size = file_path.stat().st_size
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        header = f.read(512)
        f.seek(0)
        while chunk := f.read(65536):
            sha256.update(chunk)

    ext = file_path.suffix.lower()
    magic = header[:4]

    # Magic byte routing
    # ELF: \x7fELF
    if magic == b"\x7fELF":
        return {
            "type": "binary",
            "format": "ELF (Executable and Linkable Format)",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "open_binary",
            "alternative_tool": "inspect_binary_layout",
            "description": "Linux/Unix Native Binary. Use 'open_binary' for native disassembly or 'inspect_binary_layout' for offline section/relocation diagnostics.",
            "suggested_args": {"path": str(file_path.resolve()), "provider_id": "ghidra"}
        }

    # Mach-O: 0xfeedface, 0xfeedfacf, 0xcafebabe, 0xbebafeca
    if magic in (b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe"):
        return {
            "type": "binary",
            "format": "Mach-O (macOS/iOS Binary)",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "open_binary",
            "description": "Apple Mach-O Native Binary. Use 'open_binary' with Hopper or Ghidra provider.",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    # PE / DOS: MZ
    if header[:2] == b"MZ":
        # Check if .NET managed assembly (look for CLI header in PE optional header)
        is_dotnet = False
        try:
            pe_offset = struct.unpack_from("<I", header, 0x3C)[0]
            if pe_offset + 0x18 + 0x60 < len(header):
                # Simple check for CLI metadata dictionary entry
                is_dotnet = True
        except Exception:
            pass

        format_name = ".NET Managed Assembly" if (is_dotnet or ext in (".dll", ".exe")) else "PE (Windows Executable/DLL)"
        tool = "inspect_managed_artifact" if is_dotnet else "open_binary"
        return {
            "type": "binary",
            "format": format_name,
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": tool,
            "alternative_tool": "inspect_pe_resources",
            "description": f"Windows PE binary. Use '{tool}' for inspection.",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    # WebAssembly: \x00asm
    if magic == b"\x00asm":
        return {
            "type": "binary",
            "format": "WebAssembly (WASM)",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "inspect_wasm_artifact",
            "description": "Compiled WebAssembly module. Decodes sections and WAT representations.",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    # ASAR archive (starts with size header followed by JSON)
    if ext == ".asar":
        return {
            "type": "archive",
            "format": "Electron ASAR Archive",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "analyze_javascript_application",
            "description": "Packaged Electron Application ASAR. Inspects modules, preload bridges, and IPC channels.",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    # ZIP / APK / IPA / JAR (PK\x03\x04)
    if magic == b"PK\x03\x04":
        if ext == ".apk":
            return {
                "type": "package",
                "format": "Android APK Package",
                "size_bytes": size,
                "sha256": sha256.hexdigest(),
                "recommended_tool": "inspect_android_package",
                "alternative_tool": "open_binary",
                "description": "Android Application Package. Decompiles manifest, dex classes, and methods via JADX.",
                "suggested_args": {"path": str(file_path.resolve())}
            }
        return {
            "type": "package",
            "format": f"ZIP Archive ({ext.upper()})",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "open_binary",
            "alternative_tool": "inspect_artifact",
            "description": "Archive/Package bundle. Inspects member inventories, digests, and artifacts.",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    # Network Captures (HAR, PCAP)
    if ext == ".har" or b'"log":' in header:
        return {
            "type": "capture",
            "format": "HAR (HTTP Archive Capture)",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "inspect_web_network_capture",
            "description": "Recorded web network capture. Traces requests, responses, and exposed payloads.",
            "suggested_args": {"path": str(file_path.resolve())}
        }

    # EVM Bytecode (raw hex 0x60... or binary)
    if (header.startswith(b"0x") and all(c in b"0123456789abcdefABCDEF\r\n " for c in header[2:min(len(header), 32)])) or ext == ".evm":
        return {
            "type": "bytecode",
            "format": "EVM Bytecode (Ethereum Virtual Machine)",
            "size_bytes": size,
            "sha256": sha256.hexdigest(),
            "recommended_tool": "inspect_evm_interface",
            "description": "Raw EVM bytecode. Dispatches function selectors, byte offsets, and candidate signatures.",
            "suggested_args": {"path": str(file_path.resolve()), "encoding": "hex"}
        }

    # Default fallback
    return {
        "type": "file",
        "format": f"Generic File ({ext or 'unknown'})",
        "size_bytes": size,
        "sha256": sha256.hexdigest(),
        "recommended_tool": "open_binary",
        "description": "Generic file. Bind with 'open_binary' to explore with active provider.",
        "suggested_args": {"path": str(file_path.resolve())}
    }


def check_readiness() -> dict:
    results = {}

    # Node.js
    node_path = shutil.which("node")
    if node_path:
        try:
            ver = subprocess.check_output([node_path, "-v"], text=True).strip()
            # Parse major version
            major = int(ver.lstrip("v").split(".")[0])
            compatible = major >= 22
            results["node"] = {
                "installed": True,
                "version": ver,
                "compatible": compatible,
                "requirement": ">= 22.19"
            }
        except Exception:
            results["node"] = {"installed": True, "compatible": False}
    else:
        results["node"] = {"installed": False, "compatible": False, "requirement": ">= 22.19"}

    # npm
    npm_path = shutil.which("npm")
    results["npm"] = {"installed": bool(npm_path), "path": npm_path}

    # rea CLI
    rea_path = shutil.which("rea")
    results["rea_cli"] = {"installed": bool(rea_path), "path": rea_path}

    # Ghidra
    ghidra_path = shutil.which("ghidra") or os.environ.get("GHIDRA_INSTALL_DIR")
    results["ghidra"] = {"installed": bool(ghidra_path), "path": str(ghidra_path) if ghidra_path else None}

    # Hopper
    hopper_path = shutil.which("hopper")
    results["hopper"] = {"installed": bool(hopper_path), "path": hopper_path}

    # IDA
    ida_path = shutil.which("ida64") or shutil.which("idat64")
    results["ida"] = {"installed": bool(ida_path), "path": ida_path}

    # JADX
    jadx_path = shutil.which("jadx")
    results["jadx"] = {"installed": bool(jadx_path), "path": jadx_path}

    # WABT
    wabt_path = shutil.which("wasm2wat") or os.environ.get("REA_WABT_BIN_DIRECTORY")
    results["wabt"] = {"installed": bool(wabt_path), "path": str(wabt_path) if wabt_path else None}

    return results


def get_mcp_config() -> dict:
    return {
        "mcpServers": {
            "rea": {
                "command": "npx",
                "args": ["-y", "rea-agents@latest", "mcp"]
            }
        }
    }


def main():
    parser = argparse.ArgumentParser(description="REA Target Router & Readiness Assistant")
    subparsers = parser.add_subparsers(dest="command")

    # route command
    route_parser = subparsers.add_parser("route", help="Detect artifact type and route to REA tool")
    route_parser.add_argument("target", help="Path to binary, package, or directory to route")
    route_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # readiness command
    readiness_parser = subparsers.add_parser("readiness", help="Check local environment readiness for REA")
    readiness_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # mcp-config command
    mcp_parser = subparsers.add_parser("mcp-config", help="Print MCP server configuration for Antigravity IDE")
    mcp_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.command == "route":
        target_path = Path(args.target)
        res = detect_file_type(target_path)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 68)
            print(f"Target:      {target_path}")
            print(f"Format:      {res.get('format', res.get('target_format', 'Unknown'))}")
            print(f"Tool Route:  {res.get('recommended_tool', 'open_binary')}")
            if "alternative_tool" in res:
                print(f"Alternative: {res['alternative_tool']}")
            print(f"Description: {res.get('description', '')}")
            if "sha256" in res:
                print(f"SHA-256:     {res['sha256']}")
            print("=" * 68)

    elif args.command == "readiness":
        res = check_readiness()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 68)
            print("         REA Environment Readiness Diagnostic")
            print("=" * 68)
            node_info = res["node"]
            status = "[OK] OK" if node_info["compatible"] else ("[WARN] Incompatible" if node_info["installed"] else "✖ Missing")
            print(f"Node.js:      {status:<14} (Version: {node_info.get('version', 'N/A')}, Req: {node_info['requirement']})")
            print(f"npm:          {'[OK] OK' if res['npm']['installed'] else '✖ Missing':<14} ({res['npm']['path'] or 'Not in PATH'})")
            print(f"rea CLI:      {'[OK] Detected' if res['rea_cli']['installed'] else '○ Optional (npx available)'}")
            print(f"Ghidra:       {'[OK] Detected' if res['ghidra']['installed'] else '○ Optional'}")
            print(f"JADX (APK):   {'[OK] Detected' if res['jadx']['installed'] else '○ Optional'}")
            print(f"WABT (WASM):  {'[OK] Detected' if res['wabt']['installed'] else '○ Optional'}")
            print("=" * 68)

    elif args.command == "mcp-config":
        cfg = get_mcp_config()
        if args.json:
            print(json.dumps(cfg, indent=2))
        else:
            print("Add this entry to your Antigravity MCP configuration:")
            print("File: ~/.gemini/config/mcp_config.json\n")
            print(json.dumps(cfg, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
