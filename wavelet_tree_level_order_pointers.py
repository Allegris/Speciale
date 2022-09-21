from bitarray import bitarray
from math import log2, floor, ceil
from shared import get_alphabet, letter_count
from bitarray.util import canonical_huffman#, huffman_code



########################################################
# Construct level order wavelet tree
########################################################


'''
bitarray('0011011011010000111100')

{0: {'left': (11, 16), 'right': (16, 22)},
11: {'left': (None, None), 'right': (None, None)},
16: {'left': (None, None), 'right': (None, None)}}

{
'i': bitarray('00'),
'm': bitarray('01'),
'p': bitarray('10'),
's': bitarray('11')}
'''
def wavelet_tree_and_child_dict_and_codes(x):
	wt = bitarray()
	n = len(x)
	count = letter_count(x)
	codes, _, _ = canonical_huffman(count)
	child_dict = {}
	level = 0
	q = [(level, x, 0, n)]
	correction = 0
	while q:
		level, s, i, j = q.pop(0)
		bin_s, s0, s1, a_size = split_node(s, codes, level)
		if a_size > 1: # if i is an inner node
			wt += bin_s
			child_dict[i] = {"left": (None, None), "right": (None, None)}
		# LEFT CHILD
		if len(get_alphabet(s0)) > 1:
			ii, jj = left_child(bin_s, i-correction, n)
			child_dict[i]["left"] = (ii, jj)
			q.append((level+1, s0, ii, jj))
		else:
			child_dict[i]["left"] = (None, None)
			correction += len(s0)
		# RIGHT CHILD
		if(len(get_alphabet(s1))) > 1:
			ii, jj = right_child(bin_s, i-correction, n)
			child_dict[i]["right"] = (ii, jj)
			q.append((level+1, s1, ii, jj))
		else:
			child_dict[i]["right"] = (None, None)
			correction += len(s1)
	return wt, child_dict, codes



def split_node(s, codes, level):
	alpha = get_alphabet(s)
	a_size = len(alpha)
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
	return bin_s, s0, s1, a_size


########################################################
# Preprocess wavelet tree ranks
########################################################

'''
Preprocesses word ranks of every "node" in the (implicit) wavelet tree.
Returns a dict {idx: {0: [], 1: []}} where the lists contain the word ranks
for 0 and 1, respectively. Idx is the starting index of the "node" in the
bitvector for the entire wavelet tree.
'''
def preprocess_tree_node_ranks(wt, n, child_dict):
	ranks = {idx: {0: [], 1: []} for idx in child_dict.keys()}
	ranks[0] = node_word_ranks(wt[0:n], n) # root ranks
	# iterate nodes
	for lr in child_dict.values():
		L, R = lr["left"]
		if L and R: # if inner node
			ranks[L] = node_word_ranks(wt[L:R], R-L)
		L, R = lr["right"]
		if L and R: # if inner node
			ranks[L] = node_word_ranks(wt[L:R], R-L)
	return ranks


'''
Computes word ranks of a "node" in the (implicit) wavelet tree.
Returns a dict, {0: [], 1: []} where the lists contain the word ranks
for 0 and 1, respectively.
'''
def node_word_ranks(bitvector, length):
	ranks = {0: [], 1: []}
	word_size = max(floor(log2(length)), 1)
	for i in range(length // word_size): # Iterate words
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
Rank query using a wavelet tree in level order format.
'''
def rank_query(wt, n, pointers, ranks, codes, c, i):
	code = codes[c]
	L, R = 0, n
	rank = i # current rank
	for char in code:
		rank = node_rank_query(wt[L:R], ranks[L], char, rank)
		# Update L, R depending on char
		L, R = pointers[L]["right"] if char else pointers[L]["left"]
	return rank


'''
Rank query on a given node in the wavelet tree (as a bitvector).
I.e., look-up in ranks and/or scan.
'''
def node_rank_query(bitvector, ranks, c, i):
	n = len(bitvector)
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


########################################################
# Helper functions
########################################################

'''
Computes the index of the left child of a given "node" in a level order
wavelet tree.
'''
def left_child(sub_bv, n, i):
	return i+n, i+n+sub_bv.count(0)

'''
Computes the index of the right child of a given "node" in a level order
wavelet tree.
'''
def right_child(sub_bv, n, i):
	return i+n+sub_bv.count(0), i+n+sub_bv.count(0)+sub_bv.count(1)


########################################################
# Code to run
########################################################



#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
#x = "mississippialpha"
x = "mississippi"
n = len(x)

wt, pointers, codes = wavelet_tree_and_child_dict_and_codes(x)
#print(wt)
#print(pointers)
#print(codes)
ranks = preprocess_tree_node_ranks(wt, n, pointers)
#print(ranks)
print(rank_query(wt, n, pointers, ranks, codes, "s", 4))






