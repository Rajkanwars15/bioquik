"""Succinct binary-recursive wavelet tree with rank-support."""

from __future__ import annotations

from typing import List

__all__ = ["WaveletTree"]


class WaveletTree:
    """Wavelet tree over a *bytes* sequence providing **rank1** queries.

    The implementation stores a bitvector at each internal node and samples
    prefix ranks every *sample_rate* bits (default = 32) for O(1) rank queries.
    Memory usage ≈ *n log σ* bits.
    """

    __slots__ = (
        "length",
        "alphabet",
        "bitvec",
        "sample_rate",
        "prefix_ranks",
        "left",
        "right",
    )

    def __init__(self, data: bytes, alphabet: bytes, *, sample_rate: int = 32):
        self.length = len(data)
        self.alphabet = alphabet
        self.sample_rate = sample_rate

        if len(alphabet) == 1:
            # Leaf — no bitvector needed.
            self.bitvec = None
            self.prefix_ranks = None
            self.left = self.right = None
            return

        mid = len(alphabet) // 2
        left_alpha, right_alpha = alphabet[:mid], alphabet[mid:]

        # Build bitvector and partition children sequences.
        left_bytes: List[int] = []
        right_bytes: List[int] = []
        bits: List[int] = []
        cur, cnt = 0, 0
        for b in data:
            go_left = b in left_alpha
            # 0 → left, 1 → right
            cur = (cur << 1) | int(not go_left)
            if go_left:
                left_bytes.append(b)
            else:
                right_bytes.append(b)
            cnt += 1
            if cnt == 8:
                bits.append(cur)
                cur, cnt = 0, 0
        if cnt:
            bits.append(cur << (8 - cnt))

        self.bitvec = bytes(bits)

        # Precompute rank1 samples.
        self.prefix_ranks = [0]
        total = 0
        bit_index = 0
        for byte in self.bitvec:
            for i in range(8):
                if bit_index % self.sample_rate == 0:
                    self.prefix_ranks.append(total)
                total += (byte >> (7 - i)) & 1
                bit_index += 1
        self.prefix_ranks.append(total)  # sentinel

        # Recurse.
        self.left = (
            WaveletTree(bytes(left_bytes), left_alpha, sample_rate=sample_rate)
            if left_alpha
            else None
        )
        self.right = (
            WaveletTree(bytes(right_bytes), right_alpha, sample_rate=sample_rate)
            if right_alpha
            else None
        )

    # ------ Public API ------
    def rank(self, symbol: int, i: int) -> int:
        """Return *#(symbol) in [0, i)*."""
        if len(self.alphabet) == 1 or i <= 0:
            return min(i, self.length)

        mid = len(self.alphabet) // 2
        go_left = symbol in self.alphabet[:mid]
        ones = self._rank1(i)
        zeros = i - ones
        return (
            self.left.rank(symbol, zeros) if go_left else self.right.rank(symbol, ones)
        )

    # ------ Internal helpers ------
    def _rank1(self, i: int) -> int:
        if i <= 0:
            return 0
        block = i // self.sample_rate
        rank = self.prefix_ranks[block]
        start_bit = block * self.sample_rate
        bits_to_scan = i - start_bit
        byte_idx, bit_off = divmod(start_bit, 8)
        scanned = 0
        while scanned < bits_to_scan:
            byte = self.bitvec[byte_idx]
            for bit in range(bit_off, 8):
                if scanned == bits_to_scan:
                    break
                rank += (byte >> (7 - bit)) & 1
                scanned += 1
            byte_idx += 1
            bit_off = 0
        return rank
