import wavelet_tree as wt

x = "mississippi"
root = wt.WaveletTreeNode(x, 0, None)


def test_mississippi_m_0():
	assert wt.rank(root, "m", 0) == 0

def test_mississippi_m_11():
	assert wt.rank(root, "m", 11) == 1

def test_mississippi_i_1():
	assert wt.rank(root, "i", 1) == 0

def test_mississippi_i_2():
	assert wt.rank(root, "i", 2) == 1

def test_mississippi_i_3():
	assert wt.rank(root, "i", 3) == 1

def test_mississippi_i_4():
	assert wt.rank(root, "i", 4) == 1

def test_mississippi_i_5():
	assert wt.rank(root, "i", 5) == 2

def test_mississippi_i_10():
	assert wt.rank(root, "i", 10) == 3

def test_mississippi_i_11():
	assert wt.rank(root, "i", 11) == 4

def test_mississippi_s_6():
	assert wt.rank(root, "s", 6) == 3

def test_mississippi_p_8():
	assert wt.rank(root, "p", 8) == 0

def test_mississippi_p_9():
	assert wt.rank(root, "p", 9) == 1

def test_mississippi_p_10():
	assert wt.rank(root, "p", 10) == 2


x2 = "mississippii$"
root2 = wt.WaveletTreeNode(x2, 0, None)

def test_mississippii_sentinel_13():
	assert wt.rank(root2, "$", 13) == 1

def test_mississippii_i_13():
	assert wt.rank(root2, "i", 13) == 5

def test_mississippii_i_12():
	assert wt.rank(root2, "i", 12) == 5

def test_mississippii_i_11():
	assert wt.rank(root2, "i", 11) == 4

def test_mississippii_i_10():
	assert wt.rank(root2, "i", 10) == 3

def test_mississippii_i_9():
	assert wt.rank(root2, "i", 9) == 3



x3 = "AGTCCTGAANCTGAGCCTTNAGG"
root3 = wt.WaveletTreeNode(x3, 0, None)


def test_dna_a_0():
	assert wt.rank(root3, "A", 0) == 0

def test_dna_a_1():
	assert wt.rank(root3, "A", 1) == 1

def test_dna_c_5():
	assert wt.rank(root3, "C", 5) == 2

def test_dna_G_21():
	assert wt.rank(root3, "G", 21) == 4

def test_dna_G_22():
	assert wt.rank(root3, "G", 22) == 5

def test_dna_G_23():
	assert wt.rank(root3, "G", 23) == 6

def test_dna_C_4():
	assert wt.rank(root3, "C", 4) == 1

def test_dna_C_5():
	assert wt.rank(root3, "C", 5) == 2



x4 = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
root4 = wt.WaveletTreeNode(x4, 0, None)


def test_big_a_0():
	assert wt.rank(root4, "A", 0) == 0

def test_big_a_1():
	assert wt.rank(root4, "A", 1) == 1

def test_big_b_1():
	assert wt.rank(root4, "B", 1) == 0

def test_big_b_2():
	assert wt.rank(root4, "B", 2) == 1

def test_big_z_25():
	assert wt.rank(root4, "Z", 25) == 0

def test_big_z_26():
	assert wt.rank(root4, "Z", 26) == 1

def test_big_9_37():
	assert wt.rank(root4, "9", 37) == 0

def test_big_9_38():
	assert wt.rank(root4, "9", 38) == 1





