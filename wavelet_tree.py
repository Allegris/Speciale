from bitarray import bitarray
from math import log2, floor


def construct_wavelet_tree(x, n, alpha, a_size):
	# Partition alphabet in two halves
	# d = {letter: binary} where binary is the binary value assigned to letter
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Binary representation of x
	bin_x = bitarray(0) # empty
	for char in x:
		bin_x.append(d[char])
	print(bin_x)




def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


########## Code to run ##########

x = "mississippi"
n = len(x)
alpha = get_alphabet(x) # ["i", "m", "p", "s"]
a_size = len(alpha)


construct_wavelet_tree(x, n, alpha, a_size)

