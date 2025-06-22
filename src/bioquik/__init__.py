"""Top-level package for **bioquik**."""

__version__ = "0.1.0"

from .wavelettree import WaveletTree  # noqa: E402
from .fmindex import FMIndex        # noqa: E402
from .motifs import build_pattern_to_motifs, generate_motifs  # noqa: E402
from .fasta_worker import process_fasta_file  # noqa: E402

__all__ = [
    "WaveletTree",
    "FMIndex",
    "build_pattern_to_motifs",
    "generate_motifs",
    "process_fasta_file",
]