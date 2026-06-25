"""Benchmark bioquik FM-index counting vs naive loop counter.

Compares correctness and speed across multiple FASTA files and pattern sets.
Three strategies are timed:

  naive      — str.count() per motif (non-overlapping, no index build)
  fm-count   — FMIndex.count() per motif (overlapping; O(m) per query)
  fm-locate  — FMIndex.locate() + non-overlap filter (exact match to naive)

The naive strategy mirrors the FastaSequenceCounter JS reference:
  https://github.com/Rajkanwars15/FastaSequenceCounter

Usage:
    python benchmarks/generate_fixtures.py   # one-time setup
    python -m benchmarks.run
    python -m benchmarks.run --patterns "*CG*,**CG**" --large
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from bioquik import FMIndex, build_pattern_to_motifs
from benchmarks.naive import count_all_motifs, read_fasta_sequence

_FIXTURES = Path(__file__).parent / "fixtures"


# ── counting helpers ──────────────────────────────────────────────────────────


def _fm_count_overlapping(fm: FMIndex, motifs: list[str]) -> dict[str, int]:
    """Fast path: backward-search only — O(|motif|) per query."""
    return {m: fm.count(m.encode()) for m in motifs}


def _fm_count_nonoverlap(fm: FMIndex, motifs: list[str]) -> dict[str, int]:
    """Exact match to str.count(): locate all positions, apply non-overlap filter."""
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


# ── per-file benchmark ────────────────────────────────────────────────────────


def _bench_file(fasta_path: Path, motifs: list[str]) -> dict:
    seq = read_fasta_sequence(fasta_path)

    # naive — one str.count() per motif, no index
    t0 = time.perf_counter()
    naive_counts = count_all_motifs(seq, motifs)
    naive_t = time.perf_counter() - t0

    # build the FM-index once (shared cost)
    t_build0 = time.perf_counter()
    fm = FMIndex(seq)
    build_t = time.perf_counter() - t_build0

    # fm-count — O(|motif|) per query, overlapping
    t0 = time.perf_counter()
    fmc_counts = _fm_count_overlapping(fm, motifs)
    fmc_t = time.perf_counter() - t0

    # fm-locate — exact non-overlapping (mirrors production fasta_worker)
    t0 = time.perf_counter()
    fml_counts = _fm_count_nonoverlap(fm, motifs)
    fml_t = time.perf_counter() - t0

    # correctness: fm-locate must match naive exactly
    mismatches = {m for m in motifs if naive_counts[m] != fml_counts[m]}
    # fm-count may differ for self-overlapping patterns (documented trade-off)
    overlap_diff = sum(
        abs(fmc_counts[m] - naive_counts[m]) for m in motifs
    )

    return {
        "file": fasta_path.name,
        "size_kb": fasta_path.stat().st_size / 1024,
        "n_motifs": len(motifs),
        "naive_t": naive_t,
        "build_t": build_t,
        "fmc_t": fmc_t,
        "fml_t": fml_t,
        # speedup of fm-count vs naive (index build amortised over all queries)
        "fmc_speedup": naive_t / (build_t + fmc_t),
        "mismatches": mismatches,
        "overlap_diff": overlap_diff,
        "total_hits": sum(fml_counts.values()),
    }


# ── reporting ─────────────────────────────────────────────────────────────────


def _print_table(rows: list[dict]) -> None:
    w = 105
    print()
    print(f"  {'File':<20} {'KB':>6} {'Motifs':>7}  {'naive(s)':>9}  {'build(s)':>9}  {'fm-count(s)':>12}  {'fm-locate(s)':>13}  {'Speedup':>8}  {'Hits':>7}  {'Match?':>7}")
    print("  " + "-" * w)
    for r in rows:
        ok = "✓" if not r["mismatches"] else f"✗ {len(r['mismatches'])}"
        print(
            f"  {r['file']:<20} {r['size_kb']:>6.1f} {r['n_motifs']:>7}"
            f"  {r['naive_t']:>9.4f}"
            f"  {r['build_t']:>9.4f}"
            f"  {r['fmc_t']:>12.4f}"
            f"  {r['fml_t']:>13.4f}"
            f"  {r['fmc_speedup']:>7.2f}x"
            f"  {r['total_hits']:>7}"
            f"  {ok:>7}"
        )
    print()
    print("  Speedup = naive / (build + fm-count).  Larger = FM-index faster.")
    print("  fm-locate is the exact non-overlapping match to naive (ground truth).")
    print("  fm-count may overcount self-overlapping patterns (rare in practice).")
    print()


# ── main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="bioquik vs naive motif counter")
    parser.add_argument(
        "--patterns",
        default="*CG*,**CG**",
        help="Comma-separated wildcard patterns (default: '*CG*,**CG**')",
    )
    parser.add_argument("--large", action="store_true", help="Include large.fasta")
    args = parser.parse_args()

    patterns = [p.strip() for p in args.patterns.split(",")]
    motifs = _flat_motifs(patterns)
    print(f"\nPatterns : {patterns}")
    print(f"Motifs   : {len(motifs)} unique concrete motifs expanded from patterns")

    fixture_names = ["tiny.fasta", "small.fasta", "medium.fasta"]
    if args.large:
        fixture_names.append("large.fasta")

    # also include real genomic files from experiments/ if present
    extra = [
        Path("experiments/data/C1orf105.fna"),
        Path("experiments/data/e1.fasta"),
    ]

    files: list[Path] = []
    for name in fixture_names:
        p = _FIXTURES / name
        if p.exists():
            files.append(p)
        else:
            print(f"  [skip] {name} — run: python benchmarks/generate_fixtures.py")

    for p in extra:
        if p.exists():
            files.append(p)

    if not files:
        print("No fixture files found. Run: python benchmarks/generate_fixtures.py")
        return

    rows = [_bench_file(f, motifs) for f in files]
    _print_table(rows)

    if any(r["mismatches"] for r in rows):
        print("CORRECTNESS FAILURES: fm-locate counts differ from naive.")
    else:
        print("Correctness: fm-locate matches naive for all files. ✓")

    total_overlap_diff = sum(r["overlap_diff"] for r in rows)
    if total_overlap_diff:
        print(f"Note: fm-count overcount due to overlapping patterns: {total_overlap_diff} across all files (expected for some CG patterns).")


if __name__ == "__main__":
    main()
