#!/usr/bin/env python3
"""
Check for empty files and identical files in the same folder.
"""

import sys
import hashlib
from pathlib import Path
from collections import defaultdict


def get_file_hash(filepath: Path) -> str:
    """Get MD5 hash of file content."""
    return hashlib.md5(filepath.read_bytes()).hexdigest()


def check_directory(base_path: Path):
    """Check for empty and identical files."""

    empty_files = []

    # Group files by parent directory
    files_by_dir = defaultdict(list)

    for md_file in base_path.rglob("*.md"):
        size = md_file.stat().st_size

        if size == 0:
            empty_files.append(md_file)
        else:
            files_by_dir[md_file.parent].append(md_file)

    # Check for identical files in same folder
    identical_groups = []

    for folder, files in files_by_dir.items():
        if len(files) < 2:
            continue

        # Group by hash
        hash_to_files = defaultdict(list)
        for f in files:
            h = get_file_hash(f)
            hash_to_files[h].append(f)

        # Find duplicates
        for h, file_list in hash_to_files.items():
            if len(file_list) > 1:
                identical_groups.append((folder, file_list))

    # Report
    print("=" * 60)
    print("FILE CHECK REPORT")
    print("=" * 60)

    print(f"\n## Empty Files ({len(empty_files)})")
    if empty_files:
        for f in empty_files:
            print(f"  - {f.relative_to(base_path)}")
    else:
        print("  None found")

    print(f"\n## Identical Files in Same Folder ({len(identical_groups)} groups)")
    if identical_groups:
        for folder, files in identical_groups:
            print(f"\n  Folder: {folder.relative_to(base_path)}")
            for f in files:
                print(f"    - {f.name}")
    else:
        print("  None found")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path(".")

    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)

    check_directory(path)
