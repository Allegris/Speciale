from shared import alphabet_size, bitvector_rank, split_node, huffman_codes, preprocess_one_ranks
#from line_profiler import LineProfiler

########################################################
# Class for wavelet tree
########################################################

class WaveletTree:
	def __init__(self, x):
		self.codes = huffman_codes(x)
		self.root = WaveletTreeNode(x, 0, self.codes)

	'''
	Rank query for a given char c and a given index i.
	'''
	def rank(self, c, i):
		# Current node and rank
		node = self.root
		rank = i
		# Iterate chars in code
		for bit in self.codes[c]:
			# Update rank and node
			rank = bitvector_rank(node.bitvector,
						 node.word_ranks, bit, rank)
			node = node.right_child if bit else node.left_child
		return rank



########################################################
# Class for wavelet tree internal nodes
########################################################

class WaveletTreeNode:
	def __init__(self, s, level, codes):
		# Construct node bitvector and split s in two parts (child nodes)
		self.bitvector, s0, s1 = split_node(s, codes, level)
		# Preprocess ranks
		self.word_ranks = preprocess_one_ranks(self.bitvector)
		# Create children
		self.left_child, self.right_child = None, None
		# If left child is an inner node
		if alphabet_size(s0) > 1:
			self.left_child = WaveletTreeNode(s0, level+1, codes)
		# If right child is an inner node
		if alphabet_size(s1) > 1:
			self.right_child = WaveletTreeNode(s1, level+1, codes)




########################################################
# Code to run
########################################################

'''
x = "AG$TAAC"
wt = WaveletTree(x)
#print(wt.rank("A", 2))
'''


'''
title = f"simulated_data\\simulated_DNA_n5000000.txt"
file = open(title, "r")
x = file.read()
file.close()

wt = WaveletTree(x)
lp = LineProfiler()
lp_wrapper = lp(wt.rank)
lp_wrapper("A", 990000)
lp.print_stats()
'''

########################################################
# For report
########################################################
'''
# For report (simplified version)
def rank(root, codes, c, i):
	# Current node and rank
	node = root
	rank = i
	# Iterate chars in code
	for char in codes[c]:
		# Update rank and go to child node
		rank = bv_rank(node.bitvector, char, rank)
		node = node.right_child if char else node.left_child
	return rank
'''


















