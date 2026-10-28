#!/usr/bin/env python3
"""Distribution Packager for Google Antigravity Skills Suite.

Builds clean, ready-to-share release archives and plugin bundles:
  - dist/antigravity-skills.zip (Universal ZIP archive)
  - dist/antigravity-skills.tar.gz (Gzip tarball)
  - dist/antigravity-skills-pack/ (Direct Antigravity Plugin structure)
  - dist/checksums.sha256 (Verification checksums)
"""

import hashlib
import json
import os
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    "node_modules",
    ".court",
    ".impeccable",
    "dist",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store",
    ".log",
}

SKILLS = [
    "court",
    "secure-audit",
    "anti-vcode",
    "impeccable",
    "steal",
    "taste",
    "designs",
    "ui-ux-max",
    "threeui",
    "rev-engineer",
    "logo-design",
    "writing-readme",
    "arena",
    "ponytail",
    "last30days",
    "scrapling",
    "humanizer",
    "diagram-design",
    "socratic",
    "rigor",
    "sanzo-wada-colors",
]

CORE_FILES = [
    "README.md",
    "SHARING.md",
    "LICENSE",
    ".gitignore",
    "install.sh",
    "install.py",
    "test_all.py",
    "package.py",
]


def should_include(rel_path: Path) -> bool:
    parts = set(rel_path.parts)
    if parts & EXCLUDE_DIRS:
        return False
    if rel_path.suffix in EXCLUDE_EXTS:
        return False
    if rel_path.name.startswith(".#"):
        return False
    return True


def gather_files():
    files = []
    # Core files
    for cf in CORE_FILES:
        p = ROOT / cf
        if p.is_file():
            files.append(p)

    # Skill directories
    for skill in SKILLS:
        skill_dir = ROOT / skill
        if skill_dir.is_dir():
            for p in skill_dir.rglob("*"):
                if p.is_file():
                    rel = p.relative_to(ROOT)
                    if should_include(rel):
                        files.append(p)
    return files


def make_zip(files, out_path: Path):
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            arcname = f.relative_to(ROOT)
            zf.write(f, arcname=arcname)


def make_tar(files, out_path: Path):
    with tarfile.open(out_path, "w:gz") as tf:
        for f in files:
            arcname = f.relative_to(ROOT)
            tf.add(f, arcname=str(arcname))


def make_plugin_bundle(files, plugin_dir: Path):
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
    plugin_dir.mkdir(parents=True)

    # Manifest for Antigravity Plugin
    manifest = {
        "name": "antigravity-skills-pack",
        "description": "Curated suite of 9 modular Antigravity AI coding skills",
        "version": "1.0.0",
        "author": "Antigravity Power User",
        "skills": SKILLS
    }
    with open(plugin_dir / "plugin.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # Copy skills into plugin/skills/
    skills_dest = plugin_dir / "skills"
    skills_dest.mkdir(parents=True)
    for skill in SKILLS:
        src = ROOT / skill
        dest = skills_dest / skill
        if src.is_dir():
            shutil.copytree(
                src, dest,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "node_modules")
            )

    # Copy README and license
    for item in ("README.md", "SHARING.md", "LICENSE"):
        src = ROOT / item
        if src.is_file():
            shutil.copy2(src, plugin_dir / item)


def compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    print("=" * 72)
    print("       Antigravity Skills Suite - Distribution Packager")
    print("=" * 72)

    DIST.mkdir(parents=True, exist_ok=True)
    files = gather_files()
    print(f"\nDiscovered {len(files)} files across {len(SKILLS)} skills.")

    zip_file = DIST / "antigravity-skills.zip"
    tar_file = DIST / "antigravity-skills.tar.gz"
    plugin_folder = DIST / "antigravity-skills-pack"

    print("\nBuilding universal ZIP archive...")
    make_zip(files, zip_file)
    zip_size = zip_file.stat().st_size / (1024 * 1024)
    print(f"  Created {zip_file.name} ({zip_size:.2f} MB)")

    print("\nBuilding Gzip tarball archive...")
    make_tar(files, tar_file)
    tar_size = tar_file.stat().st_size / (1024 * 1024)
    print(f"  Created {tar_file.name} ({tar_size:.2f} MB)")

    print("\nBuilding Antigravity Plugin package...")
    make_plugin_bundle(files, plugin_folder)
    print(f"  Created {plugin_folder.name}/ (Ready for ~/.gemini/config/plugins/)")

    # Checksums
    checksums = [
        f"{compute_sha256(zip_file)}  {zip_file.name}",
        f"{compute_sha256(tar_file)}  {tar_file.name}",
    ]
    checksum_file = DIST / "checksums.sha256"
    with open(checksum_file, "w", encoding="utf-8") as f:
        f.write("\n".join(checksums) + "\n")
    print(f"\n  Wrote SHA-256 checksums to {checksum_file.name}")

    print("\n" + "=" * 72)
    print("                      PACKAGE SUMMARY")
    print("=" * 72)
    print(f"Directory: {DIST}")
    print(f"  • {zip_file.name:<28} ({zip_size:.2f} MB) -> Share via Discord/Slack/Email")
    print(f"  • {tar_file.name:<28} ({tar_size:.2f} MB) -> Standard Unix Tarball")
    print(f"  • {plugin_folder.name:<28} (Folder)     -> Drop into ~/.gemini/config/plugins/")
    print(f"  • {checksum_file.name:<28} (Text)       -> Verification Hashes")
    print("=" * 72)
    print("\nTo share with friends:")
    print("  1. Send them 'dist/antigravity-skills.zip'")
    print("  2. Or publish this repository to GitHub so friends can clone or curl!")
    print()


if __name__ == "__main__":
    main()
