"""Pattern → motif expansion utilities."""
from __future__ import annotations

from itertools import product
from typing import Dict, List

from tqdm import tqdm

__all__ = ["generate_motifs", "build_pattern_to_motifs"]

_BASES = ("G", "A", "T", "C")

def generate_motifs(patterns: list[str]):
    """Expand wildcard * patterns into concrete motifs (deduplicated, sorted)."""
    unique: set[str] = set()
    for pattern in tqdm(patterns, desc="Generating motifs"):
        pre, _, post = pattern.partition("CG")
        pre_cg, post_cg = pre.count("*"), post.count("*")
        for pre_seq in product(_BASES, repeat=pre_cg):
            for post_seq in product(_BASES, repeat=post_cg):
                unique.add(f"{''.join(pre_seq)}CG{''.join(post_seq)}")
    return sorted(unique)

def build_pattern_to_motifs(patterns: list[str]) -> Dict[str, List[str]]:
    """Return mapping *pattern→[motifs]* using N as wildcard stand-in."""
    mapping: Dict[str, List[str]] = {}
    for pattern in tqdm(patterns, desc="Building pattern→motifs map"):
        key = pattern.replace("*", "N")
        pre, _, post = pattern.partition("CG")
        pre_cg, post_cg = pre.count("*"), post.count("*")
        pre_vars = ("".join(p) for p in product(_BASES, repeat=pre_cg))
        post_vars = ("".join(p) for p in product(_BASES, repeat=post_cg))
        mapping[key] = [f"{pre}CG{post}" for pre in pre_vars for post in post_vars]
    return mapping