from bitarray import bitarray
from math import log2, floor

class WaveletTreeNode:
	def __init__(self, x, root):
		#print("Node", x)
		self.x = x
		self.n = len(x)
		self.alpha = self.get_alphabet(x)
		self.bitvector = None
		self.ranks = None
		self.left_child = None
		self.right_child = None

		if root:
			self.root = root
		else: # If node has no root: it IS the root
			self.root = self
			self.codes = {letter: bitarray() for letter in self.alpha}


		# Split alphabet to create children
		bv, left, right, leaf = self.split_node(x)
		self.bitvector = bv
		self.ranks = self.preprocess_node_ranks(self.bitvector, self.n)
		if not leaf:
			self.left_child = WaveletTreeNode(left, self)
			self.right_child = WaveletTreeNode(right, self)
		else:
			self.left_child = WaveletTreeLeaf(left[0])
			self.right_child = WaveletTreeLeaf(right[0])


	def get_alphabet(self, x):
		letters = ''.join(set(x))
		return sorted(letters)


	def split_node(self, x):
		alpha = self.alpha
		a_size = len(alpha)
		# Assign binary value to each letter: d = {letter: binary},
		# (split alphabet in half)
		d = {letter: 0 for letter in alpha}
		for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
			d[letter] = 1
		# Update codes for letters
		for letter in alpha:
			self.root.codes[letter].append(d[letter])
		# Binary representation of x
		bin_x = bitarray()
		# The part of x corresponding to 0s and 1s, respectively
		x0, x1 = "", ""
		for char in x:
			bin_x.append(d[char])
			if d[char] == 0:
				x0 += char
			else:
				x1 += char
		# Are the child nodes leaves or not
		child_leaves = False if a_size > 2 else True
		return bin_x, x0, x1, child_leaves


	def preprocess_node_ranks(self, bitvector, n):
		ranks = {0: [], 1: []}
		word_size = floor(log2(n))
		for i in range(n // word_size):
			word = bitvector[i*word_size: (i+1)*word_size]
			if i == 0:
				ranks[0].append(word.count(0))
				ranks[1].append(word.count(1))
			else:
				ranks[0].append(ranks[0][i-1] + word.count(0))
				ranks[1].append(ranks[1][i-1] + word.count(1))
		return ranks

	def node_rank(self, bitvector, ranks, n, c, i):
		print("X", self.x)
		word_size = floor(log2(n))
		word_no = (i // word_size)
		scan_len = i % word_size
		# If in first word, just scan
		if word_no == 0:
			return bitvector[0:scan_len].count(c)
		# If we do not need to scan, look-up the rank directly in ranks
		if scan_len == 0:
			return ranks[c][word_no - 1]
		# If we both need to look-up in ranks and scan
		else:
			start = word_no * word_size
			end = start + scan_len
			return ranks[c][word_no - 1] + bitvector[start:end].count(c)



class WaveletTreeLeaf:
	def __init__(self, letter):
		#print("Leaf", letter)
		self.letter = letter


######################################################################################################


def rank_query(root, c, i):
	code = root.codes[c]
	node = root
	ii = i
	for char in code:
		ii = node.node_rank(node.bitvector, node.ranks, node.n, char, ii)
		if char == 0:
			node = node.left_child
		else:
			node = node.right_child
	return ii





##### Code to run #####
x = "mississippi"
wt_root = WaveletTreeNode(x, False)
print(rank_query(wt_root, "i", 8))

