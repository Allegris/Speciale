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

	return bv, d

def preprocess_rank_one_hot(bv, d, n, alpha):
	ranks = {char: [] for char in alpha}
	for char, offset in d.items():
		word_size = floor(log2(n))
		no_of_words = n // word_size
		for i in range(no_of_words):
			count = bv[offset + i*word_size : offset + (i+1)*word_size].count(1)
			if i == 0:
				ranks[char].append(count)
			else:
				ranks[char].append(ranks[char][i-1] + count)
	return ranks


def rank_one_hot(ranks, bv, d, n, c, i):
	word_size = floor(log2(n))
	if i == 0:
		return 0
	word_no = (i // word_size)
	scan_len = i % word_size

	print(word_no)


	if i % word_size == 0:
		word = int((i / word_size) - 1)
		return ranks[c][word]
	else:
		word = int((i / word_size) - 1)
	return "TO DO"


################## NEW ######################################



def new_one_hot_encoding(x, n, alpha, a_size):
	# Initiate dict {letter: bitarray} of all zeros
	# e.g., {'$': bitarray('000000000000'), 'i': bitarray('000000000000'), ...}
	d = {char: bitarray(n) for char in alpha}
	for bv in d.values():
		bv.setall(0)
	# Set bits corresponding to chars in x
	# e.g. {'$': bitarray('000000000001'), 'i': bitarray('010010010010'), ...}
	for i, char in enumerate(x):
		d[char][i] = 1
	return d

def new_preprocess_rank_one_hot(d, n, alpha):
	ranks = {char: [] for char in alpha}
	word_size = floor(log2(n))
	no_of_words = n // word_size
	for char in d.keys():
		for i in range(no_of_words):
			count = d[char][i*word_size : (i+1)*word_size].count(1)
			if i == 0:
				ranks[char].append(count)
			else:
				ranks[char].append(ranks[char][i-1] + count)
	return ranks

def new_rank_one_hot(ranks, bv, d, n, c, i):
	word_size = floor(log2(n))
	if i == 0:
		return 0
	word_no = (i // word_size)
	scan_len = i % word_size

	print(word_no)


	if i % word_size == 0:
		word = int((i / word_size) - 1)
		return ranks[c][word]
	else:
		word = int((i / word_size) - 1)
	return "TO DO"





########## Code to run ##########

x = "mississippi$"
n = len(x)
alpha = ["$", "i", "m", "p", "s"]
a_size = len(alpha)
'''
bv, d = one_hot_encoding(x, n, alpha, a_size)
ranks = preprocess_rank_one_hot(bv, d, n, alpha)
print(ranks, "\n")
print(rank_one_hot(ranks, bv, d, n, "p", 9))
'''

d = new_one_hot_encoding(x, n, alpha, a_size)
ranks = new_preprocess_rank_one_hot(d, n, alpha)
new_rank_one_hot(ranks, d, n, c, i)




