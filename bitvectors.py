from bitarray import bitarray


def one_hot_encoding(x, alpha):
	# Initiate dict {char: bitvector}
	# s.t. bitvectors are just all zeros
	d = {}
	for c in alpha:
		bv = bitarray(len(x))
		bv.setall(0)
		d[c] = bv

	# Iterate chars of x to set bits in dict
	# corresponding to the chars
	for i, c in enumerate(x):
		bv = d[c]
		bv[i] = True
	return d






# Code to run
x = "mississippi$"
alpha = ["$", "i", "m", "s", "p"]
print(one_hot_encoding(x, alpha))