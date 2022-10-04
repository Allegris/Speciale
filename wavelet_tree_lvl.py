from bitarray import bitarray
from shared import alphabet_size, bitvector_rank, preprocess_node_word_ranks, split_node, huffman_codes


########################################################
# Construct level order wavelet tree
########################################################

class wavelet_tree:
	def __init__(self, x):
		self.n = len(x)
		self.codes = huffman_codes(x)
		self.bitvector, self.child_dict = self.wt_bitvector_and_child_dict(x, self.codes)
		self.ranks = self.all_node_ranks(self.bitvector, len(x), self.child_dict)


	'''
	Constructs a level order, Huffman-shaped wavelet tree of string x using
	Huffman encoding in codes.

	Returns the wavelet tree as:
		- A bitvector (representing level order representation).
		- Child dict {parent_idx: {'left': left_child_idx, 'right': right_child_idx}}.
		  Note, if child_idx is (None, None), then the child is a leaf in the tree.

	E.g., for x = "mississippi", it returns:
	bitarray('101101101101000011011')

	{0: {'left': (None, None), 'right': (11, 18)},
	11: {'left': (None, None), 'right': (18, 21)},
	18: {'left': (None, None), 'right': (None, None)}}

	{'i': bitarray('0'),
	 's': bitarray('10'),
	 'm': bitarray('110'),
	 'p': bitarray('111')}

	'''
	def wt_bitvector_and_child_dict(self, x, codes):
		# Implicit tree: bitvector and child dict
		wt_bitvector = bitarray()
		child_dict = {} # {parent_idx: {'left': left_idx, 'right': right_idx}}
		# Queue of inner nodes - s.t. we run through them in level order
		inner_nodes = [(x, 0, 0)] # (string, idx, level)
		# The indices of inner nodes should be corrected for the number
		# of leaf chars that we encounter, so store this
		leaf_chars = 0
		while inner_nodes:
			s, idx, level = inner_nodes.pop(0)
			s_bitvector, s0, s1 = split_node(s, codes, level)
			wt_bitvector += s_bitvector
			child_dict[idx] = {"left": (None, None), "right": (None, None)}
			# If left child is an inner node
			if alphabet_size(s0) > 1:
				i, j = self.left_child(s_bitvector, idx+len(x)-leaf_chars)
				child_dict[idx]["left"] = (i, j)
				inner_nodes.append((s0, i, level+1))
			else: # If left child is a leaf
				leaf_chars += len(s0)
			# If right child is an inner node
			if alphabet_size(s1) > 1:
				i, j = self.right_child(s_bitvector, idx+len(x)-leaf_chars)
				child_dict[idx]["right"] = (i, j)
				inner_nodes.append((s1, i, level+1))
			else: # If right child is a leaf
				leaf_chars += len(s1)
		return wt_bitvector, child_dict


	'''
	Computes the index of the left child of a given "node" in a level order
	wavelet tree.
	'''
	def left_child(self, bv, left_child_idx):
		return left_child_idx, left_child_idx + bv.count(0)


	'''
	Computes the index of the right child of a given "node" in a level order
	wavelet tree.
	'''
	def right_child(self, bv, left_child_idx):
		return left_child_idx + bv.count(0), left_child_idx + len(bv)


	########################################################
	# Preprocess wavelet tree ranks
	########################################################

	'''
	Preprocesses word ranks of every "node" in the (implicit) wavelet tree.
	Returns a dict {idx: {0: [], 1: []}} where the lists contain the word ranks
	for 0 and 1, respectively. Idx is the starting index of the "node" in the
	bitvector for the entire wavelet tree, wt.
	'''
	def all_node_ranks(self, wt, n, child_dict):
		ranks = {idx: {0: [0], 1: [0]} for idx in child_dict.keys()}
		ranks[0] = preprocess_node_word_ranks(wt[0:n]) # Root ranks
		# Iterate over nodes
		for children in child_dict.values():
			for path in ["left", "right"]:
				i, j = children[path]
				if i and j: # If inner node, calculate word ranks
					ranks[i] = preprocess_node_word_ranks(wt[i:j])
		return ranks

	########################################################
	# Rank query using wavelet tree
	########################################################

	'''
	Rank query using a wavelet tree in level order.
	'''
	def rank(self, c, i):
		# Current node, (L, R), and rank
		L, R = 0, self.n
		rank = i
		# Iterate chars in code
		for char in self.codes[c]:
			# Update rank and node
			rank = bitvector_rank(self.bitvector[L:R], self.ranks[L][char], char, rank)
			L, R = self.child_dict[L]["right"] if char else self.child_dict[L]["left"]
		return rank


########################################################
# Code to run
########################################################

'''
#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
#x = "mississippialpha"
#x = "mississippi"
x = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
wt = wavelet_tree(x)

print(wt.rank("A", 0))
'''



