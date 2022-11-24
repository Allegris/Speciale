import one_hot_encoding as ohe


# Words "mis sis sip pi$"
x = "mississippi$"
oh = ohe.OneHotEncoding(x)


def test_mississippi_m_0():
	assert oh.rank("m", 0) == 0

def test_mississippi_m_12():
	assert oh.rank("m", 12) == 1

def test_mississippi_i_1():
	assert oh.rank("i", 1) == 0

def test_mississippi_i_2():
	assert oh.rank("i", 2) == 1

def test_mississippi_i_3():
	assert oh.rank("i", 3) == 1

def test_mississippi_i_4():
	assert oh.rank("i", 4) == 1

def test_mississippi_i_5():
	assert oh.rank("i", 5) == 2

def test_mississippi_i_10():
	assert oh.rank("i", 10) == 3

def test_mississippi_i_11():
	assert oh.rank("i", 11) == 4

def test_mississippi_sentinel_11():
	assert oh.rank("$", 11) == 0

def test_mississippi_sentinel_12():
	assert oh.rank("$", 12) == 1

def test_mississippi_s_6():
	assert oh.rank("s", 6) == 3


# Words "mis sis sip pii $"
x2 = "mississippii$"
oh2 = ohe.OneHotEncoding(x2)

def test_mississippii_sentinel_13():
	assert oh2.rank("$", 13) == 1

def test_mississippii_i_13():
	assert oh2.rank("i", 13) == 5

def test_mississippii_i_12():
	assert oh2.rank("i", 12) == 5

def test_mississippii_i_11():
	assert oh2.rank("i", 11) == 4

def test_mississippii_i_10():
	assert oh2.rank("i", 10) == 3

def test_mississippii_i_9():
	assert oh2.rank("i", 9) == 3



dna = "AGTCCTGAANCTGAGCCTTNAGG"
oh_dna = ohe.OneHotEncoding(dna)

def test_dna_a_0():
	assert oh_dna.rank("A", 0) == 0

def test_dna_a_1():
	assert oh_dna.rank("A", 1) == 1

def test_dna_c_5():
	assert oh_dna.rank("C", 5) == 2

def test_dna_G_21():
	assert oh_dna.rank("G", 21) == 4

def test_dna_G_22():
	assert oh_dna.rank("G", 22) == 5

def test_dna_G_23():
	assert oh_dna.rank("G", 23) == 6

def test_dna_C_4():
	assert oh_dna.rank("C", 4) == 1

def test_dna_C_5():
	assert oh_dna.rank("C", 5) == 2


big = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
oh_big = ohe.OneHotEncoding(big)


def test_big_a_0():
	assert oh_big.rank("A", 0) == 0

def test_big_a_1():
	assert oh_big.rank("A", 1) == 1

def test_big_b_1():
	assert oh_big.rank("B", 1) == 0

def test_big_b_2():
	assert oh_big.rank("B", 2) == 1

def test_big_z_25():
	assert oh_big.rank("Z", 25) == 0

def test_big_z_26():
	assert oh_big.rank("Z", 26) == 1

def test_big_9_37():
	assert oh_big.rank("9", 37) == 0

def test_big_9_38():
	assert oh_big.rank("9", 38) == 1

