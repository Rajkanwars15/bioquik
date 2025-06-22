from pathlib import Path
from typer.testing import CliRunner

import bioquik.cli

runner = CliRunner()

def test_cli(tmp_path: Path):
    fasta = tmp_path / "a.fasta"
    fasta.write_text(">seq\nGATTACAGATTACA")

    res = runner.invoke(bioquik.cli.app, [
        "count",
        "--patterns", "****CG****",
        "--seq-dir", str(tmp_path),
    ])

    if res.exit_code != 0:
        print("\n--- CLI OUTPUT ---\n")
        print(res.output)

    assert res.exit_code == 0
