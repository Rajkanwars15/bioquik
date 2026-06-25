"""Generate synthetic FASTA fixture files for benchmarking.

Usage:
    python benchmarks/generate_fixtures.py            # small + medium
    python benchmarks/generate_fixtures.py --large    # also generate 5MB file
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

_BASES = "ACGT"
_FIXTURES = Path(__file__).parent / "fixtures"


def _make_sequence(n_bases: int, seed: int = 42) -> str:
    rng = random.Random(seed)
    return "".join(rng.choices(_BASES, k=n_bases))


def _write_fasta(path: Path, sequences: list[tuple[str, str]]) -> None:
    """Write (header, seq) pairs to FASTA."""
    lines = []
    for header, seq in sequences:
        lines.append(f">{header}")
        for i in range(0, len(seq), 70):
            lines.append(seq[i : i + 70])
    path.write_text("\n".join(lines) + "\n")
    print(f"  wrote {path.name}  ({path.stat().st_size / 1024:.1f} KB)")


def generate(include_large: bool = False) -> None:
    _FIXTURES.mkdir(parents=True, exist_ok=True)

    sizes = {
        "tiny.fasta": [(f"seq{i}", _make_sequence(200, seed=i)) for i in range(5)],
        "small.fasta": [(f"seq{i}", _make_sequence(2_000, seed=i)) for i in range(5)],
        "medium.fasta": [(f"seq{i}", _make_sequence(20_000, seed=i)) for i in range(5)],
    }
    if include_large:
        sizes["large.fasta"] = [
            (f"seq{i}", _make_sequence(200_000, seed=i)) for i in range(5)
        ]

    print("Generating fixtures:")
    for name, seqs in sizes.items():
        _write_fasta(_FIXTURES / name, seqs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--large", action="store_true", help="Also generate 5 MB file")
    args = parser.parse_args()
    generate(include_large=args.large)
