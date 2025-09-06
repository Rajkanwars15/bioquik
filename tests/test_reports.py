import json
import pandas as pd
from pathlib import Path


from bioquik.reports import combine_csv, write_summary

def make_csv(path: Path, rows):
    path.write_text(pd.DataFrame(rows).to_csv(index=False))

def test_combine_csv(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    make_csv(out / "a_motif_counts.csv", [
        {"Pattern": "p", "Motif": "M1", "Count": 2},
    ])
    make_csv(out / "b_motif_counts.csv", [
        {"Pattern": "p", "Motif": "M2", "Count": 3},
    ])

    df = combine_csv(out)
    # should have two rows
    assert set(df["Motif"]) == {"M1", "M2"}
    assert df["Count"].tolist() == [2, 3]

def test_write_summary_csv_and_json(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    df = pd.DataFrame([
        {"Pattern": "p", "Motif": "M1", "Count": 2},
        {"Pattern": "p", "Motif": "M1", "Count": 3},
    ])
    write_summary(df, out, json_out=True)

    # CSV exists
    assert (out / "combined_counts.csv").exists()
    # JSON exists and sums correctly
    txt = (out / "combined_counts.json").read_text()
    data = json.loads(txt)
    assert data == {"M1": 5}
