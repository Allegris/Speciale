from bitarray import bitarray
from math import log2, floor

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
def one_hot_encoding(x, alpha):
	n = len(x)
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
def preprocess_rank_one_hot(d, n, alpha):
	ranks = {char: [] for char in alpha}
	word_size = floor(log2(n))
	for char in d.keys():
		# Iterate over the words
		for i in range(n // word_size):
			# Rank of this word
			count = d[char][i*word_size : (i+1)*word_size].count(1)
			if i == 0:
				ranks[char].append(count)
			else: # Last word rank + this word rank
				ranks[char].append(ranks[char][i-1] + count)
	return ranks

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
def rank_one_hot(ranks, d, n, c, i):
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


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


########## Code to run ##########

x = "mississippi$"
n = len(x)
alpha = get_alphabet(x) # ["$", "i", "m", "p", "s"]
#a_size = len(alpha)

d = one_hot_encoding(x, alpha)
ranks = preprocess_rank_one_hot(d, n, alpha)
print(rank_one_hot(ranks, d, n, "i", 6))




