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

Yields the
'''
def wavelet_rec(x, n, alpha, a_size):
	q = [x]
	while q:
		xx = q.pop(0)
		triple = construct_wavelet_tree(xx)
		if triple:
			yield triple[0]
			q += [triple[1], triple[2]]


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
	bin_x = bitarray(0) # empty
	# The part of x corresponding to 0s and 1s, respectively
	x0, x1 = "", ""
	for char in x:
		bin_x.append(d[char])
		if d[char] == 0:
			x0 += char
		else:
			x1 += char
	return bin_x, x0, x1


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

