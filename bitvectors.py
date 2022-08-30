from bitarray import bitarray
from math import log2, floor

'''
Return a tuple (dict, bitarray) where the bitarray is
a one hot encoding of x of size len(alpha)*len(x).
The first len(x) bits correspond to the first letter in alpha, etc.
Dict is the starting positions of the letters in the bitarray,
e.g. {'$': 0, 'i': 12, 'm': 24, 's': 36, 'p': 48}.
'''
def one_hot_encoding(x, n, alpha, a_size):

	# Initiate dict for {letter: start_pos_in_bitvector}
	# e.g., {'$': 0, 'i': 12, 'm': 24, 's': 36, 'p': 48}
	d = {}
	for i, c in enumerate(alpha):
		d[c] = i * n

	# Bit vector, all zeros
	bv = bitarray(n * a_size)
	bv.setall(0)

	# Iterate chars in x and set bits in bv correspondingly
	for i, c in enumerate(x):
		bv[d[c] + i] = 1

	return bv


def preprocess_rank_one_hot(bv, n, a_size):
	ranks = [[] for _ in range(a_size)]
	for idx, offset in enumerate(range(0, a_size*n, n)):
		word_size = floor(log2(n))
		no_of_words = n // word_size
		for i in range(no_of_words):
			count = bv[offset + i*word_size : offset + (i+1)*word_size].count(1)
			if i == 0:
				ranks[idx].append(count)
			else:
				c = ranks[idx][i-1] + count
				ranks[idx].append(c)
	return ranks


def rank_one_hot(rank_ls, n, a_size c, i):





########## Code to run ##########

x = "mississippi$"
n = len(x)
alpha = ["$", "i", "m", "p", "s"]
a_size = len(alpha)
bv = one_hot_encoding(x, n, alpha, a_size)
rank_ls = preprocess_rank_one_hot(bv, n, a_size)
rank_one_hot(rank_ls, n, a_size c, i)








