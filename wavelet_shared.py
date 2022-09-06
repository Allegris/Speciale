from bitarray import bitarray
from math import log2, floor

def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)




def split_node(self, x):
	alpha = get_alphabet(x)
	a_size = len(alpha)
	if a_size == 1:
		print("NO SPLIT", x[0], x[0])
		return False, x[0], x[0]
	# Assign binary value to each letter: d = {letter: binary},
	# (split alphabet in half)
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Update codes for letters
	for letter in alpha:
		self.root.codes[letter].append(d[letter])
		#print("update codes", letter, d[letter])
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
	print("SPLIT", bin_x, x0, x1)
	return bin_x, x0, x1