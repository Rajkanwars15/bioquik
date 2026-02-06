# Architecture Guide

This document provides a comprehensive overview of Bioquik's internal architecture, design decisions, and extension points.

## System Overview

Bioquik is built around a **pipeline architecture** that processes DNA sequences through several stages:

1. **Input Validation** → 2. **Pattern Expansion** → 3. **Parallel Processing** → 4. **Report Generation**

Each stage is implemented as a separate module with clear responsibilities.

## Core Components

### 1. FM-Index: The Heart of Pattern Matching

The **FM-index** (Full-text index in Minute space) is the core data structure that enables efficient pattern matching. It's a compressed variant of the suffix array that supports:

- **Count queries**: How many times does pattern P occur? (O(m) time)
- **Locate queries**: Where does pattern P occur? (O(m + k) time)

#### How It Works

```python
# Simplified example
seq = "ACGTACGT$"
fm = FMIndex(seq)
count = fm.count(b"ACG")  # Returns 2
positions = fm.locate(b"ACG")  # Returns [0, 4]
```

The FM-index uses:
- **Suffix Array**: Built using `pydivsufsort` (fast C implementation)
- **BWT (Burrows-Wheeler Transform)**: Permutation of the sequence
- **C-table**: Cumulative character counts
- **Wavelet Tree**: For efficient rank queries

#### Backward Search Algorithm

The key to FM-index efficiency is **backward search**:

```
For pattern P = "ACG":
  1. Start with range [0, n) covering all suffixes
  2. Process 'G': narrow range to suffixes starting with 'G'
  3. Process 'C': narrow range to suffixes starting with 'CG'
  4. Process 'A': narrow range to suffixes starting with 'ACG'
  5. Range size = number of occurrences
```

This is why counting is O(m) - we only need to process each character once.

### 2. Wavelet Tree: Enabling Rank Queries

The **Wavelet Tree** is a succinct data structure that answers rank queries efficiently:

- **Rank(symbol, i)**: How many times does `symbol` appear in positions [0, i)?

This is exactly what backward search needs to narrow the search range.

#### Structure

```
        Root (bitvector: 0101...)
       /                      \
   Left (A,C)              Right (G,T)
  /         \              /         \
A           C            G           T
```

Each internal node stores a bitvector indicating which child each position goes to.

### 3. Parallel Processing Strategy

Bioquik uses **process-based parallelism** via `ProcessPoolExecutor`:

- Each FASTA file is processed independently
- No shared state between workers
- Linear speedup with number of CPU cores

**Why processes over threads?**
- Python's GIL prevents true parallelism with threads
- Processes bypass GIL for CPU-bound tasks
- Each process has its own memory space (no synchronization needed)

### 4. Pattern Expansion

Wildcard patterns like `*CG*` are expanded into concrete motifs:

```
Pattern: *CG*
Wildcards: 1 before CG, 1 after CG
Expansion: 4 × 4 = 16 motifs
  ACGA, ACGC, ACGG, ACGT
  CCGA, CCGC, CCGG, CCGT
  GCGA, GCGC, GCGG, GCGT
  TCGA, TCGC, TCGG, TCGT
```

The expansion uses Cartesian product of DNA bases (A, C, G, T).

## Data Flow

### Input Processing

```
FASTA File
  ↓
Read lines (skip headers starting with '>')
  ↓
Concatenate sequences
  ↓
Normalize to uppercase
  ↓
Build FM-index
```

### Pattern Matching

```
Pattern List: ["*CG*", "**CG**"]
  ↓
Expand to Motifs: ["ACGA", "ACGC", ..., "TCGT", ...]
  ↓
For each motif:
  - Encode to bytes
  - Query FM-index
  - Count occurrences (non-overlapping)
  ↓
Store results: {Pattern, Motif, Count}
```

### Output Generation

```
Per-file CSVs
  ↓
Concatenate (pandas)
  ↓
Write combined CSV
  ↓
(Optional) Aggregate to JSON
  ↓
(Optional) Generate plots
```

## Memory Management

### FM-Index Memory Usage

For a sequence of length `n`:
- Suffix array: ~4n bytes (32-bit integers)
- BWT: n bytes
- C-table: ~16 bytes (4 characters × 4 bytes)
- Wavelet tree: ~n log σ bits ≈ n/2 bytes (for DNA)
- **Total**: ~5.5n bytes

