# Bioquik Module Reference

This document provides a detailed reference for each module in the Bioquik codebase, including purpose, key functions, and usage examples.

## Module Overview

```
bioquik/
├── __init__.py          # Package exports
├── cli.py               # Command-line interface
├── processor.py         # Parallel processing orchestrator
├── fasta_worker.py      # Single-file processing
├── fmindex.py          # FM-index data structure
├── wavelettree.py      # Wavelet tree for rank queries
├── motifs.py           # Pattern expansion utilities
├── reports.py          # Report generation
├── plotter.py          # Visualization (optional)
└── validate.py         # Input validation
```

---

## `__init__.py` - Package Exports

**Purpose**: Defines the public API of the bioquik package.

**Exports**:
- `WaveletTree`: Wavelet tree class
- `FMIndex`: FM-index class
- `build_pattern_to_motifs`: Pattern expansion function
- `generate_motifs`: Motif generation function
- `process_fasta_file`: Single-file processing function

**Usage**:
```python
from bioquik import FMIndex, process_fasta_file
```

---

## `cli.py` - Command-Line Interface

**Purpose**: Provides the `bioquik` command-line tool using Typer.

**Key Components**:
- `app`: Typer application instance
- `count()`: Main command for counting motifs

**Command Structure**:
```bash
bioquik count \
  --patterns "*CG*,**CG**" \
  --seq-dir data/fasta \
  --out-dir results \
  --workers 4 \
  --json-out \
  --plot
```

**Workflow**:
1. Validates inputs (patterns, directories)
2. Clears/create output directory
3. Calls `run_count()` for parallel processing
4. Aggregates results via `combine_csv()`
5. Writes summary via `write_summary()`
6. Optionally generates plots

**Dependencies**: `processor`, `reports`, `plotter`, `validate`

---

## `processor.py` - Processing Orchestrator

**Purpose**: Manages parallel processing of multiple FASTA files.

**Key Function**:
```python
def run_count(
    pattern_list: List[str],
    seq_dir: Path,
    out_dir: Path,
    workers: int,
) -> None
```

**Responsibilities**:
- Expands patterns to motifs via `build_pattern_to_motifs()`
- Discovers all `.fasta` files in `seq_dir`
- Submits files to `ProcessPoolExecutor` for parallel processing
- Tracks progress with Rich progress bar
- Propagates exceptions from workers

**Parallelization**:
- Uses `ProcessPoolExecutor` (bypasses GIL)
- Each worker processes one FASTA file independently
- No shared state between workers

**Example**:
```python
from bioquik.processor import run_count
from pathlib import Path

run_count(
    pattern_list=["*CG*", "**CG**"],
    seq_dir=Path("data/fasta"),
    out_dir=Path("results"),
    workers=4
)
```

---

## `fasta_worker.py` - Single-File Processing

**Purpose**: Processes one FASTA file and counts motifs.

**Key Function**:
```python
def process_fasta_file(
    fasta_path: str | os.PathLike,
    pattern_to_motifs: dict[str, list[str]],
    *,
    out_dir: str | os.PathLike = "bioquik_results",
) -> str
```

**Workflow**:
1. Reads FASTA file (skips headers, concatenates sequences)
2. Normalizes sequence to uppercase
3. Builds FM-index from sequence
4. For each pattern and motif:
   - Counts occurrences (non-overlapping by default)
   - Stores results if count > 0
5. Writes CSV: `{filename}_motif_counts.csv`
6. Returns output file path

**Helper Function**:
```python
def _count_in_fm(
    fm: FMIndex,
    motif: bytes,
    *,
    allow_overlap: bool = False
) -> int
```

**Counting Strategy**:
- **Non-overlapping** (default): Uses `locate()` and filters overlapping positions
- **Overlapping**: Uses `count()` directly

**Example**:
```python
from bioquik.fasta_worker import process_fasta_file
from bioquik.motifs import build_pattern_to_motifs

mapping = build_pattern_to_motifs(["*CG*"])
csv_path = process_fasta_file(
    "example.fasta",
    mapping,
    out_dir="results"
)
```

**Design Notes**:
- Stateless function: Safe for parallel execution
- Returns output path: Enables tracking generated files
- Per-file CSV: Enables incremental processing

---

## `fmindex.py` - FM-Index Implementation

**Purpose**: Provides FM-index data structure for efficient pattern matching.

**Class**: `FMIndex`

**Constructor**:
```python
def __init__(self, seq: str, *, sa_sample_rate: int = 32)
```

**Key Methods**:
- `count(pattern: bytes) -> int`: Count occurrences
- `locate(pattern: bytes) -> List[int]`: Find all positions
- `_backward_search(pattern: bytes) -> Tuple[int, int]`: Core search

