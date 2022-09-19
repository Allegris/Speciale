from bitarray import bitarray
from math import log2, floor, ceil
from shared import get_alphabet



########################################################
# Construct level order wavelet tree
########################################################


'''
Returns a wavelet tree and letter codes, e.g., for mississippi:
(bitarray('
00110110110
10000111100'),



{'i': bitarray('00'),
 'm': bitarray('01'),
 'p': bitarray('10'),
 's': bitarray('11')})

'''
def wavelet_tree_and_pointers_and_codes(x):
	wt = bitarray()
	n = len(x)
	pointer_dict = {}
	alpha = get_alphabet(x)
	codes = {letter: bitarray() for letter in alpha}
	q = [(x, (0, n))]
	correction = 0
	while q:
		s, (i, j) = q.pop(0)
		bin_x, x0, x1, a_size, codes = split_node(s, codes)
		if a_size > 1:
			wt += bin_x
			pointer_dict[i] = {"left": (None, None), "right": (None, None)}
		if a_size == 3:
			start = left_child(bin_x, i, n)[0]
			right = right_child(bin_x, i, n)
			diff = right[1] - right[0]
			#pointer_dict[i]["left"] = None #x0[0]
			pointer_dict[i]["right"] = (start, start+diff)
			q += [(x1, (start, start+diff))]
			correction += len(x0)
		if a_size >= 4:
			left = left_child(bin_x, i-correction, n)
			right = right_child(bin_x, i-correction, n)
			pointer_dict[i] = {}
			pointer_dict[i]["left"] = left
			pointer_dict[i]["right"] = right
			q += [(x0, left), (x1, right)]

	return wt, pointer_dict, codes


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
def split_node(x, codes):
	alpha = get_alphabet(x)
	a_size = len(alpha)
	# Assign binary value to each letter: d = {letter: binary},
	# (split alphabet in half)
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Update codes for letters
	for letter in alpha:
		codes[letter].append(d[letter])
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
	return bin_x, x0, x1, a_size, codes


########################################################
# Preprocess wavelet tree ranks
########################################################

'''
Preprocesses word ranks of every "node" in the (implicit) wavelet tree.
Returns a dict {idx: {0: [], 1: []}} where the lists contain the word ranks
for 0 and 1, respectively. Idx is the starting index of the "node" in the
bitvector for the entire wavelet tree.
'''
def old_preprocess_tree_node_ranks(wt, n, pointers):
	ranks = {}
	wt_len = len(wt)
	q = [(0, n)]
	while q:
		(L, R) = q.pop(0) # interval
		sub_bv = wt[L:R]
		ranks[L] = node_word_ranks(sub_bv, len(sub_bv))
		left = pointers[L]["left"] #left_child(sub_bv, n, L)
		right = pointers[L]["right"] #right_child(sub_bv, n, L)
		if right[1] <= wt_len:
			q.append(left)
			q.append(right)
	return ranks

def preprocess_tree_node_ranks(wt, n, pointers):
	ranks = {idx: {0: [], 1: []} for idx in pointers.keys()}
	ranks[0] = node_word_ranks(wt[0:n], len(wt[0:n]))
	for idx, lr in pointers.items():
		if lr["left"]:
			L, R = lr["left"]
			ranks[L] = node_word_ranks(wt[L:R], len(wt[L:R]))
		if lr["right"]:
			L, R = lr["right"]
			ranks[L] = node_word_ranks(wt[L:R], len(wt[L:R]))
	return ranks


'''
Computes word ranks of a "node" in the (implicit) wavelet tree.
Returns a dict, {0: [], 1: []} where the lists contain the word ranks
for 0 and 1, respectively.
'''
def node_word_ranks(bitvector, n):
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
Rank query using a wavelet tree in level order format.
'''
def rank_query(wt, n, pointers, ranks, codes, c, i):
	code = codes[c]
	L, R = 0, n
	ii = i
	for char in code:
		ii = node_rank_query(wt[L:R], ranks[L], char, ii)
		if char == 0:
			L, R = pointers[L]["left"] #left_child(wt[L:R], n, L)
		if char == 1:
			L, R = pointers[L]["right"] #right_child(wt[L:R], n, L)
	return ii


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
x = "mississippialpha"
n = len(x)

wt, pointers, codes = wavelet_tree_and_pointers_and_codes(x)
#print("pointer dict:\n", pointers)
#print(wt)
ranks = preprocess_tree_node_ranks(wt, n, pointers)
#print(ranks)
print(rank_query(wt, n, pointers, ranks, codes, "i", 15))









