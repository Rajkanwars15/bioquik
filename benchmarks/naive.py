"""Naive motif counter — baseline equivalent to the FastaSequenceCounter JS reference.

The reference (https://github.com/Rajkanwars15/FastaSequenceCounter) strips FASTA
headers, joins lines, then does `sequence.match(new RegExp(motif, 'g'))` per motif.
This is the Python equivalent: exact non-overlapping string search per motif.
"""

from __future__ import annotations

from pathlib import Path


def read_fasta_sequence(fasta_path: str | Path) -> str:
    """Read a FASTA file and return the raw sequence (headers stripped, uppercased)."""
    return "".join(
        line.strip().upper()
        for line in Path(fasta_path).read_text().splitlines()
        if not line.startswith(">")
    )


def count_motif(sequence: str, motif: str) -> int:
    """Count non-overlapping occurrences of *motif* in *sequence* (exact match)."""
    return sequence.count(motif)


def count_all_motifs(sequence: str, motifs: list[str]) -> dict[str, int]:
    """Return {motif: count} for every motif. Zero counts included."""
    return {m: count_motif(sequence, m) for m in motifs}


def count_file(fasta_path: str | Path, motifs: list[str]) -> dict[str, int]:
    """Read FASTA file then count all motifs — one pass per motif (naive)."""
    seq = read_fasta_sequence(fasta_path)
    return count_all_motifs(seq, motifs)