**Internal Components**:
1. **Sequence**: Original sequence (with sentinel `$`)
2. **Suffix Array**: Built via `pydivsufsort`
3. **BWT**: Burrows-Wheeler Transform
4. **C-table**: Cumulative character counts
5. **Wavelet Tree**: For rank queries
6. **SA Samples**: Sampled suffix array positions

**Algorithm**:
- **Construction**: O(n log n) via divsufsort
- **Count**: O(m) via backward search
- **Locate**: O(m + k) where k = occurrences

**Example**:
```python
from bioquik import FMIndex

seq = "ACGTACGT"
fm = FMIndex(seq)

count = fm.count(b"ACG")  # Returns 2
positions = fm.locate(b"ACG")  # Returns [0, 4]
```

**Design Notes**:
- Adds sentinel `$` automatically
- SA sampling reduces memory (configurable rate)
- Wavelet tree enables efficient rank queries

---

## `wavelettree.py` - Wavelet Tree Implementation

**Purpose**: Succinct data structure for rank queries.

**Class**: `WaveletTree`

**Constructor**:
```python
def __init__(
    self,
    data: bytes,
    alphabet: bytes,
    *,
    sample_rate: int = 32
)
```

**Key Method**:
```python
def rank(symbol: int, i: int) -> int
```
Returns number of occurrences of `symbol` in positions [0, i).

**Structure**:
- Binary recursive tree
- Internal nodes: Bitvectors
- Leaf nodes: Single characters
- Prefix rank samples for O(1) queries

**Algorithm**:
1. Partition alphabet into left/right halves
2. Build bitvector: 0 = left, 1 = right
3. Recursively build subtrees
4. Sample prefix ranks every `sample_rate` bits

**Time Complexity**: O(log σ) where σ = alphabet size

**Space Complexity**: O(n log σ) bits

**Example**:
```python
from bioquik import WaveletTree

data = b"ACGTACGT"
alphabet = b"ACGT"
wt = WaveletTree(data, alphabet)

rank_a = wt.rank(ord('A'), 4)  # Count 'A' in [0, 4) = 1
```

**Design Notes**:
- Optimized for small alphabets (DNA: 4 characters)
- Leaf nodes don't need bitvectors
- Rank sampling trades memory for query speed

---

## `motifs.py` - Pattern Expansion

**Purpose**: Expands wildcard patterns into concrete DNA motifs.

**Key Functions**:

### `generate_motifs(patterns: list[str]) -> list[str]`
Expands patterns into a flat, deduplicated list of motifs.

**Example**:
```python
from bioquik.motifs import generate_motifs

patterns = ["*CG*", "**CG**"]
motifs = generate_motifs(patterns)
# Returns: ["ACGA", "ACGC", ..., "TCGT", ...] (sorted, unique)
```

### `build_pattern_to_motifs(patterns: list[str]) -> Dict[str, List[str]]`
Creates mapping from pattern keys to motif lists.

**Pattern Keys**: Patterns with `*` replaced by `N` (e.g., `"*CG*"` → `"NCGN"`)

**Example**:
```python
from bioquik.motifs import build_pattern_to_motifs

mapping = build_pattern_to_motifs(["*CG*", "**CG**"])
# Returns: {
#   "NCGN": ["ACGA", "ACGC", "ACGG", "ACGT", ...],
#   "NNCGNN": ["AACGAA", "AACGAC", ...]
# }
```

**Algorithm**:
1. Split pattern at 'CG' anchor
2. Count wildcards before/after 'CG'
3. Generate Cartesian product of bases (A, C, G, T)
4. Combine into motifs

**Design Notes**:
- Pattern keys use 'N' to distinguish from wildcards
- Enables tracking which pattern generated each motif
- Deduplication ensures unique motifs

---

## `reports.py` - Report Generation

**Purpose**: Aggregates and formats results.

**Key Functions**:

### `combine_csv(out_dir: Path) -> pd.DataFrame`
Reads all `*_motif_counts.csv` files and concatenates them.

**Example**:
```python
from bioquik.reports import combine_csv
from pathlib import Path

df = combine_csv(Path("results"))
# Returns: DataFrame with columns [Pattern, Motif, Count]
```

### `write_summary(df: pd.DataFrame, out_dir: Path, json_out: bool = False) -> None`
Writes combined CSV and optional JSON summary.

**Output Files**:
- `combined_counts.csv`: Always generated
- `combined_counts.json`: Generated if `json_out=True`

**JSON Format**:
```json
{
  "ACGA": 42,
  "ACGC": 15,
  ...
}
```

