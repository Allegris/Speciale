import numpy as np
from shared import get_alphabet


########################################################
# BW search with C and O tables
########################################################

'''
Pattern matches for p in x (x: implicitly as sa, n, C, O, and l_to_n)
'''
def bw_search(bwt_x, p, sparse_sa, C, O, l_to_n):
	# Init L and R
	L, R = 0, len(bwt_x)
	# Update L and R
	for c in reversed(p):
		if L < R:
			a = l_to_n[c]
			L = C[a] + O[a, L]
			R = C[a] + O[a, R]
		else:
			break
	# Find and return corresponding match indices
	matches = [lookup_sparse_sa(sparse_sa, i, bwt_x, C, O, l_to_n, ) for i in range(L, R)]
	return sorted(matches)


########################################################
# Helper functions
########################################################

'''
Constructs C table for BW search
'''
def construct_C(x):
	alpha = get_alphabet(x)
	C = [0, 1]
	for i in range(2, len(alpha)):
		C.append(C[i-1] + x.count(alpha[i-1]))
	return C


'''
Constructs O table (Occ) for BW search
'''
def construct_O(x, sa, n_to_l):
	alpha = get_alphabet(x)
	O = np.zeros((len(alpha), len(x)+1), dtype=int)
	for r in range(len(alpha)):
		for c in range(1, len(x)+1):
			a = n_to_l[r]
			O[r, c] = O[r, c-1] + (x[sa[c-1]-1] == a)
	return O


'''
Finds the SA value for index i, using the sparse SA
'''
def lookup_sparse_sa(sparse_sa, i, bwt_x, C, O, l_to_n):
	idx = i
	steps = 0
	while idx not in sparse_sa.keys():
		c = bwt_x[idx]
		a = l_to_n[c]
		idx = C[a] + O[a, idx]
		steps += 1
	return sparse_sa[idx] + steps


'''
COMPACT VERSION FOR REPORT
'''
'''
def lookup_sparse_sa(i, bwt, sparse_sa, C, O):
	idx = i
	steps = 0
	while idx not in sparse_sa:
		c = bwt[idx]
		idx = C[c] + O[c, idx]
		steps += 1
	return sparse_sa[idx] + steps
'''


'''
Returns a mapping between numbers and letter, eg. {0: "0", 1: "A", 2: "C", 3: "G", 4: "T"}, 0 is the sentinel
and a list of the string, eg. for "ACGT" we get [1, 2, 3, 4]
'''
def map_string_to_ints(x):
	letters = ''.join(set(x))
	letters = sorted(letters)
	num = 0
	num_to_letter_dict = {}
	letter_to_num_dict = {}
	for letter in letters:
		num_to_letter_dict[num] = letter
		letter_to_num_dict[letter] = num
		num += 1
	num_ls = []
	for char in x:
		num_ls.append(letter_to_num_dict[char])
	return num_to_letter_dict, letter_to_num_dict, num_ls


########################################################
# Class for rank querying with Occ table
# (only used for space and time experiments, not for pattern matching)
########################################################


class Occ:
	def __init__(self, x):
		self.num_to_letter_dict, self.letter_to_num_dict, _ = map_string_to_ints(x)
		self.table = self.construct_occ(x)

	def construct_occ(self, x):
		alpha = get_alphabet(x)
		occ = np.zeros((len(alpha), len(x)+1), dtype=np.int32)
		for r in range(len(alpha)):
			for c in range(1, len(x)+1):
				letter = self.num_to_letter_dict[r]
				occ[r, c] = occ[r, c-1] + (x[c-1] == letter)
		return occ

	def rank(self, c, i):
		letter = self.letter_to_num_dict[c]
		return self.table[letter][i]

