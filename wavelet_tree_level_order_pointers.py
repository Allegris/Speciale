from bitarray import bitarray
from math import log2, floor, ceil
from shared import get_alphabet, letter_count, alphabet_size, huffman_codes




########################################################
# Construct level order wavelet tree
########################################################


'''
Constructs a level order, Huffman-shaped wavelet tree of string x.
Returns the wavelet tree as:
	- A bitvector (representing level order representation).
	- Child dict {parent_idx: {'left': left_child_idx, 'right': right_child_idx}}.
	  Note, if child_idx is (Nonen None), then the child is a leaf in the tree.
    - The Huffman codes of the letters

E.g., for x="mississippi", it returns:
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
	# Queue of inner nodes - so we run through them in level order
	q = [(x, 0, 0)] # string, idx, level
	# The indices of inner nodes should be corrected for the number
	# of leaf chars that we encounter
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
			q.append((s0, i, level + 1))
		else: # If left child is a leaf
			child_dict[idx]["left"] = (None, None)
			leaf_chars += len(s0)
		# Right child
		if alphabet_size(s1) > 1:  # If right child is an inner node
			i, j = right_child(bin_s, idx+len(x)-leaf_chars)
			child_dict[idx]["right"] = (i, j)
			q.append((s1, i, level + 1))
		else: # If right child is a leaf
			child_dict[idx]["right"] = (None, None)
			leaf_chars += len(s1)
	return wt, child_dict


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
def split_node(s, codes, level):
	alpha = get_alphabet(s)
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
bitvector for the entire wavelet tree.
'''
def preprocess_all_tree_node_ranks(wt, n, child_dict):
	ranks = {idx: {0: [], 1: []} for idx in child_dict.keys()}
	ranks[0] = node_word_ranks(wt[0:n]) # Root ranks
	# Iterate through nodes
	for children in child_dict.values():
		for path in ["left", "right"]:
			i, j = children[path]
			if i and j: # If inner node, calculate word ranks
				ranks[i] = node_word_ranks(wt[i:j])
	return ranks


'''
Computes word ranks of a "node" in the (implicit) wavelet tree.
Returns a dict, {0: [], 1: []} where the lists contain the word ranks
for 0 and 1, respectively.
'''
def node_word_ranks(bitvector):
	ranks = {0: [], 1: []}
	word_size = max(floor(log2(len(bitvector))), 1)
	for i in range(len(bitvector) // word_size): # Iterate words
		word = bitvector[i*word_size: (i+1)*word_size]
		# Zeros
		prev_0s = 0 if i == 0 else ranks[0][i-1]
		ranks[0].append(prev_0s + word.count(0))
		# Ones
		prev_1s = 0 if i == 0 else ranks[1][i-1]
		ranks[1].append(prev_1s + word.count(1))
	return ranks


########################################################
# Rank query using wavelet tree
########################################################


'''
Rank query using a wavelet tree in level order.
'''
def rank_query(wt, n, pointers, ranks, codes, c, i):
	code = codes[c]
	L, R = 0, n
	rank = i # Current rank
	for char in code:
		rank = node_rank_lookup(wt[L:R], ranks[L], char, rank)
		# Update L, R depending on char
		L, R = pointers[L]["right"] if char else pointers[L]["left"]
	return rank


'''
Rank query on a given node in the wavelet tree (as a bitvector).
I.e., look-up in ranks and/or scan.
'''
def node_rank_lookup(bitvector, ranks, c, i):
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
# Code to run
########################################################



#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
#x = "mississippialpha"
x = "mississippi"
codes = huffman_codes(x)
n = len(x)

wt, child_dict = wavelet_tree(x, codes)
print(wt)
print(child_dict)
print(codes)
ranks = preprocess_all_tree_node_ranks(wt, n, child_dict)
#print(ranks)
print(rank_query(wt, n, child_dict, ranks, codes, "s", 4))






