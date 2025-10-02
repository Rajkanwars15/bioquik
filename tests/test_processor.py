import pandas as pd
from pathlib import Path


from bioquik.processor import run_count


def dummy_process(f, mapping, out_dir):
    # create a fake CSV per‐file
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{Path(f).stem}_motif_counts.csv"
    pd.DataFrame([{"Pattern": "X", "Motif": "M", "Count": 1}]).to_csv(path, index=False)
    return str(path)


def test_run_count_creates_csvs(tmp_path, monkeypatch):
    # prepare two dummy FASTAs
    seq_dir = tmp_path / "seq"
    seq_dir.mkdir()
    for name in ("a.fasta", "b.fasta"):
        (seq_dir / name).write_text(">seq\nAAAA")

    out_dir = tmp_path / "out"

    # stub out motif expansion & worker
    monkeypatch.setattr(
        "bioquik.processor.build_pattern_to_motifs", lambda pats: {"P": ["M"]}
    )
    monkeypatch.setattr("bioquik.processor.process_fasta_file", dummy_process)

    # run
    run_count(["P"], seq_dir, out_dir, workers=1)

    files = sorted(out_dir.glob("*_motif_counts.csv"))
    assert len(files) == 2
    assert {f.name for f in files} == {"a_motif_counts.csv", "b_motif_counts.csv"}
