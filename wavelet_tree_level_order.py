from bitarray import bitarray
from math import log2, floor, ceil

'''
mississippi
bitarray('00110110110')
bitarray('10000')
bitarray('111100')

mississippi
00110110110
10000111100


mississippialpha
bitarray('1011011011001100')
bitarray('1111010')
bitarray('11110')
bitarray('011111101')
bitarray('10')
bitarray('1111000')

mississippialpha
1011011011001100
1111010011111101
0011110101111000


bitarray('
00110110110001000000000000000000000111111111111100000000000000111111111111111000000000010101010100000100000000
11111011000001111111111111110000000111111111000110010111011110001011000000000000000000000000000011111111000000
00000000011111010111010111000010000000000000000000111101111001010011111110000000000000000000111101110100001111
00000001101100011100000101111011111111111111101110101110001101011100111111111111111110110000000011101000110110
00000000001100100100101000000000000000000000000001100110100010011111100000000000000000000111110101011001010110
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')


00110110110001000000000000000000000111111111111100000000000000111111111111111000000000010101010100000100000000
11111011000001111111111111110000000111111111000110010111011110001011000000000000000000000000000011111111000000
00000000011111010111010111000010000000000000000000111101111001010011111110000000000000000000111101110100001111
00000001101100011100000101111011111111111111101110101110001101011100111111111111111110110000000011101000110110
00000000001100100100101000000000000000000000000001100110100010011111100000000000000000000111110101011001010110
mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne


sub_bv bitarray('1011011011001100')
{0: [1, 3, 5, 7], 1: [3, 5, 7, 9]}

sub_bv bitarray('1111010')
{0: [0, 2, 2, 2], 1: [4, 5, 5, 5]}

sub_bv bitarray('011111101')
{0: [1, 2, 2, 2], 1: [3, 6, 7, 7]}

sub_bv bitarray('00')
{0: [2, 2, 2, 2], 1: [0, 0, 0, 0]}

sub_bv bitarray('11110')
{0: [0, 1, 1, 1], 1: [4, 4, 4, 4]}

sub_bv bitarray('10')
{0: [1, 1, 1, 1], 1: [1, 1, 1, 1]}

sub_bv bitarray('1111000')
{0: [0, 3, 3, 3], 1: [4, 4, 4, 4]}

'''

##############################################################################################################


def node_ranks(bitvector, n):
	ranks = {0: [], 1: []}
	word_size = floor(log2(n))
	for i in range(n // word_size): # Iterate words
		word = bitvector[i*word_size: (i+1)*word_size]
		prev_0s = 0 if i == 0 else ranks[0][i-1]
		prev_1s = 0 if i == 0 else ranks[1][i-1]
		ranks[0].append(prev_0s + word.count(0))
		ranks[1].append(prev_1s + word.count(1))
	return ranks


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


def rank(wt, n, c, i):
	root = wt[0:n]
	print(root)
	print(go_left(root, n, 0))
	print(go_right(root, n, 0))
	print(go_left(wt[23:32], n, 23))
	print(go_right(wt[23:32], n, 23))


def go_left(sub_bv, n, i):
	return i+n, i+n+sub_bv.count(0)


def go_right(sub_bv, n, i):
	return i+n+sub_bv.count(0), i+n+sub_bv.count(0)+sub_bv.count(1)


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


def preprocess_node_ranks(wt, n):
	wt_len = len(wt)
	q = [(0, n)]
	while q:
		(L, R) = q.pop(0) # interval
		sub_bv = wt[L:R]
		print("sub_bv", sub_bv)
		print(node_ranks(sub_bv, n))
		yield node_ranks(sub_bv, n)
		left_child = go_left(sub_bv, n, L)
		right_child = go_right(sub_bv, n, L)
		if right_child[1] <= wt_len:
			q.append(left_child)
			q.append(right_child)


def rank_query(root, c, i):
	code = root.codes[c] # code of c, e.g., "00" (left, left) for i in mississippi
	node = root
	ii = i
	for char in code:
		ii = node.node_rank(node.bitvector, node.ranks, node.n, char, ii)
		node = node.left_child if char == 0 else node.right_child
	return ii

def rank_query():


##### Code to run #####

#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
x = "mississippialpha"
#x = "mississippi"
n = len(x)

wt, codes = wavelet_tree(x)
print(wt)
#preprocess_node_ranks(bitvector, n)
#rank(wt, n, 0, n)


#print(go_left(bitarray("1111010"), 16, 16))

#print(go_left(bitarray("00"), 16, 32))

print(list(traverse_wavelet_tree(wt, n)))

