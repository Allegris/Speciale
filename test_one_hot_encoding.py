import one_hot_encoding as oh


# Words "mis sis sip pi$"
x = "mississippi$"
ohe = oh.one_hot_encoding(x)
ranks = oh.preprocess_ranks(ohe, len(x))


def test_mississippi_m_0():
	assert oh.rank_query(ohe, ranks, "m", 0) == 0

def test_mississippi_m_12():
	assert oh.rank_query(ohe, ranks, "m", 12) == 1

def test_mississippi_i_1():
	assert oh.rank_query(ohe, ranks, "i", 1) == 0

def test_mississippi_i_2():
	assert oh.rank_query(ohe, ranks, "i", 2) == 1

def test_mississippi_i_3():
	assert oh.rank_query(ohe, ranks, "i", 3) == 1

def test_mississippi_i_4():
	assert oh.rank_query(ohe, ranks, "i", 4) == 1

def test_mississippi_i_5():
	assert oh.rank_query(ohe, ranks, "i", 5) == 2

def test_mississippi_i_10():
	assert oh.rank_query(ohe, ranks, "i", 10) == 3

def test_mississippi_i_11():
	assert oh.rank_query(ohe, ranks, "i", 11) == 4

def test_mississippi_sentinel_11():
	assert oh.rank_query(ohe, ranks, "$", 11) == 0

def test_mississippi_sentinel_12():
	assert oh.rank_query(ohe, ranks, "$", 12) == 1

def test_mississippi_s_6():
	assert oh.rank_query(ohe, ranks, "s", 6) == 3


# Words "mis sis sip pii $" (the rank of last non-full word is not calculated - must scan)
x2 = "mississippii$"
ohe2 = oh.one_hot_encoding(x2)
ranks2 = oh.preprocess_ranks(ohe2, len(x2))

def test_mississippii_sentinel_13():
	assert oh.rank_query(ohe2, ranks2, "$", 13) == 1

def test_mississippii_i_13():
	assert oh.rank_query(ohe2, ranks2, "i", 13) == 5

def test_mississippii_i_12():
	assert oh.rank_query(ohe2, ranks2, "i", 12) == 5

def test_mississippii_i_11():
	assert oh.rank_query(ohe2, ranks2, "i", 11) == 4

def test_mississippii_i_10():
	assert oh.rank_query(ohe2, ranks2, "i", 10) == 3

def test_mississippii_i_9():
	assert oh.rank_query(ohe2, ranks2, "i", 9) == 3



dna = "AGTCCTGAANCTGAGCCTTNAGG"
dna_ohe = oh.one_hot_encoding(dna)
dna_ranks = oh.preprocess_ranks(dna_ohe, len(dna))

def test_dna_a_0():
	assert oh.rank_query(dna_ohe, dna_ranks, "A", 0) == 0

def test_dna_a_1():
	assert oh.rank_query(dna_ohe, dna_ranks, "A", 1) == 1

def test_dna_c_5():
	assert oh.rank_query(dna_ohe, dna_ranks, "C", 5) == 2

def test_dna_G_21():
	assert oh.rank_query(dna_ohe, dna_ranks, "G", 21) == 4

def test_dna_G_22():
	assert oh.rank_query(dna_ohe, dna_ranks, "G", 22) == 5

def test_dna_G_23():
	assert oh.rank_query(dna_ohe, dna_ranks, "G", 23) == 6

def test_dna_C_4():
	assert oh.rank_query(dna_ohe, dna_ranks, "C", 4) == 1

def test_dna_C_5():
	assert oh.rank_query(dna_ohe, dna_ranks, "C", 5) == 2


big = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
big_ohe = oh.one_hot_encoding(big)
big_ranks = oh.preprocess_ranks(big_ohe, len(big))


def test_big_a_0():
	assert oh.rank_query(big_ohe, big_ranks, "A", 0) == 0

def test_big_a_1():
	assert oh.rank_query(big_ohe, big_ranks, "A", 1) == 1

def test_big_b_1():
	assert oh.rank_query(big_ohe, big_ranks, "B", 1) == 0

def test_big_b_2():
	assert oh.rank_query(big_ohe, big_ranks, "B", 2) == 1

def test_big_z_25():
	assert oh.rank_query(big_ohe, big_ranks, "Z", 25) == 0

def test_big_z_26():
	assert oh.rank_query(big_ohe, big_ranks, "Z", 26) == 1

def test_big_9_37():
	assert oh.rank_query(big_ohe, big_ranks, "9", 37) == 0

def test_big_9_38():
	assert oh.rank_query(big_ohe, big_ranks, "9", 38) == 1

