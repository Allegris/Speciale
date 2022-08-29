from bitarray import bitarray
import time

def old_one_hot_encoding(x, alpha):
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

'''
Return a tuple (len(x), bitarray) where the bitarray is
a one hot encoding of x of size len(alpha)*len(x).
The first len(x) bits correspond to the first letter in alpha, etc.
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

	return (len_x, bv)

def test_length(x):
	#b = len(x)
	start = time.time()
	for _ in range(10000000):
		#a = b
		a = len(x)
	end = time.time()
	print(end-start)


# Code to run

x = "mississippi$"
#alpha = ["$", "i", "m", "s", "p"]
#print(one_hot_encoding(x, alpha))

test_length(x)









