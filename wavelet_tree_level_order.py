from bitarray import bitarray
from math import log2, floor, ceil


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
def wavelet_tree(x):
	wt = bitarray()
	alpha = get_alphabet(x)
	codes = {letter: bitarray() for letter in alpha}
	q = [x]
	while q:
		xx = q.pop(0)
		triple = split_node(xx, codes)
		codes = triple[3]
		wt += triple[0]
		if triple[1] and triple[2]:
			q += [triple[1], triple[2]]
	last = len(x) * (ceil(log2(len(alpha))))
	return wt[0:last], codes


def split_node(x, codes):
	alpha = get_alphabet(x)
	a_size = len(alpha)
	if a_size == 1:
		bv = bitarray(len(x))
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
	bin_x = bitarray()
	# The part of x corresponding to 0s and 1s, respectively
	x0, x1 = "", ""
	for char in x:
		bin_x.append(d[char])
		if d[char] == 0:
			x0 += char
		else:
			x1 += char
	return bin_x, x0, x1, codes


def go_left(sub_bv, n, i):
	return i+n, i+n+sub_bv.count(0)


def go_right(sub_bv, n, i):
	return i+n+sub_bv.count(0), i+n+sub_bv.count(0)+sub_bv.count(1)


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


def preprocess_node_ranks(wt, n):
	ranks = {}
	wt_len = len(wt)
	q = [(0, n)]
	while q:
		(L, R) = q.pop(0) # interval
		sub_bv = wt[L:R]
		ranks[L] = node_word_ranks(sub_bv, len(sub_bv))
		left_child = go_left(sub_bv, n, L)
		right_child = go_right(sub_bv, n, L)
		if right_child[1] <= wt_len:
			q.append(left_child)
			q.append(right_child)
	return ranks


def node_word_ranks(bitvector, n):
	ranks = {0: [], 1: []}
	word_size = max(floor(log2(n)), 1)
	for i in range(n // word_size): # Iterate words
		word = bitvector[i*word_size: (i+1)*word_size]
		prev_0s = 0 if i == 0 else ranks[0][i-1]
		prev_1s = 0 if i == 0 else ranks[1][i-1]
		ranks[0].append(prev_0s + word.count(0))
		ranks[1].append(prev_1s + word.count(1))
	return ranks


def node_rank(bitvector, ranks, c, i):
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


def rank_query(wt, n, ranks, codes, c, i):
	code = codes[c]
	L, R = 0, n
	ii = i
	for char in code:
		ii = node_rank(wt[L:R], ranks[L], char, ii)
		if char == 0:
			L, R = go_left(wt[L:R], n, L)
		if char == 1:
			L, R = go_right(wt[L:R], n, L)
	return ii



##### Code to run #####
'''
#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
#x = "mississippialpha"
x = "mississippi"
n = len(x)

wt, codes = wavelet_tree(x)
#print(wt)
ranks = preprocess_node_ranks(wt, n)
#print(ranks)
print(rank_query(wt, n, ranks, codes, "i", 0))
'''








