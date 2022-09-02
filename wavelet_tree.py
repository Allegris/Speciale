from bitarray import bitarray
from math import log2, floor



def wavelet_rec(x, n, alpha, a_size):
	q = [x]
	while q:
		xx = q.pop(0)
		triple = construct_wavelet_tree(xx)
		if triple:
			yield triple[0]
			q += [triple[1], triple[2]]


def construct_wavelet_tree(x):
	print("x", x)
	alpha = get_alphabet(x)
	a_size = len(alpha)
	if a_size == 1:
		return None #(bitarray(0), "", "")
	# Partition alphabet in two halves
	# d = {letter: binary} where binary is the binary value assigned to letter
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Binary representation of x
	bin_x = bitarray(0) # empty
	x0, x1 = "", ""
	for char in x:
		bin_x.append(d[char])
		if d[char] == 0:
			x0 += char
		else:
			x1 += char
	return bin_x, x0, x1

def partition_string(x, alpha, a_size):
	alpha_0, alpha_1 = alpha[:a_size // 2], alpha[a_size // 2:]


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


########## Code to run ##########

x = "mississippi"
n = len(x)
alpha = get_alphabet(x) # ["i", "m", "p", "s"]
a_size = len(alpha)

print(list(wavelet_rec(x, n, alpha, a_size)))
#print(construct_wavelet_tree(x, n, alpha, a_size))