**Example**:
```python
from bioquik.reports import write_summary
import pandas as pd

df = pd.DataFrame({
    "Pattern": ["NCGN", "NCGN"],
    "Motif": ["ACGA", "ACGC"],
    "Count": [10, 5]
})

write_summary(df, Path("results"), json_out=True)
```

**Design Notes**:
- Always generates CSV (standard output)
- JSON is optional (reduces I/O)
- Uses pandas for efficient aggregation

---

## `plotter.py` - Visualization

**Purpose**: Generates plots for motif analysis (optional feature).

**Key Functions**:

### `plot_distribution(df: pd.DataFrame, out_dir: Path) -> None`
Creates bar chart of total counts per motif.

**Output**: `motif_distribution.png`

**Example**:
```python
from bioquik.plotter import plot_distribution
import pandas as pd
from pathlib import Path

df = pd.DataFrame({
    "Motif": ["ACGA", "ACGC"],
    "Count": [10, 5]
})

plot_distribution(df, Path("results"))
```

### `plot_heatmap(df: pd.DataFrame, out_dir: Path) -> None`
Creates heatmap of counts by file and motif.

**Output**: `motif_heatmap.png`

**Example**:
```python
from bioquik.plotter import plot_heatmap

plot_heatmap(df, Path("results"))
```

**Dependencies**: `matplotlib` (optional, install via `bioquik[viz]`)

**Design Notes**:
- Optional dependency: Keeps core package lightweight
- Graceful handling of empty data
- Supports both long-form and wide-form DataFrames

---

## `validate.py` - Input Validation

**Purpose**: Validates user inputs and provides error messages.

**Key Functions**:

### `validate_patterns(patterns: str) -> List[str]`
Validates and parses comma-separated patterns.

**Requirements**:
- Must contain 'CG' anchor
- Returns list of stripped patterns

**Example**:
```python
from bioquik.validate import validate_patterns

patterns = validate_patterns("*CG*,**CG**")
# Returns: ["*CG*", "**CG**"]

# Raises typer.Exit if 'CG' not found
```

### `validate_dir(path: Path, name: str) -> None`
Validates that path exists and is a directory.

**Example**:
```python
from bioquik.validate import validate_dir
from pathlib import Path

validate_dir(Path("data/fasta"), "sequence")
# Raises typer.Exit if path doesn't exist or isn't a directory
```

**Design Notes**:
- Early validation prevents wasted computation
- Uses Typer for consistent error handling
- Clear error messages for users

---

## Module Dependencies

```
cli.py
├── processor.py
│   ├── fasta_worker.py
│   │   ├── fmindex.py
│   │   │   └── wavelettree.py
│   │   └── motifs.py
│   └── motifs.py
├── reports.py
├── plotter.py (optional)
└── validate.py
```

## Usage Patterns

### Basic Usage (CLI)
```bash
bioquik count --patterns "*CG*" --seq-dir data --out-dir results
```

### Programmatic Usage
```python
from bioquik.processor import run_count
from pathlib import Path

run_count(
    pattern_list=["*CG*"],
    seq_dir=Path("data"),
    out_dir=Path("results"),
    workers=4
)
```

### Low-Level Usage
```python
from bioquik import FMIndex, process_fasta_file
from bioquik.motifs import build_pattern_to_motifs

# Build pattern mapping
mapping = build_pattern_to_motifs(["*CG*"])

# Process single file
csv_path = process_fasta_file("example.fasta", mapping)
```

### Direct Index Usage
```python
from bioquik import FMIndex

seq = "ACGTACGT"
fm = FMIndex(seq)
count = fm.count(b"ACG")
positions = fm.locate(b"ACG")
```

---

## Extension Examples

### Custom Pattern Expansion
```python
# In motifs.py
def expand_custom_pattern(pattern: str) -> List[str]:
    # Your logic here
    pass
```

### Custom Counting Strategy
```python
# In fasta_worker.py
def _count_maximal(fm: FMIndex, motif: bytes) -> int:
    # Count only maximal matches
    pass
```

### Alternative Index
```python
# Implement same interface as FMIndex
class MyIndex:
    def count(self, pattern: bytes) -> int: ...
    def locate(self, pattern: bytes) -> List[int]: ...
```

---

## Testing

Each module has corresponding test file:
- `test_cli.py`: CLI integration tests
- `test_processor.py`: Parallel processing tests
- `test_fmindex.py`: FM-index correctness
- `test_wavelettree.py`: Wavelet tree queries
- `test_motifs.py`: Pattern expansion
- `test_reports.py`: Report generation
- `test_validate.py`: Input validation
- `test_plotter.py`: Visualization

Run tests:
```bash
pytest tests/
```
