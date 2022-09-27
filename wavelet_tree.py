from bitarray import bitarray
from math import log2, floor
from shared import get_alphabet, letter_count, alphabet_size, bitvector_rank, preprocess_node_word_ranks
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
		self.word_ranks = preprocess_node_word_ranks(self.bitvector)

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
		#rank = node.rank_lookup(char, rank)
		rank = bitvector_rank(node.bitvector, node.word_ranks[char], char, rank)
		node = node.left_child if char == 0 else node.right_child
	return rank


########################################################
# Code to run
########################################################


'''
#x = "mississippialpha"
x = "mississippi"
wt_root = WaveletTreeNode(x, 0, None) # s, level, root
#print(wt_root.__dict__)
print(wt_root.word_ranks)
print(rank_query(wt_root, "i", 8))
'''
