from pathlib import Path

import pytest
from bioquik.validate import validate_patterns, validate_dir


def test_validate_patterns_valid():
    lst = validate_patterns("**CG**,A*CG*")
    assert lst == ["**CG**", "A*CG*"]


def test_validate_patterns_invalid():
    with pytest.raises(ValueError, match="must include 'CG'"):
        validate_patterns("AAAA")


def test_validate_dir_valid(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    validate_dir(d, "sequence")  # should not raise


def test_validate_dir_invalid():
    with pytest.raises(ValueError, match="directory 'no_such_dir' not found"):
        validate_dir(Path("no_such_dir"), "seq")
