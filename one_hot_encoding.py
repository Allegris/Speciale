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

Inputs are:
	x: input string
	n = length of x
	alpha: alphabet
'''
def one_hot_encoding(x):
	# Initiate dict {letter: bitarray} of all zeros
	# e.g., {'$': bitarray('000000000000'), 'i': bitarray('000000000000'), ...}
	ohe = {char: bitarray(len(x)) for char in get_alphabet(x)}
	for bv in ohe.values():
		bv.setall(0)
	# Set bits corresponding to chars in x
	# e.g. {'$': bitarray('000000000001'), 'i': bitarray('010010010010'), ...}
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
	 Input string x is only given implicitly as input, in the form of d:
	 d: dict {letter: bitarray} where the set bits correspond to the places
	    where the given letter appear in string x.
	 n: length of x
	 alpha: alphabet
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
	 Input string x is only given implicitly as input, in the form of ranks and d:
	 ranks: dict {letter: [word_ranks]} where the list contains the rank of each word.
	 d: dict {letter: bitarray} where the set bits correspond to the places
	    where the given letter appear in string x.
	 n: length of x
	 c: query letter
	 i: query index
'''
def old_rank_query(ranks, d, n, c, i):
	word_size = floor(log2(n))
	word_no = (i // word_size)
	scan_len = i % word_size
	# If in first word, just scan
	if word_no == 0:
		return d[c][0:scan_len].count(1)
	# If we do not need to scan, look-up the rank directly in ranks
	if scan_len == 0:
		return ranks[c][word_no - 1]
	# If we both need to look-up in ranks and scan
	else:
		start = word_no * word_size
		end = start + scan_len
		return ranks[c][word_no - 1] + d[c][start:end].count(1)


def rank_query(ohe, ranks, c, i):
	return bitvector_rank(ohe[c], ranks[c], 1, i)

########################################################
# Code to run
########################################################


'''
x = "mississippi$"
n = len(x)
alpha = get_alphabet(x) # ["$", "i", "m", "p", "s"]
#a_size = len(alpha)

d = one_hot_encoding(x, alpha)
ranks = preprocess_rank_one_hot(d, n, alpha)
print(rank_one_hot(ranks, d, n, "i", 6))
'''



