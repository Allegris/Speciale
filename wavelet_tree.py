from bitarray import bitarray
from math import log2, floor
from shared import get_alphabet, letter_count, alphabet_size
from bitarray.util import canonical_huffman


########################################################
# Classes for wavelet tree leaves and internal nodes
########################################################


#class WaveletTreeLeaf:
#	def __init__(self, letter):
#		self.letter = letter


class WaveletTreeNode:
	def __init__(self, s, level, root):
		self.n = len(s)

		if level == 0: #root
			self.root = self
			self.codes, _, _ = canonical_huffman(letter_count(s))
		else:
			self.root = root


		# Split alphabet to create child nodes
		bin_s, s0, s1 = self.split_node(s, level, self.root.codes)

		self.bitvector = bin_s
		self.ranks = self.preprocess_node_ranks(self.bitvector, self.n)

		if alphabet_size(s) > 1:
			self.left_child = None
			self.right_child = None
		if alphabet_size(s0) > 1: # if inner node
			self.left_child = WaveletTreeNode(s0, level+1, self.root)
		if alphabet_size(s1) > 1: # if inner node
			self.right_child = WaveletTreeNode(s1, level+1, self.root)


	'''
	Splits alphabet in half and assigns binary values to each letter,
	i.e., d = {letter: binary}.
	Returns:
		bin_x: The binary representation of x (wrt. the alphabet split)
		x0: The part of x that corresponds to 0s
		x1: The part of x that corresponds to 1s
	Examples of return:
		1) bitarray('00110110110') miiii sssspp
		2) bitarray('10000') iiii m
		3) bitarray('111100') pp ssss
	'''
	def split_node(self, s, level, codes):
		alpha = get_alphabet(s)
		d = {letter: codes[letter][level] for letter in alpha}
		# Binary representation of s
		bin_s = bitarray()
		# The part of s corresponding to 1s
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
	def preprocess_node_ranks(self, bitvector, length):
		ranks = {0: [], 1: []}
		word_size = floor(log2(length))
		for i in range(length // word_size): # Iterate words
			word = bitvector[i*word_size: (i+1)*word_size]
			# Zeros
			prev_0s = 0 if i == 0 else ranks[0][i-1]
			ranks[0].append(prev_0s + word.count(0))
			# Ones
			prev_1s = 0 if i == 0 else ranks[1][i-1]
			ranks[1].append(prev_1s + word.count(1))
		return ranks


	'''
	Finds the rank of a char c and an index i in a bitvector of length n,
	by looking up in ranks and/or scanning the bits in the bitvector.
	'''
	def node_rank(self, bitvector, ranks, n, c, i):
		word_size = floor(log2(len(bitvector)))
		word_no = (i // word_size)
		scan_len = i % word_size
		# If in first word, just scan
		if word_no == 0:
			return bitvector[0:scan_len].count(c)
		# If we do not need to scan, look-up the rank directly in ranks
		if scan_len == 0:
			return ranks[c][word_no - 1]
		# If we need to look-up in ranks AND scan
		else:
			start = word_no * word_size
			end = start + scan_len
			return ranks[c][word_no - 1] + bitvector[start:end].count(c)


########################################################
# Rank query using wavelet tree
########################################################

'''
Iterates a wavelet tree, starting from the root, and returns the rank of a
given char c and a given index i.
'''
def rank_query(root, c, i):
	code = root.codes[c] # code of c, e.g., "00" (left, left) for i in mississippi
	node = root
	ii = i
	for char in code:
		ii = node.node_rank(node.bitvector, node.ranks, node.n, char, ii)
		node = node.left_child if char == 0 else node.right_child
	return ii


########################################################
# Code to run
########################################################



#x = "mississippialpha"
x = "ississippi"
wt_root = WaveletTreeNode(x, 0, None) # s, level, root
#print(wt_root.__dict__)

'''
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















