# src/sequin/cli.py
from __future__ import annotations

import glob
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List

import typer
from rich import print
from rich.progress import Progress

from .fasta_worker import process_fasta_file
from .motifs import build_pattern_to_motifs

# ──────────────────────────────────────────────────────────────────────────────────
# 1) Create a Typer “group” called app
# ──────────────────────────────────────────────────────────────────────────────────
app = typer.Typer(
    help="Sequin — succinct FM-index motif counter for FASTA files.",
    add_help_option=True,
    no_args_is_help=True,
)


# ──────────────────────────────────────────────────────────────────────────────────
# 2) Register “count” as a SUB-COMMAND of that group
# ──────────────────────────────────────────────────────────────────────────────────
@app.command(help="Count CG-anchored motifs in FASTA files.")
def count(
    patterns: str = typer.Option(
        ...,
        help="Comma-separated wildcard patterns, e.g. '****CG****,**CG**'",
    ),
    seq_dir: str = typer.Option(
        "seq", help="Directory containing .fasta files"
    ),
    workers: int = typer.Option(
        os.cpu_count(), help="Number of worker processes"
    ),
    out_dir: str = typer.Option(
        "sequin_results", help="Directory to write CSV results"
    ),
) -> None:
    """
    Parallel motif counter. Expands each wildcard‐pattern into concrete CG-anchored motifs,
    then processes all .fasta files under `seq_dir` in parallel and writes CSVs to `out_dir`.
    """
    pattern_list: List[str] = [
        p.strip() for p in patterns.split(",") if p.strip()
    ]
    pattern_to_motifs = build_pattern_to_motifs(pattern_list)

    fasta_files = glob.glob(str(Path(seq_dir) / "*.fasta"))
    if not fasta_files:
        print(f"[red]No FASTA files found in {seq_dir!s}")
        raise typer.Exit(code=1)

    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Processing FASTA files", total=len(fasta_files)
        )
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    process_fasta_file, f, pattern_to_motifs, out_dir=out_dir
                )
                for f in fasta_files
            ]
            for fut in futures:
                fut.add_done_callback(lambda _: progress.advance(task))
            for fut in futures:  # propagate exceptions
                fut.result()

    print(f"[green]Finished. Results in {out_dir}/")


# ──────────────────────────────────────────────────────────────────────────────────
# 3) If someone runs “python -m sequin”, dispatch into the group
# ──────────────────────────────────────────────────────────────────────────────────
def _main() -> None:  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    _main()
