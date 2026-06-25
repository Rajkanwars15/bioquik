from bioquik.fmindex import FMIndex


def test_count_simple():
    fm = FMIndex("GATTACA$")
    assert fm.count(b"TA") == 1
    assert fm.count(b"GA") == 1
    assert fm.count(b"TT") == 1
    assert fm.count(b"XYZ") == 0


def test_locate_simple():
    fm = FMIndex("ABCABC")
    positions = sorted(fm.locate(b"BC"))
    assert positions == [1, 4]


def test_locate_no_match():
    fm = FMIndex("GATTACA")
    assert fm.locate(b"XYZ") == []


def test_count_matches_locate_length():
    fm = FMIndex("AAAA")
    pattern = b"AA"
    assert fm.count(pattern) == len(fm.locate(pattern))
