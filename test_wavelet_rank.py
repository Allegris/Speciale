from bitarray import bitarray
import wavelet_tree_new as wt

x = "mississippi"
alpha = wt.get_alphabet(x) # ["i", "m", "p", "s"]
#global codes
#codes = {letter: bitarray() for letter in alpha}

root = wt.WaveletTreeNode(x)
#codes = wt. codes


def test_mississippi_m_0():
	print(wt.codes)
	assert wt.rank_query(root, wt.codes, "m", 0) == 0
'''
def test_mississippi_m_11():
	assert wt.rank_query(root, "m", 11) == 1

def test_mississippi_i_1():
	assert wt.rank_query(root, "i", 11) == 0

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
'''

