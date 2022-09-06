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


