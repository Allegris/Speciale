import numpy as np
import skew
import wavelet_tree_level_order as lo

def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


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


def construct_C(x):
	alpha = get_alphabet(x)
	C = [0, 1]
	for i in range(2, len(alpha)):
		C.append(C[i-1] + x.count(alpha[i-1]))
	return C


def construct_O(x, sa, n_to_l):
	alpha = get_alphabet(x)
	O = np.zeros((len(alpha), len(x)+1), dtype=int)
	for r in range(len(alpha)):
		for c in range(1, len(x)+1):
			a = n_to_l[r]
			O[r, c] = O[r, c-1] + (x[sa[c-1]-1] == a)
	return O


def construct_sa_skew(x):
	alpha, indices = skew.map_string_to_ints(x)
	return skew.skew_rec(indices, len(alpha))

def construct_sa_slow(x):
	suffixes = [x[i:] for i in range(len(x))]
	suffixes_sorted = sorted(suffixes)
	sa = [len(x)-len(y) for y in suffixes_sorted]
	return sa



def bw_search(x, sa, p, C, O, l_to_n):
	# Init L and R
	l = 0
	r = len(x)
	# Update L and R
	for i in range(len(p)-1, -1, -1):
		if l < r:
			a = l_to_n[p[i]]
			l = C[a] + O[a, l]
			r = C[a] + O[a, r]
		else:
			break
	# Find and return corresponding match indices
	matches = [sa[i] for i in range(l, r)]
	return sorted(matches)


def bw_seach_rank(x, sa, p, C, l_to_n, wt, ranks, codes):
	n = len(x)
	l = 0
	r = len(x)
	for i in range(len(p)-1, -1, -1):
		if l < r:
			a = l_to_n[p[i]]
			#print(lo.rank_query(wt, n, ranks, codes, p[i], l))
			l = C[a] + lo.rank_query(wt, n, ranks, codes, p[i], l)
			r = C[a] + lo.rank_query(wt, n, ranks, codes, p[i], r)
		else:
			break
	matches = [sa[i] for i in range(l, r)]
	return sorted(matches)


'''

$AACGTAAACGTAAC  0
AAACGTAAC$AACGT  1
AAC$AACGTAAACGT  2
AACGTAAACGTAAC$  3
AACGTAAC$AACGTA  4
AC$AACGTAAACGTA  5
ACGTAAACGTAAC$A  6
ACGTAAC$AACGTAA  7
C$AACGTAAACGTAA  8
CGTAAACGTAAC$AA  9
CGTAAC$AACGTAAA  10
GTAAACGTAAC$AAC  11
GTAAC$AACGTAAAC  12
TAAACGTAAC$AACG  13
TAAC$AACGTAAACG  14

btw(x) = CTT$AAAAAAACCGG

'''



x = "AACGTAAACGTAAC"
x += "$"
n = len(x)
p = "AAC"
sa = construct_sa_skew(x)
#sa = construct_sa_slow(x)
num_to_letter_dict, letter_to_num_dict, num_ls = map_string_to_ints(x)

C = construct_C(x)
O = construct_O(x, sa, num_to_letter_dict)
print(bw_search(x, sa, p, C, O, letter_to_num_dict))


x = "CTT$AAAAAAACCGG"
wt, codes = lo.wavelet_tree(x)
ranks = lo.preprocess_node_ranks(wt, n)
print(bw_seach_rank(x, sa, p, C, letter_to_num_dict, wt, ranks, codes))

#print(lo.rank_query(wt, n, ranks, codes, "A", 3))

#l_to_n = {"$":0, "A":1, "C":2, "G":3, "T":4}
#n_to_l = {0:"$", 1:"A", 2:"C", 3:"G", 4:"T"}
