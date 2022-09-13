import one_hot_encoding as bv
from shared import get_alphabet
import tracemalloc



# starting the monitoring
tracemalloc.start()


# Words "mis sis sip pi$"
x = "mississippi$"
n = len(x)
alpha = get_alphabet(x) #["$", "i", "m", "p", "s"]
d = bv.one_hot_encoding(x, alpha)
ranks = bv.preprocess_ranks(d, n, alpha)


def test_mississippi_m_0():
	assert bv.rank_query(ranks, d, n, "m", 0) == 0

def test_mississippi_m_12():
	assert bv.rank_query(ranks, d, n, "m", 12) == 1

def test_mississippi_i_1():
	assert bv.rank_query(ranks, d, n, "i", 1) == 0

def test_mississippi_i_2():
	assert bv.rank_query(ranks, d, n, "i", 2) == 1

def test_mississippi_i_3():
	assert bv.rank_query(ranks, d, n, "i", 3) == 1

def test_mississippi_i_4():
	assert bv.rank_query(ranks, d, n, "i", 4) == 1

def test_mississippi_i_5():
	assert bv.rank_query(ranks, d, n, "i", 5) == 2

def test_mississippi_i_10():
	assert bv.rank_query(ranks, d, n, "i", 10) == 3

def test_mississippi_i_11():
	assert bv.rank_query(ranks, d, n, "i", 11) == 4

def test_mississippi_sentinel_11():
	assert bv.rank_query(ranks, d, n, "$", 11) == 0

def test_mississippi_sentinel_12():
	assert bv.rank_query(ranks, d, n, "$", 12) == 1

def test_mississippi_s_6():
	assert bv.rank_query(ranks, d, n, "s", 6) == 3


# Words "mis sis sip pii $" (the rank of last non-full word is not calculated - must scan)
x2 = "mississippii$"
n2 = len(x2)
d2 = bv.one_hot_encoding(x2, alpha)
ranks2 = bv.preprocess_ranks(d2, n2, alpha)

def test_mississippii_sentinel_13():
	assert bv.rank_query(ranks2, d2, n2, "$", 13) == 1

def test_mississippii_i_13():
	assert bv.rank_query(ranks2, d2, n2, "i", 13) == 5

def test_mississippii_i_12():
	assert bv.rank_query(ranks2, d2, n2, "i", 12) == 5

def test_mississippii_i_11():
	assert bv.rank_query(ranks2, d2, n2, "i", 11) == 4

def test_mississippii_i_10():
	assert bv.rank_query(ranks2, d2, n2, "i", 10) == 3

def test_mississippii_i_9():
	assert bv.rank_query(ranks2, d2, n2, "i", 9) == 3



dna = "AGTCCTGAANCTGAGCCTTNAGG"
dna_n = len(dna)
dna_alpha = get_alphabet(dna) #["A", "C", "G", "N", "T"]
dna_d = bv.one_hot_encoding(dna, dna_alpha)
dna_ranks = bv.preprocess_ranks(dna_d, dna_n, dna_alpha)

def test_dna_a_0():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "A", 0) == 0

def test_dna_a_1():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "A", 1) == 1

def test_dna_c_5():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "C", 5) == 2

def test_dna_G_21():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "G", 21) == 4

def test_dna_G_22():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "G", 22) == 5

def test_dna_G_23():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "G", 23) == 6

def test_dna_C_4():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "C", 4) == 1

def test_dna_C_5():
	assert bv.rank_query(dna_ranks, dna_d, dna_n, "C", 5) == 2


big = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
big_n = len(big)
big_alpha = get_alphabet(big) #["A", "C", "G", "N", "T"]
big_d = bv.one_hot_encoding(big, big_alpha)
big_ranks = bv.preprocess_ranks(big_d, big_n, big_alpha)


def test_big_a_0():
	assert bv.rank_query(big_ranks, big_d, big_n, "A", 0) == 0

def test_big_a_1():
	assert bv.rank_query(big_ranks, big_d, big_n, "A", 1) == 1

def test_big_b_1():
	assert bv.rank_query(big_ranks, big_d, big_n, "B", 1) == 0

def test_big_b_2():
	assert bv.rank_query(big_ranks, big_d, big_n, "B", 2) == 1

def test_big_z_25():
	assert bv.rank_query(big_ranks, big_d, big_n, "Z", 25) == 0

def test_big_z_26():
	assert bv.rank_query(big_ranks, big_d, big_n, "Z", 26) == 1

def test_big_9_37():
	assert bv.rank_query(big_ranks, big_d, big_n, "9", 37) == 0

def test_big_9_38():
	assert bv.rank_query(big_ranks, big_d, big_n, "9", 38) == 1



# displaying the memory
print(tracemalloc.get_traced_memory())

# stopping the library
tracemalloc.stop()
