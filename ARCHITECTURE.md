# Bioquik Architecture Documentation

## Overview

**Bioquik** is a high-performance bioinformatics toolkit for counting CG-anchored DNA motifs in FASTA files. It uses advanced data structures (FM-index and Wavelet Trees) to achieve memory-efficient pattern matching with parallel processing capabilities.

## System Architecture

### High-Level Flow

```
User Input (CLI)
    ↓
Validation Layer
    ↓
Pattern Expansion (Wildcards → Motifs)
    ↓
Parallel Processing (ProcessPoolExecutor)
    ├─→ FASTA File 1 → FM-Index → Count Motifs → CSV
    ├─→ FASTA File 2 → FM-Index → Count Motifs → CSV
    └─→ FASTA File N → FM-Index → Count Motifs → CSV
    ↓
Report Aggregation
    ├─→ Combined CSV
    ├─→ Optional JSON Summary
    └─→ Optional Plots
```

## Component Architecture

### 1. CLI Layer (`cli.py`)

**Purpose**: User-facing command-line interface using Typer.

**Responsibilities**:
- Parse command-line arguments
- Validate inputs
- Orchestrate the processing pipeline
- Handle output directory management

**Key Functions**:
- `count()`: Main command handler that coordinates the entire workflow

**Dependencies**: `processor`, `reports`, `plotter`, `validate`

---

### 2. Validation Layer (`validate.py`)

**Purpose**: Input validation and error handling.

**Key Functions**:
- `validate_patterns()`: Ensures patterns contain 'CG' anchor
- `validate_dir()`: Verifies directory existence

**Design Decision**: Early validation prevents wasted computation on invalid inputs.

---

### 3. Pattern Expansion (`motifs.py`)

**Purpose**: Expands wildcard patterns (e.g., `**CG**`) into concrete DNA motifs.

**Key Functions**:
- `generate_motifs()`: Expands patterns into a flat list of motifs
- `build_pattern_to_motifs()`: Creates a mapping from pattern keys to motif lists

**Algorithm**:
- Splits pattern at 'CG' anchor
- Counts wildcards before and after 'CG'
- Uses Cartesian product to generate all combinations
- Example: `*CG*` → `ACGA`, `ACGC`, `ACGG`, `ACGT`, `CCGA`, ...

**Design Decision**: Pattern-to-motif mapping allows tracking which pattern generated each motif in results.

---

### 4. Processing Orchestrator (`processor.py`)

**Purpose**: Manages parallel processing of multiple FASTA files.

**Key Functions**:
- `run_count()`: Main orchestrator function

**Parallelization Strategy**:
- Uses `ProcessPoolExecutor` for true parallelism (bypasses GIL)
- Each worker process handles one FASTA file independently
- Progress tracking via Rich progress bar

**Design Decisions**:
- Process-based parallelism: Better for CPU-bound tasks than threads
- Each file processed independently: No shared state, easier parallelization
- Progress callbacks: User feedback during long-running operations

---

### 5. FASTA Worker (`fasta_worker.py`)

**Purpose**: Processes a single FASTA file and counts motifs.

**Key Functions**:
- `process_fasta_file()`: Main processing function for one file
- `_count_in_fm()`: Helper for counting with overlap handling

**Workflow**:
1. Read and parse FASTA file (skip headers, concatenate sequences)
2. Build FM-index from sequence
3. For each motif, count occurrences (non-overlapping by default)
4. Write results to CSV file

**Design Decisions**:
- Non-overlapping counts by default: More biologically meaningful
- Per-file CSV output: Enables incremental processing and debugging
- Returns output path: Allows caller to track generated files

---

### 6. FM-Index (`fmindex.py`)

**Purpose**: Core data structure for efficient pattern matching.

**Class**: `FMIndex`

**Key Components**:
1. **Suffix Array**: Built using `pydivsufsort` (external C library)
2. **Burrows-Wheeler Transform (BWT)**: Derived from suffix array
3. **C-table**: Cumulative character counts (for backward search)
4. **Wavelet Tree**: For rank queries on BWT
5. **SA Sampling**: For locate queries (space-time tradeoff)

**Key Methods**:
- `count(pattern)`: Returns number of occurrences
- `locate(pattern)`: Returns all start positions
- `_backward_search()`: Core search algorithm

**Algorithm - Backward Search**:
```
For pattern P = pₙ...p₁:
  Initialize [lo, hi) = [0, n)
  For each symbol pᵢ (right to left):
    lo = C[pᵢ] + rank(pᵢ, lo)
    hi = C[pᵢ] + rank(pᵢ, hi)
  Return hi - lo (count) or positions in [lo, hi)
```

**Time Complexity**:
- Count: O(m) where m = pattern length
- Locate: O(m + k) where k = number of occurrences

**Space Complexity**: O(n) where n = sequence length

**Design Decisions**:
- SA sampling: Reduces memory at cost of slower locate queries
- Wavelet Tree: Enables efficient rank queries needed for backward search
- Sentinel character ($): Ensures unique suffix array

---

### 7. Wavelet Tree (`wavelettree.py`)

**Purpose**: Succinct data structure for rank queries on sequences.

**Class**: `WaveletTree`

**Structure**:
- Binary recursive tree
- Each internal node stores a bitvector
- Leaf nodes represent single characters
- Prefix rank samples for O(1) rank queries

**Key Methods**:
- `rank(symbol, i)`: Count occurrences of symbol in [0, i)

**Algorithm**:
1. Partition alphabet into left/right halves
2. Build bitvector: 0 for left alphabet, 1 for right
3. Recursively build left and right subtrees
4. Sample prefix ranks every `sample_rate` bits

**Time Complexity**: O(log σ) where σ = alphabet size (4 for DNA)

