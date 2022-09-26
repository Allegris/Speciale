import wavelet_tree_level_order as lo
from shared import huffman_codes
import tracemalloc



# starting the monitoring
tracemalloc.start()


x = "mississippi"
n = len(x)
codes = huffman_codes(x)
wt = lo.wavelet_tree(x, codes)
ranks = lo.preprocess_all_tree_node_ranks(wt, n)


def test_mississippi_m_0():
	assert lo.rank_query(wt, n, ranks, codes, "m", 0) == 0

def test_mississippi_m_12():
	assert lo.rank_query(wt, n, ranks, codes, "m", 11) == 1

def test_mississippi_i_1():
	assert lo.rank_query(wt, n, ranks, codes, "i", 1) == 0

def test_mississippi_i_2():
	assert lo.rank_query(wt, n, ranks, codes, "i", 2) == 1

def test_mississippi_i_3():
	assert lo.rank_query(wt, n, ranks, codes, "i", 3) == 1

def test_mississippi_i_4():
	assert lo.rank_query(wt, n, ranks, codes, "i", 4) == 1

def test_mississippi_i_5():
	assert lo.rank_query(wt, n, ranks, codes, "i", 5) == 2

def test_mississippi_i_10():
	assert lo.rank_query(wt, n, ranks, codes, "i", 10) == 3

def test_mississippi_i_11():
	assert lo.rank_query(wt, n, ranks, codes, "i", 11) == 4

def test_mississippi_s_6():
	assert lo.rank_query(wt, n, ranks, codes, "s", 6) == 3





x2 = "mississippii"
n2 = len(x2)
codes2 = huffman_codes(x2)
wt2 = lo.wavelet_tree(x2, codes2)
ranks2 = lo.preprocess_all_tree_node_ranks(wt2, n2)

def test_mississippii_i_12():
	assert lo.rank_query(wt2, n2, ranks2, codes2, "i", 12) == 5

def test_mississippii_i_11():
	assert lo.rank_query(wt2, n2, ranks2, codes2, "i", 11) == 4

def test_mississippii_i_10():
	assert lo.rank_query(wt2, n2, ranks2, codes2, "i", 10) == 3

def test_mississippii_i_9():
	assert lo.rank_query(wt2, n2, ranks2, codes2, "i", 9) == 3




dna = "AGTCCTGAANCTGAGCCTTNAGG"
dna_n = len(dna)
dna_codes = huffman_codes(dna)
dna_wt = lo.wavelet_tree(dna, dna_codes)
dna_ranks = lo.preprocess_all_tree_node_ranks(dna_wt, dna_n)


def test_dna_a_0():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "A", 0) == 0

def test_dna_a_1():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "A", 1) == 1

def test_dna_c_5():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "C", 5) == 2

def test_dna_G_21():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "G", 21) == 4

def test_dna_G_22():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "G", 22) == 5

def test_dna_G_23():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "G", 23) == 6

def test_dna_C_4():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "C", 4) == 1

def test_dna_C_5():
	assert lo.rank_query(dna_wt, dna_n, dna_ranks, dna_codes, "C", 5) == 2


big = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
big_n = len(big)
big_codes = huffman_codes(big)
big_wt = lo.wavelet_tree(big, big_codes)
big_ranks = lo.preprocess_all_tree_node_ranks(big_wt, big_n)


def test_big_a_0():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "A", 0) == 0

def test_big_a_1():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "A", 1) == 1

def test_big_b_1():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "B", 1) == 0

def test_big_b_2():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "B", 2) == 1

def test_big_z_25():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "Z", 25) == 0

def test_big_z_26():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "Z", 26) == 1

def test_big_9_37():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "9", 37) == 0

def test_big_9_38():
	assert lo.rank_query(big_wt, big_n, big_ranks, big_codes, "9", 38) == 1


# displaying the memory
print(tracemalloc.get_traced_memory())

# stopping the library
tracemalloc.stop()
