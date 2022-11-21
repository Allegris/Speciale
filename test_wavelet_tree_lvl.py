from wavelet_tree_lvl import WaveletTree


x = "mississippi"
wt = WaveletTree(x)

def test_mississippi_m_0():
	assert wt.rank("m", 0) == 0

def test_mississippi_m_12():
	assert wt.rank("m", 11) == 1

def test_mississippi_i_1():
	assert wt.rank("i", 1) == 0

def test_mississippi_i_2():
	assert wt.rank("i", 2) == 1

def test_mississippi_i_3():
	assert wt.rank("i", 3) == 1

def test_mississippi_i_4():
	assert wt.rank("i", 4) == 1

def test_mississippi_i_5():
	assert wt.rank("i", 5) == 2

def test_mississippi_i_10():
	assert wt.rank("i", 10) == 3

def test_mississippi_i_11():
	assert wt.rank("i", 11) == 4

def test_mississippi_s_6():
	assert wt.rank("s", 6) == 3




x2 = "mississippii"
wt2 = WaveletTree(x2)

def test_mississippii_i_11():
		assert wt2.rank("i", 11) == 4

def test_mississippii_i_10():
	assert wt2.rank("i", 10) == 3

def test_mississippii_i_9():
	assert wt2.rank("i", 9) == 3




x3 = "AGTCCTGAANCTGAGCCTTNAGG"
wt3 = WaveletTree(x3)

def test_dna_a_0():
	assert wt3.rank("A", 0) == 0

def test_dna_a_1():
	wt3.rank("A", 1) == 1

def test_dna_c_5():
	wt3.rank("C", 5) == 2

def test_dna_G_21():
	wt3.rank("G", 21) == 4

def test_dna_G_22():
	wt3.rank("G", 22) == 5

def test_dna_G_23():
	wt3.rank("G", 23) == 6

def test_dna_C_4():
	wt3.rank("C", 4) == 1

def test_dna_C_5():
	wt3.rank("C", 5) == 2




x4 = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
wt4 = WaveletTree(x4)


def test_big_a_0():
	wt4.rank("A", 0) == 0

def test_big_a_1():
	wt4.rank("A", 1) == 1

def test_big_b_1():
	wt4.rank("B", 1) == 0

def test_big_b_2():
	wt4.rank("B", 2) == 1

def test_big_z_25():
	wt4.rank("Z", 25) == 0

def test_big_z_26():
	wt4.rank("Z", 26) == 1

def test_big_9_37():
	wt4.rank("9", 37) == 0

def test_big_9_38():
	wt4.rank("9", 38) == 1




