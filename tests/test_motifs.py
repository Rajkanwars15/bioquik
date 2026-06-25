from bioquik.motifs import generate_motifs, build_pattern_to_motifs


def test_generate_motifs_no_wildcard():
    # bare CG with no wildcards — single motif
    result = generate_motifs(["CG"])
    assert result == ["CG"]


def test_generate_motifs_single_wildcard():
    result = generate_motifs(["*CG"])
    assert len(result) == 4
    assert all(m.endswith("CG") for m in result)
    assert sorted(result) == ["ACG", "CCG", "GCG", "TCG"]


def test_generate_motifs_deduplicated():
    # same pattern twice — result must be deduplicated
    result = generate_motifs(["*CG", "*CG"])
    assert result == sorted(set(result))


def test_build_pattern_to_motifs_keys_use_N():
    mapping = build_pattern_to_motifs(["*CG*"])
    assert "NCG N".replace(" ", "") in mapping or "NCGN" in mapping
    # wildcards replaced with N in key
    for key in mapping:
        assert "*" not in key


def test_build_pattern_to_motifs_values():
    mapping = build_pattern_to_motifs(["*CG"])
    key = "NCG"
    assert key in mapping
    assert sorted(mapping[key]) == ["ACG", "CCG", "GCG", "TCG"]
