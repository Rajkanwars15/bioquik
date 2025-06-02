"""FM-index backed by *pydivsufsort* and *WaveletTree*."""
from __future__ import annotations

from typing import Dict, List

from pydivsufsort import divsufsort

from .wavelettree import WaveletTree

__all__ = ["FMIndex"]

class FMIndex:
    """Succinct FM-index supporting *count* and *locate* queries."""

    __slots__ = (
        "seq",
        "seq_b",
        "bwt",
        "alphabet",
        "C",
        "wt",
        "sa_sample_rate",
        "sa_samples",
        "_sa_len",
    )

    def __init__(self, seq: str, *, sa_sample_rate: int = 32):
        if not seq.endswith("$"):
            seq += "$"  # unique sentinel
        self.seq = seq
        self.seq_b = seq.encode("ascii")

        # 1) Suffix array.
        sa = divsufsort(self.seq_b)

        # 2) BWT.
        self.bwt = bytes(
            self.seq_b[s - 1] if s != 0 else ord("$") for s in sa
        )

        # 3) C-table.
        self.alphabet = sorted(set(self.bwt))
        totals: Dict[int, int] = {c: 0 for c in self.alphabet}
        for b in self.bwt:
            totals[b] += 1
        cumsum = 0
        self.C = {}
        for c in self.alphabet:
            self.C[c] = cumsum
            cumsum += totals[c]

        # 4) Occurrences via wavelet-tree.
        self.wt = WaveletTree(self.bwt, bytes(self.alphabet))

        # 5) SA sampling (for locate).
        self.sa_sample_rate = sa_sample_rate
        self.sa_samples: Dict[int, int] = {
            i: sa_i for i, sa_i in enumerate(sa) if i % sa_sample_rate == 0
        }
        self._sa_len = len(sa)

    # ------ Core queries ------
    def _backward_search(self, pattern: bytes):
        lo, hi = 0, self._sa_len
        for symbol in reversed(pattern):
            if symbol not in self.C:
                return 0, 0
            lo = self.C[symbol] + self.wt.rank(symbol, lo)
            hi = self.C[symbol] + self.wt.rank(symbol, hi)
            if lo >= hi:
                return 0, 0
        return lo, hi

    def count(self, pattern: bytes) -> int:
        """Return the number of occurrences of *pattern* in *seq*."""
        lo, hi = self._backward_search(pattern)
        return hi - lo

    def locate(self, pattern: bytes) -> List[int]:
        """Return all start positions of *pattern* (0-based)."""
        lo, hi = self._backward_search(pattern)
        return [self._resolve_sa(idx) for idx in range(lo, hi)]

    # ------ Internal helper ------
    def _resolve_sa(self, idx: int) -> int:
        steps = 0
        while idx not in self.sa_samples:
            symbol = self.bwt[idx]
            idx = self.C[symbol] + self.wt.rank(symbol, idx)
            steps += 1
        return (self.sa_samples[idx] + steps) % len(self.seq)