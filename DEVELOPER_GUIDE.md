# Bioquik Developer Guide

This guide is for developers who want to understand, modify, or extend Bioquik.

## Quick Start for Developers

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Rajkanwars15/bioquik
cd bioquik

# Install in editable mode with dev dependencies
pip install -e '.[dev,docs]'

# Run tests
pytest tests/

# Run linter
ruff check src/

# Build documentation
cd docs
make html
```

## Codebase Structure

```
bioquik/
├── src/bioquik/          # Source code
│   ├── __init__.py       # Package exports
│   ├── cli.py            # CLI interface
│   ├── processor.py      # Parallel processing
│   ├── fasta_worker.py   # Single-file processing
│   ├── fmindex.py        # FM-index implementation
│   ├── wavelettree.py    # Wavelet tree
│   ├── motifs.py         # Pattern expansion
│   ├── reports.py        # Report generation
│   ├── plotter.py        # Visualization
│   └── validate.py       # Input validation
├── tests/                # Test suite
├── docs/                 # Documentation
├── pyproject.toml        # Project configuration
└── README.md             # User-facing README
```

## Key Design Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- **CLI**: User interface only
- **Processor**: Orchestration only
- **FASTA Worker**: File processing only
- **FM-Index**: Data structure only

### 2. Stateless Functions
Worker functions are stateless to enable easy parallelization:
```python
# Good: Stateless
def process_fasta_file(fasta_path, pattern_to_motifs, out_dir):
    # No shared state
    pass

# Bad: Stateful
class Processor:
    def __init__(self):
        self.cache = {}  # Shared state
```

### 3. Process-Based Parallelism
Uses `ProcessPoolExecutor` instead of threads:
- Bypasses Python's GIL
- True parallelism for CPU-bound tasks
- No synchronization needed (stateless workers)

### 4. Early Validation
Validate inputs before expensive operations:
```python
# Validate before processing
validate_patterns(patterns)
validate_dir(seq_dir, "sequence")
# Then process
run_count(...)
```

## Core Algorithms

### FM-Index Construction

```python
# Simplified construction flow
def build_fm_index(seq: str):
    # 1. Add sentinel
    seq += "$"
    
    # 2. Build suffix array (O(n log n))
    sa = divsufsort(seq.encode())
    
    # 3. Build BWT
    bwt = [seq[sa[i] - 1] for i in range(len(sa))]
    
    # 4. Build C-table (cumulative counts)
    C = compute_c_table(bwt)
    
    # 5. Build wavelet tree
    wt = WaveletTree(bwt, alphabet)
    
    return FMIndex(seq, sa, bwt, C, wt)
```

### Backward Search

```python
def backward_search(fm: FMIndex, pattern: bytes):
    lo, hi = 0, len(fm.seq)
    
    # Process pattern right-to-left
    for symbol in reversed(pattern):
        # Narrow range using C-table and rank
        lo = fm.C[symbol] + fm.wt.rank(symbol, lo)
        hi = fm.C[symbol] + fm.wt.rank(symbol, hi)
        
        if lo >= hi:
            return 0, 0  # No matches
    
    return lo, hi  # Range size = count
```

### Pattern Expansion

```python
def expand_pattern(pattern: str):
    # Split at CG anchor
    pre, _, post = pattern.partition("CG")
    
    # Count wildcards
    pre_wildcards = pre.count("*")
    post_wildcards = post.count("*")
    
    # Generate all combinations
    motifs = []
    for pre_seq in product("ACGT", repeat=pre_wildcards):
        for post_seq in product("ACGT", repeat=post_wildcards):
            motifs.append(f"{''.join(pre_seq)}CG{''.join(post_seq)}")
    
    return sorted(set(motifs))
```

## Adding New Features

### Adding a New Pattern Type

1. **Extend `motifs.py`**:
```python
def expand_custom_pattern(pattern: str) -> List[str]:
    # Your expansion logic
    if pattern.startswith("REGEX:"):
        # Handle regex patterns
        return expand_regex_pattern(pattern[6:])
    # Fall back to wildcard expansion
    return expand_wildcard_pattern(pattern)
```

2. **Update `build_pattern_to_motifs()`**:
```python
def build_pattern_to_motifs(patterns: List[str]) -> Dict[str, List[str]]:
    mapping = {}
    for pattern in patterns:
        if pattern.startswith("REGEX:"):
            motifs = expand_custom_pattern(pattern)
        else:
            motifs = expand_wildcard_pattern(pattern)
        mapping[pattern] = motifs
    return mapping
```

3. **Add tests**:
```python
# tests/test_motifs.py
def test_custom_pattern():
    motifs = expand_custom_pattern("REGEX:AC.G")
    assert "ACCG" in motifs
    assert "ACGG" in motifs
```

### Adding a New Output Format

1. **Extend `reports.py`**:
```python
def write_xml_summary(df: pd.DataFrame, out_dir: Path) -> None:
    # Generate XML output
    xml_content = generate_xml(df)
    (out_dir / "combined_counts.xml").write_text(xml_content)
```

2. **Add CLI option**:
```python
# In cli.py
@app.command()
def count(
    ...
    xml_out: bool = typer.Option(False, help="Also write XML summary"),
):
    ...
    if xml_out:
        write_xml_summary(df_all, out_dir)
```

3. **Add tests**:
```python
# tests/test_reports.py
def test_xml_output():
    df = create_test_dataframe()
    write_xml_summary(df, tmp_path)
    assert (tmp_path / "combined_counts.xml").exists()
