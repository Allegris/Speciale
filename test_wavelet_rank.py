import wavelet_tree as wt

x = "mississippi"
root = wt.WaveletTreeNode(x, False)


def test_mississippi_m_0():
	assert wt.rank_query(root, "m", 0) == 0

def test_mississippi_m_11():
	assert wt.rank_query(root, "m", 11) == 1

def test_mississippi_i_1():
	assert wt.rank_query(root, "i", 1) == 0

def test_mississippi_i_2():
	assert wt.rank_query(root, "i", 2) == 1

def test_mississippi_i_3():
	assert wt.rank_query(root, "i", 3) == 1

def test_mississippi_i_4():
	assert wt.rank_query(root, "i", 4) == 1

def test_mississippi_i_5():
	assert wt.rank_query(root, "i", 5) == 2

def test_mississippi_i_10():
	assert wt.rank_query(root, "i", 10) == 3

def test_mississippi_i_11():
	assert wt.rank_query(root, "i", 11) == 4

def test_mississippi_s_6():
	assert wt.rank_query(root, "s", 6) == 3

def test_mississippi_p_8():
	assert wt.rank_query(root, "p", 8) == 0

def test_mississippi_p_9():
	assert wt.rank_query(root, "p", 9) == 1

def test_mississippi_p_10():
	assert wt.rank_query(root, "p", 10) == 2




dna = "AGTCCTGAANCTGAGCCTTNAGG"
dna_root = wt.WaveletTreeNode(dna, False)

def test_dna_a_0():
	assert wt.rank_query(dna_root, "A", 0) == 0
'''
def test_dna_a_1():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "A", 1) == 1

def test_dna_c_5():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "C", 5) == 2

def test_dna_G_21():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "G", 21) == 4

def test_dna_G_22():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "G", 22) == 5

def test_dna_G_23():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "G", 23) == 6

def test_dna_C_4():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "C", 4) == 1

def test_dna_C_5():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "C", 5) == 2

	'''








