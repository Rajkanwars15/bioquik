# Bioquik Architecture Summary

## Executive Summary

**Bioquik** is a bioinformatics toolkit that counts CG-anchored DNA motifs in FASTA files using advanced data structures (FM-index and Wavelet Trees) for efficient pattern matching. The system is designed for parallel processing of multiple files with a clean, modular architecture.

## System Overview

### Core Purpose
Count DNA motifs (patterns like `*CG*`) across multiple FASTA files efficiently and in parallel.

### Key Technologies
- **FM-Index**: Compressed suffix array for O(m) pattern counting
- **Wavelet Tree**: Succinct data structure for rank queries
- **ProcessPoolExecutor**: True parallelism (bypasses Python GIL)
- **Typer**: Modern CLI framework

## Architecture Layers

```
┌─────────────────────────────────────┐
│         CLI Layer (cli.py)          │  User Interface
├─────────────────────────────────────┤
│      Validation (validate.py)       │  Input Validation
├─────────────────────────────────────┤
│    Pattern Expansion (motifs.py)    │  Wildcard → Motifs
├─────────────────────────────────────┤
│   Processor (processor.py)          │  Parallel Orchestration
├─────────────────────────────────────┤
│   FASTA Worker (fasta_worker.py)    │  Single-File Processing
├─────────────────────────────────────┤
│   FM-Index (fmindex.py)             │  Pattern Matching Engine
├─────────────────────────────────────┤
│   Wavelet Tree (wavelettree.py)     │  Rank Query Support
├─────────────────────────────────────┤
│   Reports (reports.py)              │  Output Generation
└─────────────────────────────────────┘
```

## Data Flow

```
Input: Patterns + FASTA Directory
  ↓
1. Validate inputs
  ↓
2. Expand patterns: "*CG*" → ["ACGA", "ACGC", ...]
  ↓
3. For each FASTA file (parallel):
   a. Read sequence
   b. Build FM-index
   c. Count each motif
   d. Write per-file CSV
  ↓
4. Aggregate results
  ↓
5. Generate reports (CSV, JSON, plots)
  ↓
Output: Combined results
```

## Key Components

### 1. FM-Index (`fmindex.py`)
**Purpose**: Core pattern matching engine

**How it works**:
- Builds suffix array from sequence
- Creates Burrows-Wheeler Transform (BWT)
- Uses backward search for O(m) counting
- Supports both count and locate queries

**Performance**: O(n log n) construction, O(m) counting

### 2. Wavelet Tree (`wavelettree.py`)
**Purpose**: Enables efficient rank queries for FM-index

**How it works**:
- Binary recursive tree structure
- Each node stores bitvector
- Samples prefix ranks for O(1) queries
- Time complexity: O(log σ) per query

### 3. Pattern Expansion (`motifs.py`)
**Purpose**: Converts wildcards to concrete motifs

**How it works**:
- Splits pattern at 'CG' anchor
- Counts wildcards before/after
- Generates Cartesian product of bases
- Example: `*CG*` → 16 motifs (4×4)

### 4. Parallel Processing (`processor.py`)
**Purpose**: Orchestrates parallel file processing

**How it works**:
- Uses ProcessPoolExecutor (bypasses GIL)
- Each worker processes one file independently
- Progress tracking with Rich progress bar
- No shared state (stateless workers)

## Design Decisions

### Why FM-Index?
- **Memory efficient**: Compressed suffix array
- **Fast queries**: O(m) counting vs O(nm) naive
- **Mature algorithm**: Well-studied and reliable

### Why Process-Based Parallelism?
- **GIL bypass**: True parallelism for CPU-bound tasks
- **Isolation**: Process crashes don't affect others
- **Scalability**: Linear speedup with cores

### Why Non-Overlapping Counts?
- **Biological relevance**: Overlapping motifs may not be independent
- **Configurable**: Can enable overlapping if needed

### Why Per-File CSVs?
- **Incremental processing**: Process files independently
- **Debugging**: Easy to inspect individual results
- **Flexibility**: Users can process subsets

## Performance Characteristics

### Time Complexity
- **FM-index construction**: O(n log n)
- **Pattern counting**: O(m) per pattern
- **Overall (f files, k motifs)**: O(f × (n log n + m×k))
- **With parallelization**: O(n log n + m×k) with f cores

### Space Complexity
- **FM-index**: O(n) where n = sequence length
- **Wavelet tree**: O(n log σ) ≈ O(n) for DNA
- **Total per file**: ~5.5n bytes

### Scalability
- **Memory**: Limited by largest FASTA file
- **CPU**: Linear scaling with cores
- **I/O**: May bottleneck with many small files

## Extension Points

### Easy Extensions
1. **New pattern types**: Extend `motifs.py`
2. **New output formats**: Extend `reports.py`
3. **New counting strategies**: Modify `_count_in_fm()`
4. **Alternative indexes**: Implement same interface as `FMIndex`

### Future Enhancements
1. **Index caching**: Reuse FM-indexes for repeated queries
2. **Streaming**: Process files too large for memory
3. **Distributed processing**: Scale to multiple machines
4. **GPU acceleration**: Offload FM-index construction

## Module Responsibilities

| Module | Responsibility | Key Function |
|--------|---------------|--------------|
| `cli.py` | User interface | `count()` command |
| `validate.py` | Input validation | `validate_patterns()`, `validate_dir()` |
| `motifs.py` | Pattern expansion | `build_pattern_to_motifs()` |
| `processor.py` | Parallel orchestration | `run_count()` |
| `fasta_worker.py` | Single-file processing | `process_fasta_file()` |
| `fmindex.py` | Pattern matching | `FMIndex.count()`, `FMIndex.locate()` |
| `wavelettree.py` | Rank queries | `WaveletTree.rank()` |
| `reports.py` | Output generation | `combine_csv()`, `write_summary()` |
| `plotter.py` | Visualization | `plot_distribution()`, `plot_heatmap()` |

## Testing Strategy

- **Unit tests**: Each module tested independently
- **Integration tests**: End-to-end CLI workflows
- **Test coverage**: High coverage of core algorithms
- **Test files**: Located in `tests/` directory

## Dependencies

### Core
- `pandas`: Data manipulation
- `pydivsufsort`: Fast suffix array construction
- `typer`: CLI framework
- `rich`: Progress bars
- `tqdm`: Progress indicators

### Optional
- `matplotlib`: Visualization (via `bioquik[viz]`)

## Code Quality

- **Type hints**: All functions typed
- **Docstrings**: Google-style docstrings
- **Linting**: Ruff for code quality
- **Testing**: Pytest with high coverage
- **Documentation**: Comprehensive docs

## Getting Started for Developers

1. **Read**: [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
2. **Explore**: [MODULES.md](MODULES.md) for module details
3. **Contribute**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for guidelines
4. **Deep dive**: [docs/source/architecture.md](docs/source/architecture.md) for algorithms

## Key Takeaways

1. **Modular design**: Clear separation of concerns
2. **Efficient algorithms**: FM-index for fast pattern matching
3. **Parallel processing**: Process-based for true parallelism
4. **Extensible**: Easy to add new features
5. **Well-tested**: Comprehensive test coverage
6. **Well-documented**: Multiple documentation levels

## Next Steps

- **Users**: See [README.md](README.md) and [docs/source/quickstart.md](docs/source/quickstart.md)
- **Developers**: See [ARCHITECTURE.md](ARCHITECTURE.md) and [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Researchers**: See [docs/source/architecture.md](docs/source/architecture.md)
