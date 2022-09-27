from bitarray import bitarray
from shared import alphabet_size, bitvector_rank, preprocess_node_word_ranks, split_node


########################################################
# Construct level order wavelet tree
########################################################

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
def wavelet_tree(x, codes):
	wt = bitarray()
	child_dict = {}
	# Queue of inner nodes - s.t. we run through them in level order
	q = [(x, 0, 0)] # (string, idx, level)
	# The indices of inner nodes should be corrected for the number
	# of leaf chars that we encounter, so store this
	leaf_chars = 0
	while q:
		s, idx, level = q.pop(0)
		bin_s, s0, s1 = split_node(s, codes, level)
		if alphabet_size(s) > 1: # If s is an inner node
			wt += bin_s
			child_dict[idx] = {"left": (None, None), "right": (None, None)}
		# Left Child
		if alphabet_size(s0) > 1: # If left child is an inner node
			i, j = left_child(bin_s, idx+len(x)-leaf_chars)
			child_dict[idx]["left"] = (i, j)
			q.append((s0, i, level+1))
		else: # If left child is a leaf
			leaf_chars += len(s0)
		# Right child
		if alphabet_size(s1) > 1:  # If right child is an inner node
			i, j = right_child(bin_s, idx+len(x)-leaf_chars)
			child_dict[idx]["right"] = (i, j)
			q.append((s1, i, level+1))
		else: # If right child is a leaf
			leaf_chars += len(s1)
	return wt, child_dict


'''
Computes the index of the left child of a given "node" in a level order
wavelet tree.
'''
def left_child(bv, left_child_idx):
	return left_child_idx, left_child_idx + bv.count(0)


'''
Computes the index of the right child of a given "node" in a level order
wavelet tree.
'''
def right_child(bv, left_child_idx):
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
def preprocess_all_tree_node_ranks(wt, n, child_dict):
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
def rank_query(wt, n, child_dict, ranks, codes, c, i):
	code = codes[c]
	L, R = 0, n
	rank = i # Current rank
	for char in code:
		rank = bitvector_rank(wt[L:R], ranks[L][char], char, rank)
		# Update L, R depending on char
		L, R = child_dict[L]["right"] if char else child_dict[L]["left"]
	return rank


########################################################
# Code to run
########################################################

'''
#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
#x = "mississippialpha"
x = "mississippi"
codes = huffman_codes(x)
wt, child_dict = wavelet_tree(x, codes)
ranks = preprocess_all_tree_node_ranks(wt, len(x), child_dict)

#print(wt)
#print(child_dict)
#print(codes)
#print(ranks)

print(rank_query(wt, len(x), child_dict, ranks, codes, "s", 4))
'''




