from shared import alphabet_size, bitvector_rank, preprocess_node_word_ranks, split_node, huffman_codes
import sys

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
def rank_query(root, c, i):
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

def size_of_tree(root):
	s = 0
	s += sys.getsizeof(root.codes)
	q = [root]
	while q:
		node = q.pop(0)
		#s += sys.getsizeof(node)
		s += sys.getsizeof(node.bitvector)
		s += sys.getsizeof(node.word_ranks)
		s += sys.getsizeof(node.root)
		s += sys.getsizeof(node.left_child)
		s += sys.getsizeof(node.right_child)
		if node.left_child:
			q.append(node.left_child)
		if node.right_child:
			q.append(node.right_child)
	return s


#x = "mississippialpha"
#x = "mississippi"
x = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
wt_root = WaveletTreeNode(x, 0, None) # x, level, root
#print(wt_root.__dict__)
#print(wt_root.word_ranks)
#print(rank_query(wt_root, "i", 8))


print(size_of_tree(wt_root))



