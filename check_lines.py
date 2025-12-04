#!/usr/bin/env python3
"""Scan markdown files and show line counts to find empty/small files."""

import os
from pathlib import Path

def scan_md_files(root_dir: str) -> list[tuple[int, str]]:
    """Scan all .md files and return (line_count, filepath) tuples."""
    results = []
    root = Path(root_dir)

    for md_file in root.rglob("*.md"):
        # Skip Archive folder
        if "Archive" in md_file.parts:
            continue

        try:
            line_count = len(md_file.read_text().splitlines())
            rel_path = md_file.relative_to(root)
            results.append((line_count, str(rel_path)))
        except Exception as e:
            results.append((-1, f"{md_file} (ERROR: {e})"))

    return sorted(results)  # Sort by line count ascending


def main():
    refs_dir = "vercel/skills/vercel-ai-sdk/references"

    print(f"Scanning: {refs_dir}\n")
    print(f"{'Lines':>6}  File")
    print("-" * 60)

    results = scan_md_files(refs_dir)

    empty_or_small = []
    for lines, filepath in results:
        marker = ""
        if lines == 0:
            marker = " ⚠️  EMPTY"
            empty_or_small.append((lines, filepath))
        elif lines < 10:
            marker = " ⚠️  VERY SMALL"
            empty_or_small.append((lines, filepath))

        print(f"{lines:>6}  {filepath}{marker}")

    print("-" * 60)
    print(f"Total: {len(results)} files\n")

    if empty_or_small:
        print("⚠️  Files that may need attention:")
        for lines, filepath in empty_or_small:
            print(f"  - {filepath} ({lines} lines)")
    else:
        print("✅ All files have content (10+ lines)")


if __name__ == "__main__":
    main()
