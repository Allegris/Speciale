import one_hot_encoding as bv
import tracemalloc



# starting the monitoring
tracemalloc.start()


# Words "mis sis sip pi$"
x = "mississippi$"
n = len(x)
alpha = bv.get_alphabet(x) #["$", "i", "m", "p", "s"]
d = bv.one_hot_encoding(x, alpha)
ranks = bv.preprocess_rank_one_hot(d, n, alpha)


def test_mississippi_m_0():
	assert bv.rank_one_hot(ranks, d, n, "m", 0) == 0

def test_mississippi_m_12():
	assert bv.rank_one_hot(ranks, d, n, "m", 12) == 1

def test_mississippi_i_1():
	assert bv.rank_one_hot(ranks, d, n, "i", 1) == 0

def test_mississippi_i_2():
	assert bv.rank_one_hot(ranks, d, n, "i", 2) == 1

def test_mississippi_i_3():
	assert bv.rank_one_hot(ranks, d, n, "i", 3) == 1

def test_mississippi_i_4():
	assert bv.rank_one_hot(ranks, d, n, "i", 4) == 1

def test_mississippi_i_5():
	assert bv.rank_one_hot(ranks, d, n, "i", 5) == 2

def test_mississippi_i_10():
	assert bv.rank_one_hot(ranks, d, n, "i", 10) == 3

def test_mississippi_i_11():
	assert bv.rank_one_hot(ranks, d, n, "i", 11) == 4

def test_mississippi_sentinel_11():
	assert bv.rank_one_hot(ranks, d, n, "$", 11) == 0

def test_mississippi_sentinel_12():
	assert bv.rank_one_hot(ranks, d, n, "$", 12) == 1

def test_mississippi_s_6():
	assert bv.rank_one_hot(ranks, d, n, "s", 6) == 3


# Words "mis sis sip pii $" (the rank of last non-full word is not calculated - must scan)
x2 = "mississippii$"
n2 = len(x2)
d2 = bv.one_hot_encoding(x2, alpha)
ranks2 = bv.preprocess_rank_one_hot(d2, n2, alpha)

def test_mississippii_sentinel_13():
	assert bv.rank_one_hot(ranks2, d2, n2, "$", 13) == 1

def test_mississippii_i_13():
	assert bv.rank_one_hot(ranks2, d2, n2, "i", 13) == 5

def test_mississippii_i_12():
	assert bv.rank_one_hot(ranks2, d2, n2, "i", 12) == 5

def test_mississippii_i_11():
	assert bv.rank_one_hot(ranks2, d2, n2, "i", 11) == 4

def test_mississippii_i_10():
	assert bv.rank_one_hot(ranks2, d2, n2, "i", 10) == 3

def test_mississippii_i_9():
	assert bv.rank_one_hot(ranks2, d2, n2, "i", 9) == 3



dna = "AGTCCTGAANCTGAGCCTTNAGG"
dna_n = len(dna)
dna_alpha = bv.get_alphabet(dna) #["A", "C", "G", "N", "T"]
dna_d = bv.one_hot_encoding(dna, dna_alpha)
dna_ranks = bv.preprocess_rank_one_hot(dna_d, dna_n, dna_alpha)

def test_dna_a_0():
	assert bv.rank_one_hot(dna_ranks, dna_d, dna_n, "A", 0) == 0

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


big_a = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
big_a_n = len(big_a)
big_a_alpha = bv.get_alphabet(big_a) #["A", "C", "G", "N", "T"]
big_a_d = bv.one_hot_encoding(big_a, big_a_alpha)
big_a_ranks = bv.preprocess_rank_one_hot(big_a_d, big_a_n, big_a_alpha)


# displaying the memory
print(tracemalloc.get_traced_memory())

# stopping the library
tracemalloc.stop()
