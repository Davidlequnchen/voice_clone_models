"""Cut the large model files of this repository into 90 MiB parts that git can take (GitHub refuses files over
100 MB). Run by whoever updates the weights, before committing; the other machine only runs join_parts.py.

Usage (from this folder, antideepfake/models/voice_clone/):
    python split_parts.py
FILES lists the files to cut, PART_MIB the size of a part. Next to each file it writes <file>.part000, .part001, ...
and <file>.sha256 (SHA-256 of the whole file). A file whose parts already match its SHA-256 is skipped.
Then commit the parts and the .sha256 files (never the whole files: .gitignore keeps them out), and push in batches
of at most 15 parts (about 1.4 GB; GitHub refuses a push over 2 GB).
"""
import hashlib
import sys
from pathlib import Path

# ======================================================================
# Settings (paths are relative to this folder)
# ======================================================================
FILES = [  # every file over 90 MiB; smaller files are committed as they are
    "cosyvoice2_0.5b/llm.pt",
    "cosyvoice2_0.5b/speech_tokenizer_v2.onnx",
    "cosyvoice2_0.5b/flow.pt",
    "cosyvoice3_0.5b/llm.pt",
    "cosyvoice3_0.5b/flow.pt",
    "cosyvoice3_0.5b/speech_tokenizer_v3.onnx",
    "chatterbox/t3_cfg.safetensors",
    "chatterbox/s3gen.safetensors",
]
PART_MIB = 90  # size of each part, in MiB

ROOT = Path(__file__).resolve().parent


def sha256(paths):
    """SHA-256 of the files in `paths`, read one after the other as if they were one file."""
    digest = hashlib.sha256()
    for path in paths:
        with open(path, "rb") as fh:
            while chunk := fh.read(1 << 24):
                digest.update(chunk)
    return digest.hexdigest()


def main():
    sys.stdout.reconfigure(line_buffering=True)
    size = PART_MIB * 2**20
    total_parts = 0
    for name in FILES:
        path = ROOT / name
        total = path.stat().st_size
        names = [path.with_name(f"{path.name}.part{i:03d}") for i in range(-(-total // size))]
        sidecar = path.with_name(path.name + ".sha256")
        old = sorted(path.parent.glob(path.name + ".part[0-9][0-9][0-9]"))
        digest = sha256([path])
        if old == names and sidecar.exists() and sidecar.read_text().split()[0] == digest and sha256(old) == digest:
            print(f"  {name}: already split ({len(names)} parts, SHA-256 checked)")
        else:
            for p in old:
                p.unlink()
            with open(path, "rb") as fh:
                for part in names:
                    part.write_bytes(fh.read(size))
            sidecar.write_text(f"{digest}  {path.name}\n")
            print(f"  {name}: {total / 1e6:,.1f} MB -> {len(names)} parts and {sidecar.name}")
        total_parts += len(names)
    print(f"Done: {total_parts} parts. Commit them in batches of at most 15 parts per push.")


if __name__ == "__main__":
    main()
