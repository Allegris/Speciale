from bitarray import bitarray
from math import log2, floor

class WaveletTreeLeaf:
	def __init__(self, letter):
		self.letter = letter


class WaveletTreeNode:
	def __init__(self, x, root):
		self.n = len(x)
		alpha = self.get_alphabet(x)

		if root:
			self.root = root
		else: # If node has no root: it IS the root
			self.root = self
			self.codes = {letter: bitarray() for letter in alpha}

		# Split alphabet to create child nodes
		bv, left, right, no_of_children = self.split_node(x, alpha)

		self.bitvector = bv
		self.ranks = self.preprocess_node_ranks(self.bitvector, self.n)

		if no_of_children >= 4:
			self.left_child = WaveletTreeNode(left, self.root)
			self.right_child = WaveletTreeNode(right, self.root)
		elif no_of_children == 3:
			self.left_child = WaveletTreeLeaf(left[0])
			self.right_child = WaveletTreeNode(right, self.root)
		else:
			self.left_child = WaveletTreeLeaf(left[0])
			self.right_child = WaveletTreeLeaf(right[0])


	'''
	Returns a sorted list of the set of letters used in x.
	'''
	def get_alphabet(self, x):
		letters = ''.join(set(x))
		return sorted(letters)


	'''
	Splits alphabet in half and assigns binary values to each letter,
	i.e., d = {letter: binary}.
	Returns:
		bin_x: The binary representation of x (wrt. the alphabet split)
		x0: The part of x that corresponds to 0s
		x1: The part of x that corresponds to 1s
		a_size: Size of the alphabet of x
	Examples of return:
		1) bitarray('00110110110') miiii sssspp 4
		2) bitarray('10000') iiii m 2
		3) bitarray('111100') pp ssss 2
	'''
	def split_node(self, x, alpha):
		a_size = len(alpha)
		d = {letter: 0 for letter in alpha}

		for letter in alpha[a_size // 2:]: # assign second half of alphabet to 1
			d[letter] = 1
		for letter in alpha: # Update codes for letters
			self.root.codes[letter].append(d[letter])

		bin_x = bitarray() # Binary representation of x
		x0, x1 = "", "" # The 0 / 1 parts of x
		for char in x:
			bin_x.append(d[char])
			if d[char] == 0:
				x0 += char
			else:
				x1 += char
		print(bin_x, x0, x1, a_size)
		return bin_x, x0, x1, a_size


	'''
	Preprocesses word ranks of a bitvector of length n.
	Each word is of length floor(log2(n)) (remainder is not in a word).

	Returns a dict {0: [word_ranks], 1: [word_ranks]} where the lists contain
	the rank of each word for the given bit, e.g., {0: [2, 3, 4], 1: [1, 3, 5]}
	'''
	def preprocess_node_ranks(self, bitvector, n):
		ranks = {0: [], 1: []}
		word_size = floor(log2(n))
		for i in range(n // word_size): # Iterate words
			word = bitvector[i*word_size: (i+1)*word_size]
			prev_0s = 0 if i == 0 else ranks[0][i-1]
			prev_1s = 0 if i == 0 else ranks[1][i-1]
			ranks[0].append(prev_0s + word.count(0))
			ranks[1].append(prev_1s + word.count(1))
		return ranks

	'''
	Finds the rank of a char c and an index i in a bitvector of length n,
	by looking up in ranks and/or scanning the bits in the bitvector.
	'''
	def node_rank(self, bitvector, ranks, n, c, i):
		word_size = floor(log2(n))
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




######################################################################################################

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





##### Code to run #####

x = "mississippi"
wt_root = WaveletTreeNode(x, False)
print(rank_query(wt_root, "i", 8))



