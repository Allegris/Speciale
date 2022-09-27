from bitarray import bitarray
from math import log2, floor
from shared import get_alphabet, bitvector_rank


########################################################
# Construct one hot encoding
########################################################

'''
Returns a dict {letter: bitarray} where the set bits correspond to the places
where the given letter appear in string x. E.g., for x = "mississippi$", it returns:
{'$': bitarray('000000000001'),
 'i': bitarray('010010010010'),
 'm': bitarray('100000000000'),
 'p': bitarray('000000001100'),
 's': bitarray('001101100000')}
'''
def one_hot_encoding(x):
	# Initiate dict {letter: bitarray} of all zeros
	ohe = {char: bitarray(len(x)) for char in get_alphabet(x)}
	for bv in ohe.values():
		bv.setall(0)
	# Set bits corresponding to chars in x
	for i, char in enumerate(x):
		ohe[char][i] = 1
	return ohe


########################################################
# Preprocess ranks for one hot encoding
########################################################

'''
Returns a dict {letter: [word_ranks]} where the list contains the rank of each
word of x (x is split into log(n) words).
E.g. x = "mississippi$" will be split into 4 words of length 3:
"mis sis sip pi$" and the ranks of the words will be:
{'$': [0, 0, 0, 1],
 'i': [1, 2, 3, 4],
 'm': [1, 1, 1, 1],
 'p': [0, 0, 1, 2],
 's': [1, 3, 4, 4]}

Inputs are:
	 Input string x is only given implicitly as input, in the form of:
	 ohe: dict {letter: bitarray} where the set bits correspond to the places
	      where the given letter appear in string x.
	 n: length of x
'''
def preprocess_ranks(ohe, n):
	ranks = {char: [0] for char in ohe.keys()}
	word_size = floor(log2(n))
	for char in ohe.keys():
		# Iterate over the words
		for i in range(n // word_size):
			# Rank of this word
			count = ohe[char][i*word_size : (i+1)*word_size].count(1)
			ranks[char].append(ranks[char][i] + count)
	return ranks


########################################################
# Rank query for one hot encoding
########################################################

'''
Returns the rank of a given letter and index in string x.

Inputs are:
	 Input string x is only given implicitly as input, in the form of ohe and ranks:
	 ohe: dict {letter: bitarray} where the set bits correspond to the places
	      where the given letter appear in string x.
	 ranks: dict {letter: [word_ranks]} where the list contains the rank of each word.
	 c: query letter
	 i: query index
'''
def rank_query(ohe, ranks, c, i):
	# We query 1s in bitvector for c (set bits)
	return bitvector_rank(ohe[c], ranks[c], 1, i)


########################################################
# Code to run
########################################################


'''
x = "mississippi$"
ohe = one_hot_encoding(x)
ranks = preprocess_ranks(ohe, len(x))
print(rank_query(ohe, ranks, "i", 6))
'''


