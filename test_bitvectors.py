import bitvectors as bv

global x
global n
global alpha
global a_size
global d
global ranks



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





