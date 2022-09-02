from bitarray import bitarray
from math import log2, floor


'''
Keep track of queue of x strings to partition and encode,
and encode them recursively. E.g. for x = "mississippi", the queue would be:
	mississippi    alpha0 = {i, m},  alpha1 = {p, s}
	miii           alpha0 = {i},     alpha1 = {m}
	sssspp         alpha0 = {p},     alpha1 = {s}
	iiii
	m
	pp
	ssss

Yields the...
'''
def wavelet_rec(x, n, alpha, a_size):
	res = bitarray()
	q = [x]
	while q:
		xx = q.pop(0)
		triple = construct_wavelet_tree(xx)
		if triple:
			res += triple[0]
			q += [triple[1], triple[2]]
	return res

'''
Assigns binary values to all chars of input string x, by splitting the alphabet
of x in half. Then splits x into substrings corresponding to only 0s vs only 1s.
Returns
	bin_x: a bitarray representation of x, e.g., bitarray('00110110110').
	x0: the 0 chars of x, e.g., miiii
	x1: the 1 chars of x, e.g., sssspp
'''
def construct_wavelet_tree(x):
	#print("x", x)
	alpha = get_alphabet(x)
	a_size = len(alpha)
	if a_size == 1:
		return None
	# Assign binary value to each letter: d = {letter: binary},
	# (split alphabet in half)
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
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
	print(bin_x, x0, x1)
	return bin_x, x0, x1


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


########## Code to run ##########

x = "mississippi"
n = len(x)
alpha = get_alphabet(x) # ["i", "m", "p", "s"]
a_size = len(alpha)

print(wavelet_rec(x, n, alpha, a_size))
#print(construct_wavelet_tree(x, n, alpha, a_size))

