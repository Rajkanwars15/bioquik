from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List
from rich.progress import Progress

from .fasta_worker import process_fasta_file
from .motifs import build_pattern_to_motifs


def run_count(
    pattern_list: List[str],
    seq_dir: Path,
    out_dir: Path,
    workers: int,
) -> None:
    """
    Expand patterns, then process every .fasta in parallel.
    """
    mapping = build_pattern_to_motifs(pattern_list)
    fasta_files = list(seq_dir.glob("*.fasta"))

    with Progress() as progress:
        task = progress.add_task("[cyan]Counting motifs", total=len(fasta_files))
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futures = [
                ex.submit(process_fasta_file, f, mapping, out_dir=out_dir)
                for f in fasta_files
            ]
            for fut in futures:
                fut.add_done_callback(lambda _: progress.advance(task))
            # propagate exceptions
            for fut in futures:
                fut.result()
