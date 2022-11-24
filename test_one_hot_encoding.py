from one_hot_encoding import OneHotEncoding

# Words "mis sis sip pi$"
x = "mississippi$"
ohe = OneHotEncoding(x)


def test_mississippi_m_0():
	assert ohe.rank("m", 0) == 0

def test_mississippi_m_12():
	assert ohe.rank("m", 12) == 1

def test_mississippi_i_1():
	assert ohe.rank("i", 1) == 0

def test_mississippi_i_2():
	assert ohe.rank("i", 2) == 1

def test_mississippi_i_3():
	assert ohe.rank("i", 3) == 1

def test_mississippi_i_4():
	assert ohe.rank("i", 4) == 1

def test_mississippi_i_5():
	assert ohe.rank("i", 5) == 2

def test_mississippi_i_10():
	assert ohe.rank("i", 10) == 3

def test_mississippi_i_11():
	assert ohe.rank("i", 11) == 4

def test_mississippi_sentinel_11():
	assert ohe.rank("$", 11) == 0

def test_mississippi_sentinel_12():
	assert ohe.rank("$", 12) == 1

def test_mississippi_s_6():
	assert ohe.rank("s", 6) == 3


# Words "mis sis sip pii $"
x2 = "mississippii$"
ohe2 = OneHotEncoding(x2)

def test_mississippii_sentinel_13():
	assert ohe2.rank("$", 13) == 1

def test_mississippii_i_13():
	assert ohe2.rank("i", 13) == 5

def test_mississippii_i_12():
	assert ohe2.rank("i", 12) == 5

def test_mississippii_i_11():
	assert ohe2.rank("i", 11) == 4

def test_mississippii_i_10():
	assert ohe2.rank("i", 10) == 3

def test_mississippii_i_9():
	assert ohe2.rank("i", 9) == 3



dna = "AGTCCTGAANCTGAGCCTTNAGG"
ohe_dna = OneHotEncoding(dna)

def test_dna_a_0():
	assert ohe_dna.rank("A", 0) == 0

def test_dna_a_1():
	assert ohe_dna.rank("A", 1) == 1

def test_dna_c_5():
	assert ohe_dna.rank("C", 5) == 2

def test_dna_G_21():
	assert ohe_dna.rank("G", 21) == 4

def test_dna_G_22():
	assert ohe_dna.rank("G", 22) == 5

def test_dna_G_23():
	assert ohe_dna.rank("G", 23) == 6

def test_dna_C_4():
	assert ohe_dna.rank("C", 4) == 1

def test_dna_C_5():
	assert ohe_dna.rank("C", 5) == 2


big = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
ohe_big = OneHotEncoding(big)


def test_big_a_0():
	assert ohe_big.rank("A", 0) == 0

def test_big_a_1():
	assert ohe_big.rank("A", 1) == 1

def test_big_b_1():
	assert ohe_big.rank("B", 1) == 0

def test_big_b_2():
	assert ohe_big.rank("B", 2) == 1

def test_big_z_25():
	assert ohe_big.rank("Z", 25) == 0

def test_big_z_26():
	assert ohe_big.rank("Z", 26) == 1

def test_big_9_37():
	assert ohe_big.rank("9", 37) == 0

def test_big_9_38():
	assert ohe_big.rank("9", 38) == 1

