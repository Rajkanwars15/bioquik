# Benchmarks

Bioquik ships a benchmark suite that compares the FM-index counting strategy against a naive loop counter equivalent to the [FastaSequenceCounter](https://github.com/Rajkanwars15/FastaSequenceCounter) JavaScript reference.

---

## Setup

Generate fixture FASTA files (one-time):

```bash
python benchmarks/generate_fixtures.py          # tiny (1 KB), small (10 KB), medium (100 KB)
python benchmarks/generate_fixtures.py --large  # also generate a 5 MB file
```

Real genomic files in `experiments/data/` are picked up automatically if present.

---

## Running

```bash
python -m benchmarks.run
python -m benchmarks.run --patterns "*CG*,**CG**"
python -m benchmarks.run --large
```

Sample output:

```
Patterns : ['*CG*', '**CG**']
Motifs   : 272 unique concrete motifs

  File                   KB  Motifs   naive(s)   build(s)  fm-count(s)  fm-locate(s)  Speedup   Hits  Match?
  -----------------------------------------------------------------------------------------------------------
  tiny.fasta            1.0     272     0.0011     0.0038       0.0139        0.0378    0.06x    129       ✓
  small.fasta           9.9     272     0.0106     0.0329       0.0171        0.2348    0.21x   1333       ✓
  medium.fasta         99.1     272     0.0827     0.3295       0.0158        2.3472    0.24x  12603       ✓
  C1orf105.fna         95.5     272     0.0746     0.3160       0.0157        0.2724    0.22x   1422       ✓
```

---

## Strategies compared

| Strategy | Description |
|---|---|
| `naive` | `str.count()` per motif — no index, equivalent to the JS reference |
| `fm-count` | `FMIndex.count()` per motif — O(pattern length) per query after build; counts overlapping occurrences |
| `fm-locate` | `FMIndex.locate()` + non-overlap filter — exact non-overlapping match to `naive` |

**Speedup** is `naive_time / (build_time + fm-count_time)`. Values > 1× mean the FM-index is faster overall.

---

## Understanding the results

The naive `str.count()` is backed by a C implementation and is very fast for small-to-medium files. The FM-index build cost (constructing the suffix array and wavelet tree in Python) currently dominates for files under ~10 MB.

The FM-index advantage becomes significant when:
- Querying very long patterns against large sequences
- Counting hundreds or thousands of patterns without rebuilding the index per pattern

`fm-count` and `naive` may disagree by a small margin when a motif is self-overlapping (e.g. `CGCG` in a long CG-repeat). `fm-locate` corrects for this and matches `naive` exactly.

---

## Correctness tests

The cross-validation tests in `tests/test_correctness.py` assert that `fm-locate` counts equal `naive` counts across multiple fixture files and pattern sets:

```bash
pytest tests/test_correctness.py -v
```
