from bioquik.wavelettree import WaveletTree


def test_rank_basic():
    data = b"ABRACADABRA"
    alphabet = bytes(sorted(set(data)))
    wt = WaveletTree(data, alphabet)
    # count of 'A' in first 5 chars "ABRAC" = 2
    assert wt.rank(ord("A"), 5) == 2
    # count of 'B' in first 4 chars "ABRA" = 1
    assert wt.rank(ord("B"), 4) == 1
    # count of 'R' in full string = 2
    assert wt.rank(ord("R"), len(data)) == 2


def test_rank_zero_position():
    data = b"ACGT"
    alphabet = bytes(sorted(set(data)))
    wt = WaveletTree(data, alphabet)
    for sym in data:
        assert wt.rank(sym, 0) == 0


def test_rank_full_length():
    data = b"AACGT"
    alphabet = bytes(sorted(set(data)))
    wt = WaveletTree(data, alphabet)
    assert wt.rank(ord("A"), len(data)) == 2
    assert wt.rank(ord("C"), len(data)) == 1
    assert wt.rank(ord("G"), len(data)) == 1
    assert wt.rank(ord("T"), len(data)) == 1


def test_rank_single_symbol_alphabet():
    # leaf node path: alphabet of size 1
    data = b"AAAA"
    wt = WaveletTree(data, b"A")
    assert wt.rank(ord("A"), 4) == 4
    assert wt.rank(ord("A"), 2) == 2


def test_rank_sample_rate_accuracy():
    # Results must be identical regardless of sample_rate
    data = b"GATTACAGATTACA"
    alphabet = bytes(sorted(set(data)))
    wt1 = WaveletTree(data, alphabet, sample_rate=1)
    wt32 = WaveletTree(data, alphabet, sample_rate=32)
    for sym in alphabet:
        for i in range(len(data) + 1):
            assert wt1.rank(sym, i) == wt32.rank(sym, i)
