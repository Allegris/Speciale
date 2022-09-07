from bitarray import bitarray
from math import log2, floor

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
'''


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


def wavelet_queue(x):
	wt = bitarray()
	q = [x]
	while q:
		xx = q.pop(0)
		triple = construct_wavelet_tree(xx)
		if triple[0]:
			wt += triple[0]
		if triple[1]:
			q += [triple[1], triple[2]]

	alpha = get_alphabet(x)
	last = len(x) * (floor(log2(len(alpha))) + 1)
	return wt[0:last]


def construct_wavelet_tree(x):
	alpha = get_alphabet(x)
	a_size = len(alpha)
	if a_size == 1:
		bv = bitarray(len(x))
		bv.setall(0)
		return bv, None, None
	# Assign binary value to each letter: d = {letter: binary},
	# (split alphabet in half)
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Update codes for letters
	#for letter in alpha:
	#	codes[letter].append(d[letter])
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
	return bin_x, x0, x1


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

#bv = bitarray('0011011011010000111100')
#sub_bv = bv[0:11]
#print(go_left(sub_bv, len(bv), 0, len(sub_bv)))

#x = "mississippialphaaaaaiiiiiiiiiiiiiiipppppppppppppabcdefghijklmnopqrstuvwxyzøæåjkfadnkcdnoeuhritnodhnijsbdakflne"
x = "mississippialpha"
n = len(x)
#wt = bitarray('0011011011010000111100')
#rank(wt, n, "i", 8)


wt = wavelet_queue(x)
print(rank(wt, n, 0, n))


