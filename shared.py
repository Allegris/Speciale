from bitarray import bitarray
from bitarray.util import huffman_code, canonical_huffman
from math import floor, log2
import skew
from bitarray.util import count_n




########################################################
# Suffix arrays
########################################################

'''
Slow, naïve suffix array construction algorithm
'''
def construct_sa_slow(x):
	suffixes = [x[i:] for i in range(len(x))]
	suffixes_sorted = sorted(suffixes)
	sa = [len(x)-len(y) for y in suffixes_sorted]
	return sa

'''
Constructs the suffix array of x, using the Skew algorithm; time O(n)
'''
def construct_sa_skew(x):
	alpha, indices = skew.map_string_to_ints(x)
	return skew.skew_rec(indices, len(alpha))

'''
Constructs sparse SA as dict {idx: SA_val} for only some of the indices in
normal SA; namely for SA_vals = 0, k, 2k, 3k, etc.
'''
def construct_sparse_sa(sa, k):
	sparse_sa = {}
	for idx, val in enumerate(sa):
		if val % k == 0:
			sparse_sa[idx] = val
	return sparse_sa


########################################################
# Alphabets, letter counts, Huffman codes
########################################################

'''
Returns a lex sorted list of the letters of string x.
'''
def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)

'''
Returns the size of the alphabet of string x.
'''
def alphabet_size(x):
	letters = ''.join(set(x))
	return len(letters)

'''
Returns a dict {letter: count} of the counts of the letters in x.
'''
def letter_count(x):
	alpha = get_alphabet(x)
	# Map between letters and ints
	counts = {a: 0 for a in alpha}
	for char in x:
		counts[char] += 1
	return counts

'''
Returns the Huffman codes of the alphabet of x, depending on the letter counts.
E.g., for x = "mississippi", it returns:
{'i': bitarray('0'),
 's': bitarray('10'),
 'm': bitarray('110'),
 'p': bitarray('111')}
'''
def huffman_codes(x):
	count = letter_count(x)
	codes, _, _ = canonical_huffman(count) # lexicographical order, if equal count
	#codes = huffman_code(count) # non-lexicographical order, uf equal count
	return codes


########################################################
# Bitvector ranks: preprocess and lookup
########################################################

'''
Preprocesses node word ranks of a bitvector of length n.
Each word is of length floor(log2(n)).

Returns a list of word ranks for 1
(for 0, we will just subtract the number of ones from the index).
'''
def preprocess_one_ranks(bitvector):
	ranks = [0]
	word_size = floor(log2(len(bitvector)))
	for i in range(len(bitvector) // word_size): # Iterate words
		word = bitvector[i*word_size: (i+1)*word_size]
		ranks.append(ranks[i] + word.count(1)) # Ones
	return ranks

'''
Finds the rank of a char c and an index i in a bitvector,
by looking up in the word ranks and scanning the bits in the bitvector.
'''
def bitvector_rank(bitvector, one_ranks, c, i):
	word_size = floor(log2(len(bitvector))) #bit length, højst satte bit
	word_no = (i // word_size)
	scan_len = i % word_size
	scan_start = word_no * word_size
	scan_end = scan_start + scan_len
	word_rank = one_ranks[word_no] if c else word_no * word_size - one_ranks[word_no]
	return word_rank + bitvector[scan_start:scan_end].count(c)


########################################################
# Wavelet tree: Split node in two
########################################################

'''
Encodes string s using Huffman encoding in codes (index level in each code).

Returns:
	bin_s: The binary representation of s
	s0: The part of s that corresponds to 0s
	s1: The part of s that corresponds to 1s

E.g., for s = "mississippi" at level 0, it returns:
	bitarray('00110110110') miiii sssspp
'''
def split_node(s, codes, level):
	alpha = get_alphabet(s)
	d = {letter: codes[letter][level] for letter in alpha}
	# Binary representation of s
	bin_s = bitarray()
	# The part of s corresponding to zeros and ones, respectively
	s0, s1 = "", ""
	for char in s:
		bin_s.append(d[char])
		if d[char] == 0:
			s0 += char
		else:
			s1 += char
	return bin_s, s0, s1


########################################################
# Burrows-Wheeler Transform
########################################################

'''
Construct BWT(x) using SA
'''
def bwt(x, sa):
	bwt = ""
	for i in range(len(x)):
		if sa[i] == 0:
			bwt += "$"
		else:
			bwt += x[sa[i]-1]
	return bwt


