from wavelet_tree import wavelet_tree

x = "mississippi"
root = wavelet_tree(x)


def test_mississippi_m_0():
	assert root.rank("m", 0) == 0

def test_mississippi_m_11():
	assert root.rank("m", 11) == 1

def test_mississippi_i_1():
	assert root.rank("i", 1) == 0

def test_mississippi_i_2():
	assert root.rank("i", 2) == 1

def test_mississippi_i_3():
	assert root.rank("i", 3) == 1

def test_mississippi_i_4():
	assert root.rank("i", 4) == 1

def test_mississippi_i_5():
	assert root.rank("i", 5) == 2

def test_mississippi_i_10():
	assert root.rank("i", 10) == 3

def test_mississippi_i_11():
	assert root.rank("i", 11) == 4

def test_mississippi_s_6():
	assert root.rank("s", 6) == 3

def test_mississippi_p_8():
	assert root.rank("p", 8) == 0

def test_mississippi_p_9():
	assert root.rank("p", 9) == 1

def test_mississippi_p_10():
	assert root.rank("p", 10) == 2


x2 = "mississippii$"
root2 = wavelet_tree(x2)

def test_mississippii_sentinel_13():
	assert root2.rank("$", 13) == 1

def test_mississippii_i_13():
	assert root2.rank("i", 13) == 5

def test_mississippii_i_12():
	assert root2.rank("i", 12) == 5

def test_mississippii_i_11():
	assert root2.rank("i", 11) == 4

def test_mississippii_i_10():
	assert root2.rank("i", 10) == 3

def test_mississippii_i_9():
	assert root2.rank("i", 9) == 3



x3 = "AGTCCTGAANCTGAGCCTTNAGG"
root3 = wavelet_tree(x3)


def test_dna_a_0():
	assert root3.rank("A", 0) == 0

def test_dna_a_1():
	assert root3.rank("A", 1) == 1

def test_dna_c_5():
	assert root3.rank("C", 5) == 2

def test_dna_G_21():
	assert root3.rank("G", 21) == 4

def test_dna_G_22():
	assert root3.rank("G", 22) == 5

def test_dna_G_23():
	assert root3.rank("G", 23) == 6

def test_dna_C_4():
	assert root3.rank("C", 4) == 1

def test_dna_C_5():
	assert root3.rank("C", 5) == 2



x4 = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
root4 = wavelet_tree(x4)


def test_big_a_0():
	assert root4.rank("A", 0) == 0

def test_big_a_1():
	assert root4.rank("A", 1) == 1

def test_big_b_1():
	assert root4.rank("B", 1) == 0

def test_big_b_2():
	assert root4.rank("B", 2) == 1

def test_big_z_25():
	assert root4.rank("Z", 25) == 0

def test_big_z_26():
	assert root4.rank("Z", 26) == 1

def test_big_9_37():
	assert root4.rank("9", 37) == 0

def test_big_9_38():
	assert root4.rank("9", 38) == 1





