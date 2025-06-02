import pytest
from sequin.fmindex import FMIndex

def test_count_simple():
    fm = FMIndex("GATTACA$")
    assert fm.count(b"TA") == 1
    assert fm.count(b"GA") == 1
    assert fm.count(b"TT") == 1
    assert fm.count(b"XYZ") == 0