For a 1GB sequence: ~5.5GB memory (reasonable for modern systems)

### Optimization: SA Sampling

The suffix array is sampled (every 32nd position) to reduce memory:
- **Count queries**: No SA needed (already fast)
- **Locate queries**: May need to "walk back" to find sampled position
- Trade-off: Slightly slower locate, much less memory

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| FM-index construction | O(n log n) | Via divsufsort |
| Pattern counting | O(m) | m = pattern length |
| Pattern locating | O(m + k) | k = occurrences |
| Per-file processing | O(n log n + m×k) | Construction + queries |
| Overall (f files) | O(f × (n log n + m×k)) | Sequential |
| Overall (parallel) | O((n log n + m×k)) | With f cores |

### Space Complexity

- FM-index: O(n)
- Wavelet tree: O(n log σ) = O(n) for DNA
- **Total per file**: O(n)

### Parallelization Efficiency

- **Ideal speedup**: Linear with number of cores
- **Bottlenecks**: 
  - I/O for many small files
  - Memory for very large files
  - GIL doesn't affect (using processes)

## Extension Points

### Adding New Pattern Types

To support different pattern syntax:

```python
# In motifs.py
def expand_custom_pattern(pattern: str) -> List[str]:
    # Your expansion logic
    pass

def build_pattern_to_motifs(patterns: List[str]) -> Dict[str, List[str]]:
    # Integrate custom expansion
    ...
```

### Custom Counting Strategies

Modify `_count_in_fm()` in `fasta_worker.py`:

```python
def _count_in_fm(fm: FMIndex, motif: bytes, *, 
                 strategy: str = "non_overlapping") -> int:
    if strategy == "overlapping":
        return fm.count(motif)
    elif strategy == "non_overlapping":
        # Current implementation
        ...
    elif strategy == "maximal":
        # New strategy
        ...
```

### Alternative Index Structures

Implement a new index with the same interface:

```python
class MyCustomIndex:
    def count(self, pattern: bytes) -> int:
        ...
    def locate(self, pattern: bytes) -> List[int]:
        ...

# In fasta_worker.py, swap:
# fm = FMIndex(seq)
fm = MyCustomIndex(seq)
```

## Design Decisions

### Why FM-Index?

- **Memory efficient**: Compressed suffix array
- **Fast queries**: O(m) counting, O(m + k) locating
- **Mature algorithm**: Well-studied, reliable

### Why Non-Overlapping Counts?

- **Biological relevance**: Overlapping motifs may not be independent
- **Configurable**: Can enable overlapping via parameter

### Why Per-File CSVs?

- **Incremental processing**: Can process files independently
- **Debugging**: Easy to inspect individual file results
- **Flexibility**: Users can process subsets

### Why Process-Based Parallelism?

- **GIL bypass**: True parallelism for CPU-bound tasks
- **Isolation**: Process crashes don't affect others
- **Scalability**: Linear speedup with cores

## Testing Strategy

### Unit Tests

Each module has corresponding test file:
- `test_fmindex.py`: FM-index correctness
- `test_wavelettree.py`: Wavelet tree queries
- `test_motifs.py`: Pattern expansion
- `test_processor.py`: Parallel processing
- `test_reports.py`: Output generation

### Integration Tests

- `test_cli.py`: End-to-end CLI workflows
- Test with real FASTA files
- Verify output formats

### Performance Tests

- Benchmark with various file sizes
- Measure parallelization efficiency
- Profile memory usage

## Future Enhancements

### Potential Improvements

1. **Index Caching**: Reuse FM-indexes for repeated queries
2. **Streaming**: Process files too large for memory
3. **Distributed**: Scale to multiple machines
4. **GPU Acceleration**: Offload FM-index construction
5. **Compressed Storage**: Store indexes on disk

### Research Directions

- Alternative index structures (BWT variants)
- Approximate matching support
- Multi-pattern batch queries
- Real-time streaming queries

## Further Reading

- **FM-Index**: Ferragina & Manzini (2000) "Opportunistic Data Structures"
- **Wavelet Trees**: Grossi et al. (2003) "High-Order Entropy-Compressed Text Indexes"
- **Suffix Arrays**: Manber & Myers (1993) "Suffix Arrays: A New Method for On-Line String Searches"
