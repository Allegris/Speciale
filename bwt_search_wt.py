from wavelet_tree_lvl import rank_query
from shared import get_alphabet, letter_count
#from shared_bwt import construct_sparse_sa, bwt, construct_skew
#import bwt_search_wt as bwt_wt
#import wavelet_tree_lvl as lop
#from shared import huffman_codes
#from shared_bwt import construct_sa_skew, construct_sparse_sa, bwt, bwt2

########################################################
# BWT search with wavelet trees
########################################################

'''
Construct C table as a dict {letter: start_idx_of_letter_block}
'''
def construct_C(x):
	alpha = get_alphabet(x)
	counts = letter_count(x)
	C = {}
	C[alpha[0]] = 0 # first letter has idx 0
	offset = counts[alpha[0]]
	for letter in alpha[1:]:
		C[letter] = offset
		offset += counts[letter]
	return C


'''
Finds the SA value for index i, using the sparse SA.
'''
def lookup_sparse_sa(i, bwt_x, SENTINEL_idx, sparse_sa, C, wt_tuple):
	idx = i
	steps = 0
	while idx not in sparse_sa.keys():
		c = bwt_x[idx]
		idx = update_bwt_idx(idx, SENTINEL_idx, C, c, wt_tuple)
		steps += 1
	return sparse_sa[idx] + steps

'''
Pattern match using wavelet tree of BWT(x)
'''
def bw_search(p, bwt_x, SENTINEL_idx, sparse_sa, C, wt_tuple):
	L, R = 0, len(bwt_x)
	for c in reversed(p):
		if L < R:
			L = update_bwt_idx(L, SENTINEL_idx, C, c, wt_tuple)
			R = update_bwt_idx(R, SENTINEL_idx, C, c, wt_tuple)
		else:
			break
	matches = [lookup_sparse_sa(i, bwt_x, SENTINEL_idx, sparse_sa, C, wt_tuple) for i in range(L, R)]
	#matches = [sa[i] for i in range(L, R)]
	return sorted(matches)


def update_bwt_idx(idx, SENTINEL_idx, C, c, wt_tuple):
	wt, pointers, ranks, codes, n = wt_tuple
	if idx > SENTINEL_idx:
		return C[c] + rank_query(wt, n, pointers, ranks, codes, c, idx-1)
	else:
		return C[c] + rank_query(wt, n, pointers, ranks, codes, c, idx)


########################################################
# Code to run
########################################################
'''

x = "mississippi$"
n = len(x)
sa = construct_sa_skew(x)
sparse_sa = construct_sparse_sa(sa, 4)
bwt_x = bwt(x, sa)

# BW search with wavelet tree rank query (level order wt)
SENTINEL_idx = bwt_x.index("$")
C_dict = bwt_wt.construct_C(x)
x2 = "mississippi"
n2 = len(x2)
sa2 = construct_sa_skew(x2)
bwt_x2 = bwt2(x2, sa2)
codes = huffman_codes(x2)
wt, pointers = lop.wavelet_tree(bwt_x2, codes)
ranks = lop.all_node_ranks(wt, len(bwt_x2), pointers)

p = "ssi"
print(bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx))

'''


'''
x = "AACGTAAACGTAAC"
x += "$"
n = len(x)
sa = construct_sa_skew(x)
p = "AAC"


# BW search with wavelet tree rank query (level order wt)
bwt_x = bwt(x, sa)

offset = construct_offset_dict(x)
wt, codes = lo.wavelet_tree(bwt_x)
ranks = lo.preprocess_node_ranks(wt, len(bwt_x))
print(bw_search(p, n, sa, offset, wt, ranks, codes))

'''




