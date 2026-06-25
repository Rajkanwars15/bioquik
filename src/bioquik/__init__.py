"""Top-level package for **bioquik**."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bioquik")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .fasta_worker import process_fasta_file
from .fmindex import FMIndex
from .motifs import build_pattern_to_motifs, generate_motifs
from .processor import run_count
from .wavelettree import WaveletTree

__all__ = [
    "WaveletTree",
    "FMIndex",
    "build_pattern_to_motifs",
    "generate_motifs",
    "process_fasta_file",
    "run_count",
]
