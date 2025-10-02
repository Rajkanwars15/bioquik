from pathlib import Path
import json
import pandas as pd


def combine_csv(out_dir: Path) -> pd.DataFrame:
    """
    Read all *_motif_counts.csv in out_dir and concatenate in sorted order.
    """
    csvs = sorted(out_dir.glob("*_motif_counts.csv"))
    return pd.concat((pd.read_csv(f) for f in csvs), ignore_index=True)


def write_summary(
    df: pd.DataFrame,
    out_dir: Path,
    json_out: bool = False,
) -> None:
    """
    Always write combined_counts.csv.  Optionally write JSON summary.
    """
    csv_path = out_dir / "combined_counts.csv"
    df.to_csv(csv_path, index=False)

    if json_out:
        summary = df.groupby("Motif")["Count"].sum().to_dict()
        (out_dir / "combined_counts.json").write_text(json.dumps(summary, indent=2))