```

### Adding a New Counting Strategy

1. **Extend `fasta_worker.py`**:
```python
def _count_maximal(fm: FMIndex, motif: bytes) -> int:
    """Count only maximal matches (not contained in longer matches)."""
    positions = fm.locate(motif)
    # Filter out positions that are contained in longer matches
    return len(filter_maximal(positions, motif))
```

2. **Update `process_fasta_file()`**:
```python
def process_fasta_file(
    fasta_path: Path,
    pattern_to_motifs: Dict[str, List[str]],
    *,
    counting_strategy: str = "non_overlapping",
    ...
):
    ...
    if counting_strategy == "maximal":
        count = _count_maximal(fm, motif.encode())
    elif counting_strategy == "non_overlapping":
        count = _count_in_fm(fm, motif.encode(), allow_overlap=False)
    ...
```

3. **Add CLI option**:
```python
counting_strategy: str = typer.Option(
    "non_overlapping",
    help="Counting strategy: non_overlapping, overlapping, or maximal"
)
```

## Testing Strategy

### Unit Tests
Test each module independently:
```python
# tests/test_fmindex.py
def test_fm_index_count():
    fm = FMIndex("ACGTACGT")
    assert fm.count(b"ACG") == 2

def test_fm_index_locate():
    fm = FMIndex("ACGTACGT")
    assert fm.locate(b"ACG") == [0, 4]
```

### Integration Tests
Test end-to-end workflows:
```python
# tests/test_cli.py
def test_cli_count_command(tmp_path):
    # Create test FASTA file
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(">seq1\nACGTACGT\n")
    
    # Run CLI command
    result = runner.invoke(app, [
        "count",
        "--patterns", "*CG*",
        "--seq-dir", str(tmp_path),
        "--out-dir", str(tmp_path / "results")
    ])
    
    assert result.exit_code == 0
    assert (tmp_path / "results" / "test_motif_counts.csv").exists()
```

### Performance Tests
Benchmark critical operations:
```python
# tests/test_performance.py
def test_fm_index_construction_time(benchmark):
    seq = "A" * 1000000
    result = benchmark(FMIndex, seq)
    assert result is not None
```

## Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Profile Performance
```python
import cProfile
cProfile.run('process_fasta_file("large.fasta", mapping)')
```

### Debug FM-Index
```python
fm = FMIndex(seq)
print(f"BWT: {fm.bwt}")
print(f"C-table: {fm.C}")
print(f"SA samples: {fm.sa_samples}")
```

### Debug Pattern Expansion
```python
from bioquik.motifs import build_pattern_to_motifs
mapping = build_pattern_to_motifs(["*CG*"])
print(f"Pattern mapping: {mapping}")
```

## Code Style

### Formatting
- Use `ruff` for linting and formatting
- Follow PEP 8 style guide
- Use type hints for all functions

### Docstrings
Use Google-style docstrings:
```python
def process_fasta_file(
    fasta_path: Path,
    pattern_to_motifs: Dict[str, List[str]],
) -> str:
    """Process a single FASTA file and count motifs.
    
    Args:
        fasta_path: Path to FASTA file
        pattern_to_motifs: Mapping from patterns to motif lists
        
    Returns:
        Path to output CSV file
        
    Raises:
        FileNotFoundError: If FASTA file doesn't exist
    """
    ...
```

### Type Hints
Always use type hints:
```python
from typing import List, Dict, Optional

def count_motifs(
    patterns: List[str],
    seq: str,
    allow_overlap: bool = False
) -> Dict[str, int]:
    ...
```

## Common Pitfalls

### 1. Memory Issues with Large Files
**Problem**: Loading entire FASTA file into memory
**Solution**: Consider streaming for very large files (future enhancement)

### 2. GIL Limitations
**Problem**: Using threads instead of processes
**Solution**: Always use `ProcessPoolExecutor` for CPU-bound tasks

### 3. Overlapping Counts
**Problem**: Counting overlapping motifs incorrectly
**Solution**: Use `locate()` and filter positions, or use `allow_overlap=False`

### 4. Pattern Validation
**Problem**: Not validating patterns before expansion
**Solution**: Always validate patterns contain 'CG' anchor

## Performance Optimization

### Profile First
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# Your code
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Common Optimizations
1. **Index Caching**: Cache FM-indexes for repeated queries
2. **Batch Queries**: Process multiple motifs in one pass
3. **Memory Mapping**: Use memory-mapped files for large sequences
4. **Early Termination**: Stop searching if pattern can't match

## Contributing

### Workflow
1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and add tests
4. Run tests: `pytest tests/`
5. Run linter: `ruff check src/`
6. Commit: `git commit -m "Add feature X"`
7. Push: `git push origin feature/my-feature`
8. Create pull request

### Commit Messages
Follow conventional commits:
- `feat: Add new pattern type`
- `fix: Correct overlap counting`
- `docs: Update architecture guide`
- `test: Add performance benchmarks`

### Pull Request Checklist
- [ ] Tests pass
- [ ] Linter passes
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Docstrings added
- [ ] Changelog updated

## Resources

### Internal Documentation
- `ARCHITECTURE.md`: System architecture
- `MODULES.md`: Module reference
- `docs/source/architecture.md`: Detailed architecture guide

### External Resources
- [FM-Index Paper](https://people.unipmn.it/manzini/papers/focs00.pdf)
- [Wavelet Trees](https://www.dcc.uchile.cl/~gnavarro/ps/survey12.pdf)
- [Suffix Arrays](https://web.stanford.edu/~mjkay/gusfield.pdf)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Rajkanwars15/bioquik/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Rajkanwars15/bioquik/discussions)
- **Email**: rajkanwars15@outlook.com
