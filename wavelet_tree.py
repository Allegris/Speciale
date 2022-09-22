from bitarray import bitarray
from math import log2, floor
from shared import get_alphabet, letter_count, alphabet_size
from bitarray.util import canonical_huffman


########################################################
# Classes for wavelet tree internal nodes
########################################################

class WaveletTreeNode:
	def __init__(self, s, level, root):
		if level == 0: # If is root
			self.root = self
			self.codes, _, _ = canonical_huffman(letter_count(s))
		else:
			self.root = root

		# Encode s and split s in two parts (potential child nodes)
		bin_s, s0, s1 = self.split(s, level)

		# Set bitvector and preprocess ranks
		self.bitvector = bin_s
		self.word_ranks = self.preprocess_word_ranks()

		# Create children
		self.left_child, self.right_child = None, None
		# Left child
		if alphabet_size(s0) > 1: # If left child is inner node
			self.left_child = WaveletTreeNode(s0, level + 1, self.root)
		# Right child
		if alphabet_size(s1) > 1: # If right child is inner node
			self.right_child = WaveletTreeNode(s1, level + 1, self.root)


	'''
	Encodes string s using Huffman encoding in codes (index level in each code).
	Returns:
		bin_s: The binary representation of s
		s0: The part of s that corresponds to 0s
		s1: The part of s that corresponds to 1s
	Examples of return:
		1) bitarray('00110110110') miiii sssspp
		2) bitarray('10000') iiii m
		3) bitarray('111100') pp ssss
	'''
	def split(self, s, level):
		codes = self.root.codes
		alpha = get_alphabet(s)
		# Set d = {letter: binary code at this level (either 0 or 1)}
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
	Preprocesses word ranks of a bitvector of length n.
	Each word is of length floor(log2(n)) (remainder is not in a word).

	Returns a dict {0: [word_ranks], 1: [word_ranks]} where the lists contain
	the rank of each word for the given bit, e.g., {0: [2, 3, 4], 1: [1, 3, 5]}
	'''
	def preprocess_word_ranks(self):
		ranks = {0: [], 1: []}
		word_size = floor(log2(len(self.bitvector)))
		for i in range(len(self.bitvector) // word_size): # Iterate words
			word = self.bitvector[i*word_size: (i+1)*word_size]
			# Zeros
			prev_0s = 0 if i == 0 else ranks[0][i-1]
			ranks[0].append(prev_0s + word.count(0))
			# Ones
			prev_1s = 0 if i == 0 else ranks[1][i-1]
			ranks[1].append(prev_1s + word.count(1))
		return ranks


	'''
	Finds the rank of a char c and an index i in a bitvector,
	by looking up in word_ranks and/or scanning the bits in the bitvector.
	'''
	def rank_lookup(self, c, i):
		word_size = floor(log2(len(self.bitvector)))
		word_no = (i // word_size)
		scan_len = i % word_size
		# If in first word, just scan
		if word_no == 0:
			return self.bitvector[0:scan_len].count(c)
		# If we do not need to scan, look-up the rank directly in ranks
		if scan_len == 0:
			return self.word_ranks[c][word_no - 1]
		# If we need to look-up in ranks AND scan
		else:
			start = word_no * word_size
			end = start + scan_len
			return self.word_ranks[c][word_no - 1] + self.bitvector[start:end].count(c)


########################################################
# Rank query using wavelet tree
########################################################

'''
Iterates a wavelet tree, starting from the root, and returns the rank of a
given char c and a given index i.
'''
def rank_query(root, c, i):
	code = root.codes[c]
	node = root
	rank = i # Current rank
	for char in code:
		rank = node.rank_lookup(char, rank)
		node = node.left_child if char == 0 else node.right_child
	return rank


########################################################
# Code to run
########################################################


'''
#x = "mississippialpha"
x = "ississippi"
wt_root = WaveletTreeNode(x, 0, None) # s, level, root
#print(wt_root.__dict__)


print(rank_query(wt_root, "i", 8))


# starting the monitoring
#tracemalloc.start()

# function call
x = "mississippi"
wt_root = WaveletTreeNode(x, False)
rank_query(wt_root, "i", 8)

# displaying the memory
#print(tracemalloc.get_traced_memory())

# stopping the library
#tracemalloc.stop()
'''

