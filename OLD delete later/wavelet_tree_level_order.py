from bitarray import bitarray
from math import log2, floor, ceil
from shared import get_alphabet, huffman_codes, alphabet_size



########################################################
# Construct level order wavelet tree
########################################################


'''
Returns a wavelet tree, e.g., for mississippi:
(bitarray('
00110110110
10000111100')
'''
def wavelet_tree(x, codes):
	wt = bitarray()
	q = [(x, 0)] # s, level
	while q:
		s, level = q.pop(0)
		bin_s, s0, s1 = split_node(s, level, codes)
		wt += bin_s
		if s0 and s1:
			q.append((s0, level + 1))
			q.append((s1, level + 1))
	# A bit hacky: remove last useless 0s
	#last = len(x) * (ceil(log2(alphabet_size(x))))
	#return wt[0:last]
	return wt

'''
Takes a string, x, and a code dict {letter: code} as input.
Assigns a binary value to every character of x, by splitting the alphabet of x
in half.
Then returns:
	 - The binary representation of x
	 - The substring of x corresponding to 0s
	 - The substring of x corresponding to 1s
	 - An updated code dict
'''
def old_split_node(s, codes):
	alpha = get_alphabet(s)
	a_size = len(alpha)
	if a_size == 1:
		bv = bitarray(len(s))
		bv.setall(0)
		return bv, None, None, codes
	# Assign binary value to each letter: d = {letter: binary},
	# (split alphabet in half)
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Update codes for letters
	for letter in alpha:
		codes[letter].append(d[letter])
	# Binary representation of x
	bin_s = bitarray()
	# The part of x corresponding to 0s and 1s, respectively
	s0, s1 = "", ""
	for char in s:
		bin_s.append(d[char])
		if d[char] == 0:
			s0 += char
		else:
			s1 += char
	return bin_s, s0, s1, codes

def split_node(s, level, codes):
	#print("s:", s)
	alpha = get_alphabet(s)
	# If leaf
	if alphabet_size(s) == 1:
		bv = bitarray(len(s))
		bv.setall(0)
		return bv, None, None
	#for letter in alpha:
	#	print("!", letter, codes[letter], level)
	d = {letter: codes[letter][level] for letter in alpha}
	# Binary representation of x
	bin_s = bitarray()
	# The part of x corresponding to 0s and 1s, respectively
	s0, s1 = "", ""
	for char in s:
		bin_s.append(d[char])
		if d[char] == 0:
			s0 += char
		else:
			s1 += char
	return bin_s, s0, s1

########################################################
# Preprocess wavelet tree ranks
########################################################

'''
Preprocesses word ranks of every "node" in the (implicit) wavelet tree.
Returns a dict {idx: {0: [], 1: []}} where the lists contain the word ranks
for 0 and 1, respectively. Idx is the starting index of the "node" in the
bitvector for the entire wavelet tree.
'''
def preprocess_all_tree_node_ranks(wt, n):
	ranks = {}
	#wt_len = len(wt)
	q = [(0, n)]
	while q:
		(L, R) = q.pop(0) # interval
		sub_bv = wt[L:R]
		ranks[L] = node_word_ranks(sub_bv)
		# Left child
		i, j = left_child(sub_bv, n+L)
		if(alphabet_size(wt[i:j].to01())) > 1: # If inner node
			q.append((i, j))
		# Right child
		i, j = right_child(sub_bv, n+L)
		if(alphabet_size(wt[i:j].to01())) > 1: # If inner node
			q.append((i, j))
	return ranks


'''
Computes word ranks of a "node" in the (implicit) wavelet tree.
Returns a dict, {0: [], 1: []} where the lists contain the word ranks
for 0 and 1, respectively.
'''
def node_word_ranks(bitvector):
	n = len(bitvector)
	ranks = {0: [], 1: []}
	if n == 0: return ranks
	word_size = max(floor(log2(n)), 1)
	#word_size = floor(log2(n)) if floor(log2(n)) < 0 else 1  # BLOWS SPACE USAGE UP???
	for i in range(n // word_size): # Iterate words
		word = bitvector[i*word_size: (i+1)*word_size]
		prev_0s = 0 if i == 0 else ranks[0][i-1]
		prev_1s = 0 if i == 0 else ranks[1][i-1]
		ranks[0].append(prev_0s + word.count(0))
		ranks[1].append(prev_1s + word.count(1))
	return ranks


########################################################
# Rank query using wavelet tree
########################################################


'''
Rank query using a wavelet tree in level order format (a single bitvector).
'''
def rank_query(wt, n, ranks, codes, c, i):
	code = codes[c]
	print("Code", code)
	L, R = 0, n
	rank = i # Current rank
	for char in code:
		print("Code char", char)
		print("L, R", L, R)
		#if L in ranks:
		rank = node_rank_lookup(wt[L:R], ranks[L], char, rank)
		print("Right", right_child(wt[L:R], n+L))
		L, R = right_child(wt[L:R], n+L) if char else left_child(wt[L:R], n+L)

	return rank


'''
Rank query on a given node in the wavelet tree (as a bitvector).
I.e., look-up in ranks and/or scan.
'''
def node_rank_lookup(bitvector, ranks, c, i):
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
def left_child(bv, left_child_idx):
	return left_child_idx, left_child_idx + bv.count(0)


'''
Computes the index of the right child of a given "node" in a level order
wavelet tree.
'''
def right_child(bv, left_child_idx):
	print("left_child_idx", left_child_idx)
	print("bv.count(0)", bv.count(0))
	return left_child_idx + bv.count(0), left_child_idx + len(bv)

########################################################
# Code to run
########################################################


#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
#x = "mississippialpha"
x = "mississippi"
codes = huffman_codes(x)
n = len(x)

wt = wavelet_tree(x, codes)
print(wt)
ranks = preprocess_all_tree_node_ranks(wt, n)
print(ranks)
#print(rank_query(wt, n, ranks, codes, "i", 11))





