import wavelet_tree_level_order_pointers as lop
from shared import huffman_codes
import tracemalloc


x = "mississippi"
codes = huffman_codes(x)
n = len(x)
wt, pointers = lop.wavelet_tree(x, codes)
ranks = lop.preprocess_all_tree_node_ranks(wt, n, pointers)

def test_mississippi_m_0():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "m", 0) == 0

def test_mississippi_m_12():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "m", 11) == 1

def test_mississippi_i_1():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 1) == 0

def test_mississippi_i_2():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 2) == 1

def test_mississippi_i_3():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 3) == 1

def test_mississippi_i_4():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 4) == 1

def test_mississippi_i_5():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 5) == 2

def test_mississippi_i_10():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 10) == 3

def test_mississippi_i_11():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 11) == 4

def test_mississippi_s_6():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "s", 6) == 3




x2 = "mississippii"
codes2 = huffman_codes(x2)
n2 = len(x2)
wt2, pointers2 = lop.wavelet_tree(x2, codes2)
ranks2 = lop.preprocess_all_tree_node_ranks(wt2, n2, pointers2)

def test_mississippii_i_11():
		assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 11) == 4

def test_mississippii_i_10():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 10) == 3

def test_mississippii_i_9():
	assert lop.rank_query(wt, n, pointers, ranks, codes, "i", 9) == 3




dna = "AGTCCTGAANCTGAGCCTTNAGG"
dna_codes = huffman_codes(dna)
dna_n = len(dna)
dna_wt, dna_pointers = lop.wavelet_tree(dna, dna_codes)
dna_ranks = lop.preprocess_all_tree_node_ranks(dna_wt, dna_n, dna_pointers)


def test_dna_a_0():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "A", 0) == 0

def test_dna_a_1():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "A", 1) == 1

def test_dna_c_5():
		assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "C", 5) == 2

def test_dna_G_21():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "G", 21) == 4

def test_dna_G_22():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "G", 22) == 5

def test_dna_G_23():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "G", 23) == 6

def test_dna_C_4():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "C", 4) == 1

def test_dna_C_5():
	assert lop.rank_query(dna_wt, dna_n, dna_pointers, dna_ranks, dna_codes, "C", 5) == 2




big = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
big_codes = huffman_codes(big)
big_n = len(big)
big_wt, big_pointers = lop.wavelet_tree(big, big_codes)
big_ranks = lop.preprocess_all_tree_node_ranks(big_wt, big_n, big_pointers)


def test_big_a_0():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "A", 0) == 0

def test_big_a_1():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "A", 1) == 1

def test_big_b_1():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "B", 1) == 0

def test_big_b_2():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "B", 2) == 1

def test_big_z_25():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "Z", 25) == 0

def test_big_z_26():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "Z", 26) == 1

def test_big_9_37():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "9", 37) == 0

def test_big_9_38():
	assert lop.rank_query(big_wt, big_n, big_pointers, big_ranks, big_codes, "9", 38) == 1




