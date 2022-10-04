from shared import alphabet_size, bitvector_rank, preprocess_node_word_ranks, split_node, huffman_codes

########################################################
# Classes for wavelet tree internal nodes
########################################################

class WaveletTreeNode:
	def __init__(self, s, level, root):
		# Root pointer and store codes at root
		if level == 0:
			self.root = self
			self.codes = huffman_codes(s)
		else:
			self.root = root
		# Construct bitvector and split s in two parts (child nodes)
		self.bitvector, s0, s1 = split_node(s, self.root.codes, level)
		# Preprocess ranks
		self.word_ranks = preprocess_node_word_ranks(self.bitvector)
		# Create children
		self.left_child, self.right_child = None, None
		# If left child is an inner node
		if alphabet_size(s0) > 1:
			self.left_child = WaveletTreeNode(s0, level+1, self.root)
		# If right child is an inner node
		if alphabet_size(s1) > 1:
			self.right_child = WaveletTreeNode(s1, level+1, self.root)

########################################################
# Rank query using wavelet tree
########################################################
'''
Iterates a wavelet tree, starting from the root, and returns the rank of a
given char c and a given index i.
'''
def rank(root, c, i):
	# Current node and rank
	node = root
	rank = i
	# Iterate chars in code
	for char in root.codes[c]:
		# Update rank and node
		rank = bitvector_rank(node.bitvector, node.word_ranks[char], char, rank)
		node = node.right_child if char else node.left_child
	return rank


########################################################
# Code to run
########################################################
'''
x = "mississippi"
root = WaveletTreeNode(x, 0, None) # x, level, root
print(rank(root, "m", 0))

'''
