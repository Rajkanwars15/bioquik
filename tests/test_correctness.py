"""Cross-validation: bioquik FM-index counts must match naive str.count().

These tests act as ground-truth correctness checks by comparing against the
naive loop counter (equivalent to the FastaSequenceCounter JS reference at
https://github.com/Rajkanwars15/FastaSequenceCounter).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from benchmarks.naive import count_all_motifs, read_fasta_sequence
from benchmarks.generate_fixtures import generate
from bioquik import FMIndex
from bioquik.motifs import build_pattern_to_motifs

_FIXTURES = Path(__file__).parent.parent / "benchmarks" / "fixtures"


def _fm_count_nonoverlap(fm: FMIndex, motifs: list[str]) -> dict[str, int]:
    """Non-overlapping FM-index count (matches production fasta_worker logic)."""
    result: dict[str, int] = {}
    for m in motifs:
        starts = sorted(fm.locate(m.encode()))
        ml = len(m)
        last, count = -ml, 0
        for s in starts:
            if s >= last + ml:
                count += 1
                last = s
        result[m] = count
    return result


def _flat_motifs(patterns: list[str]) -> list[str]:
    mapping = build_pattern_to_motifs(patterns)
    seen: set[str] = set()
    result: list[str] = []
    for motifs in mapping.values():
        for m in motifs:
            if m not in seen:
                seen.add(m)
                result.append(m)
    return result


@pytest.fixture(scope="module")
def tiny_fasta(tmp_path_factory) -> Path:
    """Return path to tiny.fasta, generating it if needed."""
    if (_FIXTURES / "tiny.fasta").exists():
        return _FIXTURES / "tiny.fasta"
    out = tmp_path_factory.mktemp("fixtures")
    generate_to = out / "tiny.fasta"
    # inline tiny generation so test has no external dep
    import random
    rng = random.Random(42)
    bases = "ACGT"
    lines = []
    for i in range(5):
        seq = "".join(rng.choices(bases, k=200))
        lines.append(f">seq{i}")
        lines.append(seq)
    generate_to.write_text("\n".join(lines) + "\n")
    return generate_to


# ── parametrised correctness tests ───────────────────────────────────────────

FIXTURE_FILES = [
    pytest.param("tiny.fasta", id="tiny"),
    pytest.param("small.fasta", id="small"),
]

PATTERN_SETS = [
    pytest.param(["*CG*"], id="1-wildcard"),
    pytest.param(["**CG**"], id="2-wildcard"),
    pytest.param(["*CG*", "**CG**"], id="mixed"),
]


@pytest.mark.parametrize("fixture_name", FIXTURE_FILES)
@pytest.mark.parametrize("patterns", PATTERN_SETS)
def test_fm_index_matches_naive(fixture_name, patterns):
    """FM-index non-overlapping count must equal naive str.count() for all motifs."""
    fasta_path = _FIXTURES / fixture_name
    if not fasta_path.exists():
        generate()  # create fixtures if missing

    motifs = _flat_motifs(patterns)
    seq = read_fasta_sequence(fasta_path)

    naive = count_all_motifs(seq, motifs)
    fm = FMIndex(seq)
    fm_result = _fm_count_nonoverlap(fm, motifs)

    mismatches = {m: (naive[m], fm_result[m]) for m in motifs if naive[m] != fm_result[m]}
    assert not mismatches, f"Count mismatches for {len(mismatches)} motifs: {list(mismatches.items())[:5]}"


def test_known_sequence_counts():
    """Spot-check FM-index counts on a hand-verified sequence."""
    # "ACGACGACG" contains ACG at positions 0, 3, 6 — 3 non-overlapping
    seq = "ACGACGACG"
    motif = "ACG"
    fm = FMIndex(seq)
    starts = sorted(fm.locate(motif.encode()))
    ml = len(motif)
    last, count = -ml, 0
    for s in starts:
        if s >= last + ml:
            count += 1
            last = s
    assert count == 3
    assert seq.count(motif) == 3


def test_counts_consistent_with_cli(tmp_path):
    """End-to-end: process_fasta_file counts match naive for a known file."""
    from bioquik import process_fasta_file, build_pattern_to_motifs
    import pandas as pd

    fasta = tmp_path / "test.fasta"
    seq = "ACGACGTCGATCG"
    fasta.write_text(f">test\n{seq}\n")

    patterns = ["*CG*"]
    mapping = build_pattern_to_motifs(patterns)
    csv_path = process_fasta_file(fasta, mapping, out_dir=tmp_path)
    df = pd.read_csv(csv_path)

    # Build flat motif list and compare
    all_motifs = [m for ms in mapping.values() for m in ms]
    naive = {m: seq.count(m) for m in all_motifs}

    for _, row in df.iterrows():
        motif = row["Motif"]
        assert row["Count"] == naive[motif], (
            f"Mismatch for {motif}: got {row['Count']}, expected {naive[motif]}"
        )
