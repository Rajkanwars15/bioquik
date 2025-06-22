from pathlib import Path

import pytest
import typer
from bioquik.validate import validate_patterns, validate_dir


def test_validate_patterns_valid():
    lst = validate_patterns("**CG**,A*CG*")
    assert lst == ["**CG**", "A*CG*"]


def test_validate_patterns_invalid(capsys):
    with pytest.raises(typer.Exit):
        validate_patterns("AAAA")
    captured = capsys.readouterr()
    assert "must include 'CG'" in captured.out


def test_validate_dir_valid(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    # Should not raise
    validate_dir(d, "sequence")


def test_validate_dir_invalid(capsys):
    fake = Path("no_such_dir")
    with pytest.raises(typer.Exit):
        validate_dir(fake, "seq")
    captured = capsys.readouterr()
    assert "directory 'no_such_dir' not found" in captured.out
