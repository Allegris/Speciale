from bitarray import bitarray

'''
Return a tuple (dict, bitarray) where the bitarray is
a one hot encoding of x of size len(alpha)*len(x).
The first len(x) bits correspond to the first letter in alpha, etc.
Dict is the starting positions of the letters in the bitarray,
e.g. {'$': 0, 'i': 12, 'm': 24, 's': 36, 'p': 48}.
'''
def one_hot_encoding(x, alpha):
	len_x = len(x)

	# Initiate dict for {letter: start_pos_in_bitvector}
	# e.g., {'$': 0, 'i': 12, 'm': 24, 's': 36, 'p': 48}
	d = {}
	for i, c in enumerate(alpha):
		d[c] = i * len_x

	# Bit vector, all zeros
	bv = bitarray(len_x * len(alpha))
	bv.setall(0)

	# Iterate chars in x and set bits in bv correspondingly
	for i, c in enumerate(x):
		bv[d[c] + i] = 1

	return (d, bv)




########## Code to run ##########

x = "mississippi$"
alpha = ["$", "i", "m", "s", "p"]
print(one_hot_encoding(x, alpha))