**Space Complexity**: O(n log σ) bits

**Design Decisions**:
- Binary recursive structure: Simple and efficient for small alphabets
- Rank sampling: Trade memory for query speed
- Leaf optimization: No bitvector needed for single-character nodes

---

### 8. Report Generation (`reports.py`)

**Purpose**: Aggregates and formats results.

**Key Functions**:
- `combine_csv()`: Concatenates all per-file CSVs
- `write_summary()`: Writes combined CSV and optional JSON

**Output Formats**:
- **CSV**: Tabular format with columns: Pattern, Motif, Count
- **JSON**: Aggregated counts per motif (optional)

**Design Decisions**:
- Always generate combined CSV: Standard output format
- JSON as optional: Reduces I/O for users who don't need it
- Pandas for aggregation: Leverages efficient DataFrame operations

---

### 9. Visualization (`plotter.py`)

**Purpose**: Generate plots for motif analysis (optional feature).

**Key Functions**:
- `plot_distribution()`: Bar chart of total counts per motif
- `plot_heatmap()`: Heatmap of counts by file and motif

**Dependencies**: `matplotlib` (optional, via `bioquik[viz]`)

**Design Decisions**:
- Optional dependency: Keeps core package lightweight
- Graceful handling of empty data: Prevents crashes on edge cases

---

## Data Flow

### Input
- **Patterns**: Comma-separated wildcard strings (e.g., `"*CG*,**CG**"`)
- **FASTA Files**: Directory containing `.fasta` files
- **Configuration**: Number of workers, output options

### Processing
1. Patterns validated and expanded to motifs
2. Each FASTA file processed independently:
   - Sequence extracted and normalized
   - FM-index constructed
   - Motifs counted using backward search
   - Results written to per-file CSV
3. Results aggregated across files

### Output
- Per-file CSVs: `{filename}_motif_counts.csv`
- Combined CSV: `combined_counts.csv`
- Optional JSON: `combined_counts.json`
- Optional plots: `motif_distribution.png`, `motif_heatmap.png`

## Design Patterns

### 1. **Worker Pattern**
- `fasta_worker.py` implements stateless worker functions
- Enables easy parallelization via `ProcessPoolExecutor`

### 2. **Pipeline Pattern**
- Clear separation: Validation → Expansion → Processing → Aggregation
- Each stage has single responsibility

### 3. **Strategy Pattern** (implicit)
- Overlap vs. non-overlap counting via `allow_overlap` parameter
- Extensible for future counting strategies

### 4. **Builder Pattern** (implicit)
- FM-index construction: Complex object built step-by-step
- Wavelet tree construction: Recursive building

## Performance Characteristics

### Time Complexity
- **Pattern Expansion**: O(p × 4^w) where p = patterns, w = wildcards
- **FM-Index Construction**: O(n log n) via divsufsort
- **Pattern Counting**: O(m) per pattern where m = pattern length
- **Overall**: O(n log n + f × (m × k)) where f = files, k = motifs

### Space Complexity
- **FM-Index**: O(n) for sequence of length n
- **Wavelet Tree**: O(n log σ) bits
- **Per-file processing**: Memory scales with largest file

### Parallelization Benefits
- Linear speedup with number of CPU cores (for I/O-bound or many files)
- Process-based: Avoids GIL limitations
- Independent files: No synchronization overhead

## Extension Points

### Adding New Pattern Types
- Extend `motifs.py` with new expansion logic
- Update validation in `validate.py`

### Adding New Output Formats
- Extend `reports.py` with new formatters
- Add CLI options in `cli.py`

### Custom Counting Strategies
- Extend `_count_in_fm()` in `fasta_worker.py`
- Add parameters for different counting modes

### Alternative Index Structures
- Implement new index class with same interface as `FMIndex`
- Swap in `fasta_worker.py` via dependency injection

## Testing Strategy

- **Unit Tests**: Each module tested independently
- **Integration Tests**: End-to-end CLI workflows
- **Test Files**: Located in `tests/` directory
- **Coverage**: Aim for high coverage of core algorithms

## Dependencies

### Core
- `pandas`: Data manipulation and CSV handling
- `pydivsufsort`: Fast suffix array construction (C extension)
- `typer`: CLI framework
- `rich`: Progress bars and formatted output
- `tqdm`: Progress indicators

### Optional
- `matplotlib`: Visualization (via `bioquik[viz]`)

### Development
- `pytest`: Testing framework
- `ruff`: Linting
- `sphinx`: Documentation generation

## Future Considerations

### Potential Improvements
1. **Streaming Processing**: For very large files that don't fit in memory
2. **Index Caching**: Reuse FM-indexes for repeated queries
3. **Distributed Processing**: Scale beyond single machine
4. **Alternative Algorithms**: Support for other index structures
5. **Real-time Progress**: More granular progress reporting
6. **Configuration Files**: YAML/JSON config for complex workflows

### Scalability Limits
- **Memory**: Limited by largest FASTA file size
- **CPU**: Linear scaling with cores (process-based parallelism)
- **I/O**: May become bottleneck with many small files

## Glossary

- **FM-Index**: Full-text index in Minute space - compressed suffix array variant
- **BWT**: Burrows-Wheeler Transform - permutation of text used in FM-index
- **Suffix Array**: Array of all suffixes sorted lexicographically
- **Wavelet Tree**: Succinct data structure for rank/select queries
- **Rank Query**: Count occurrences of symbol up to position i
- **CG Anchor**: Required 'CG' dinucleotide in patterns (biological constraint)
- **Motif**: Specific DNA sequence pattern (e.g., "ACGT")
- **Pattern**: Wildcard template (e.g., "*CG*")
