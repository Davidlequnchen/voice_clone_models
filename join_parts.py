"""Join the model files that were cut into parts to pass through git, and check each against its SHA-256.

Usage (from this folder, antideepfake/models/voice_clone/), after cloning or pulling this repository:
    python join_parts.py
It finds every <file>.part000 under this folder, writes <file> next to its parts and checks its SHA-256 (from
<file>.sha256). Files that are already there with the right checksum are skipped, so it can simply be re-run.
Needs only Python 3.11+ (no packages). The parts can be deleted afterwards to save 10 GB, but then `git pull` would
bring them back; keep them if you pull this repository again.
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.file_digest(fh, "sha256").hexdigest()


def main():
    sys.stdout.reconfigure(line_buffering=True)
    firsts = sorted(ROOT.rglob("*.part000"))
    if not firsts:
        sys.exit("ERROR: no split files (*.part000) in this folder; clone or pull the repository first")
    print(f"Found {len(firsts)} split file(s)")
    failed = 0
    for first in firsts:
        target = first.with_suffix("")  # llm.pt.part000 -> llm.pt
        name = target.relative_to(ROOT)
        parts = sorted(target.parent.glob(target.name + ".part[0-9][0-9][0-9]"))
        expected = (target.parent / f"{target.name}.sha256").read_text().split()[0]
        if target.exists() and sha256(target) == expected:  # 1. joined before
            print(f"  {name}: already joined and checked")
            continue
        if [p.suffix for p in parts] != [f".part{i:03d}" for i in range(len(parts))]:  # 2. no gaps
            print(f"  ERROR {name}: parts are missing (found {', '.join(p.suffix[1:] for p in parts)})")
            failed += 1
            continue
        print(f"  {name}: joining {len(parts)} parts ...")  # 3. join, check, then rename
        joining = target.parent / f"{target.name}.joining"
        with open(joining, "wb") as out:
            for p in parts:
                out.write(p.read_bytes())
        if sha256(joining) != expected:
            joining.unlink()
            print(f"  ERROR {name}: SHA-256 does not match; run git pull again, then this script")
            failed += 1
            continue
        joining.replace(target)
        print(f"  {name}: OK, {target.stat().st_size / 1e6:,.0f} MB, SHA-256 checked")
    if failed:
        sys.exit(f"ERROR: {failed} file(s) could not be joined")
    print("Done. The models are ready: python scripts/voice_clone/generate.py (from the antideepfake/ folder)")


if __name__ == "__main__":
    main()
