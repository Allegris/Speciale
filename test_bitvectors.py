import bitvectors as bv
'''
global x
global n
global alpha
global a_size
global d
global ranks
'''

# Words "mis sis sip pi$"
x = "mississippi$"
n = len(x)
alpha = ["$", "i", "m", "p", "s"]
a_size = len(alpha)
d = bv.one_hot_encoding(x, n, alpha, a_size)
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
d2 = bv.one_hot_encoding(x2, n2, alpha, a_size)
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



