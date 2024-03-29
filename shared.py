from bitarray import bitarray
from bitarray.util import canonical_huffman #, huffman_code
import skew
import numpy as np

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
	#codes = huffman_code(count) # not necessarily lexicographical order, if equal count
	return codes


########################################################
# Bitvector ranks: preprocess and lookup
########################################################

'''
Preprocesses node word ranks of a bitvector of length n.
Each word is of length 32.
Returns a list of word ranks for ones.
(for zeros, we will just subtract the number of ones from the index).
'''
def preprocess_one_ranks(bitvector):
	no_of_words = ((len(bitvector)) // 32) + 1
	ranks = np.zeros(no_of_words, dtype = np.int32)
	word_size = 32
	# Iterate words
	for i in range(len(bitvector) // word_size):
		word = bitvector[i*word_size: (i+1)*word_size]
		ranks[i+1] = ranks[i] + word.count(1) # count ones
	return ranks

'''
Finds the rank of a letter c and an index i in a bitvector,
by looking up in the word ranks and counting the remaining bits in the word.
'''
def bitvector_rank(bitvector, one_ranks, c, i):
	word_size = 32
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
Encodes string s using Huffman codes (at index level in each code).

Returns:
	bin_s: The binary encoding of s
	s0: The part of s that corresponds to zeros
	s1: The part of s that corresponds to ones

E.g., for s = "mississippi" at level 0, it returns:
	bitarray('00110110110') miiii sssspp
'''
def split_node(s, codes, level):
	# Binary encoding of s
	bin_s = bitarray()
	# The part of s corresponding to zeros and ones, respectively
	s0, s1 = "", ""
	for char in s:
		# Encoding of char at this level
		char_code = codes[char][level]
		bin_s.append(char_code)
		if char_code:
			s1 += char
		else:
			s0 += char
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


