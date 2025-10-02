from pathlib import Path
from typer.testing import CliRunner

import bioquik.cli

runner = CliRunner()


def write_fasta(path: Path, seq: str):
    path.write_text(f">seq\n{seq}")


def test_cli_minimal(tmp_path: Path):
    # minimal run (no JSON, no plot)
    seq_dir = tmp_path / "seq"
    seq_dir.mkdir()
    write_fasta(seq_dir / "a.fasta", "ATCGCGAT")

    res = runner.invoke(
        bioquik.cli.app,
        [
            "count",
            "--patterns",
            "**CG**",
            "--seq-dir",
            str(seq_dir),
            "--out-dir",
            str(tmp_path / "out"),
        ],
    )
    assert res.exit_code == 0
    csv = Path(tmp_path / "out" / "combined_counts.csv")
    assert csv.exists()


def test_cli_json_and_plot(tmp_path):
    seq_dir = tmp_path / "seq"
    seq_dir.mkdir()
    write_fasta(seq_dir / "a.fasta", "ATCGCGAT")

    out_dir = tmp_path / "out"
    res = runner.invoke(
        bioquik.cli.app,
        [
            "count",
            "--patterns",
            "**CG**",
            "--seq-dir",
            str(seq_dir),
            "--out-dir",
            str(out_dir),
            "--json-out",
            "--plot",
        ],
    )
    assert res.exit_code == 0
    assert (out_dir / "combined_counts.csv").exists()
    assert (out_dir / "combined_counts.json").exists()
    assert (out_dir / "motif_distribution.png").exists()
