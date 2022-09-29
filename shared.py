from bitarray import bitarray
from bitarray.util import canonical_huffman#, huffman_code
from math import floor, log2
import sys

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
	codes, _, _ = canonical_huffman(count)
	return codes


'''
Preprocesses node word ranks of a bitvector of length n.
Each word is of length floor(log2(n)) (remainder is not in a word).

Returns a dict {0: [word_ranks], 1: [word_ranks]} where the lists contain
the rank of each word for the given bit, e.g., {0: [0, 1, 2, 3], 1: [0, 2, 4, 6]}
'''
def preprocess_node_word_ranks(bitvector):
	ranks = {0: [0], 1: [0]}
	word_size = floor(log2(len(bitvector)))
	for i in range(len(bitvector) // word_size): # Iterate words
		word = bitvector[i*word_size: (i+1)*word_size]
		ranks[0].append(ranks[0][i] + word.count(0)) # Zeros
		ranks[1].append(ranks[1][i] + word.count(1)) # Ones
	return ranks

'''
Finds the rank of a char c and an index i in a bitvector,
by looking up in the word ranks and scanning the bits in the bitvector.
'''
def bitvector_rank(bitvector, word_ranks, c, i):
	word_size = floor(log2(len(bitvector)))
	word_no = (i // word_size)
	scan_len = i % word_size
	scan_start = word_no * word_size
	scan_end = scan_start + scan_len
	# Look-up and scan (scan length may be 0)
	return word_ranks[word_no] + bitvector[scan_start:scan_end].count(c)


'''
Encodes string s using Huffman encoding in codes (index level in each code).

Returns:
	bin_s: The binary representation of s
	s0: The part of s that corresponds to 0s
	s1: The part of s that corresponds to 1s

E.g., for s = "mississippi" at level 0, it returns:
	1) bitarray('00110110110') miiii sssspp
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


'''
#codes = huffman_codes("ABCDEFG")

alfa = ["A","C","G","T","$"]

codes = [bitarray('0'), bitarray('100'), bitarray('101'), bitarray('110'), bitarray('111')]

b = huffman_codes("ACTAGA$") #alfa

bv = bitarray('0000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111111000000000001')

print(sys.getsizeof(b))

#print(huffman_codes("ACTAGA$"))
'''



