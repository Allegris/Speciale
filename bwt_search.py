import numpy as np
from shared import get_alphabet
from shared_bwt import lookup_sparse_sa#, bwt, construct_sa_skew, construct_sparse_sa

########################################################
# BW search with C and O tables
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
Constructs O table for BW search
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
Pattern natch for p in x (x: implicitly as sa, n, C, O, and l_to_n)
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
	#matches = [sa[i] for i in range(L, R)]
	matches = [lookup_sparse_sa(sparse_sa, i, C, O, l_to_n, bwt_x) for i in range(L, R)]
	return sorted(matches)


########################################################
# Helper functions
########################################################

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
# Code to run
########################################################

'''
x = "mississippi"
x += "$"
sa = construct_sa_skew(x)
bwt_x = bwt(x, sa)
num_to_letter_dict, letter_to_num_dict, num_ls = map_string_to_ints(x)
C = construct_C(x)
O = construct_O(x, sa, num_to_letter_dict)
sparse_sa = construct_sparse_sa(sa, 4)
print(sa)
print(sparse_sa)
print(lookup_sparse_sa(sparse_sa, 12, C, O, letter_to_num_dict, bwt_x))
'''


'''
x = "AACGTAAACGTAAC"
x += "$"
p = "AAC"

sa = construct_sa_skew(x)
num_to_letter_dict, letter_to_num_dict, num_ls = map_string_to_ints(x)


# BW search with Occ table
C = construct_C(x)
O = construct_O(x, sa, num_to_letter_dict)
print(bw_search(p, sa, C, O, letter_to_num_dict))
'''


###########################################################


'''
# Lorem ipsum test
x = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sit amet justo donec enim diam vulputate. Id eu nisl nunc mi ipsum. Eget est lorem ipsum dolor sit amet consectetur adipiscing. Nisl pretium fusce id velit ut tortor pretium viverra. Felis eget velit aliquet sagittis id. Orci porta non pulvinar neque laoreet. Nulla pellentesque dignissim enim sit amet. Dui sapien eget mi proin sed libero. Arcu ac tortor dignissim convallis aenean et tortor at. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Consectetur adipiscing elit duis tristique sollicitudin nibh sit amet. Laoreet suspendisse interdum consectetur libero. Dictum at tempor commodo ullamcorper a lacus. Integer feugiat scelerisque varius morbi enim nunc faucibus a pellentesque. Auctor augue mauris augue neque gravida in fermentum et sollicitudin. Tortor id aliquet lectus proin. Adipiscing enim eu turpis egestas pretium aenean pharetra magna. Tristique nulla aliquet enim tortor at auctor."
x += "$"
x = x.replace(" ", "_")
p = "dolor"
n = len(x)
'''


'''
# BWT example:
x: AACGTAAACGTAAC

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
