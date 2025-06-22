"""Per-file FASTA motif counter (intended for parallel use via **concurrent.futures**)."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from .fmindex import FMIndex
from .motifs import build_pattern_to_motifs

__all__ = ["process_fasta_file"]

def _count_in_fm(fm: FMIndex, motif: bytes, *, allow_overlap: bool = False) -> int:
    if allow_overlap:
        return fm.count(motif)
    starts = sorted(fm.locate(motif))
    m = len(motif)
    last, non_overlap = -m, 0
    for s in starts:
        if s >= last + m:
            non_overlap += 1
            last = s
    return non_overlap

def process_fasta_file(
    fasta_path: str | os.PathLike,
    pattern_to_motifs: dict[str, list[str]],
    *,
    out_dir: str | os.PathLike = "bioquik_results",
) -> str:
    """Count motifs in *fasta_path* and save CSV → *out_dir*.

    Returns the output CSV filepath.
    """
    fasta_path = Path(fasta_path)
    seq = "".join(
        line.strip().upper() for line in fasta_path.read_text().splitlines() if not line.startswith(">")
    )

    tqdm.write(f"  Building FM-index for {fasta_path.name} …")
    fm = FMIndex(seq)

    results: list[dict[str, str | int]] = []
    for pattern_key, motif_list in pattern_to_motifs.items():
        for motif in motif_list:
            c = _count_in_fm(fm, motif.encode(), allow_overlap=False)
            if c:
                results.append({"Pattern": pattern_key, "Motif": motif, "Count": c})

    out_path = Path(out_dir) / f"{fasta_path.stem}_motif_counts.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(results,columns = ["Pattern", "Motif", "Count"],).to_csv(out_path, index=False)
    tqdm.write(f"→ {fasta_path} → {out_path.name}")
    return str(out_path)