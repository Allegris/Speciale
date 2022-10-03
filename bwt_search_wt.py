from wavelet_tree_lvl import rank_query
from shared import get_alphabet, letter_count
#from shared_bwt import construct_sparse_sa, bwt, construct_skew


########################################################
# BWT search with wavelet trees
########################################################

'''
Construct C table as a dict {letter: start_idx_of_letter_block}
'''
def construct_C_dict(x):
	alpha = get_alphabet(x)
	counts = letter_count(x)
	letter_offsets = {}
	letter_offsets[alpha[0]] = 0
	offset = counts[alpha[0]]
	for letter in alpha[1:]:
		letter_offsets[letter] = offset
		offset += counts[letter]
	return letter_offsets


'''
Finds the SA value for index i, using the sparse SA.
'''
def lookup_sparse_sa(sparse_sa, i, bwt_x, C, wt, n, pointers, ranks, codes):
	idx = i
	steps = 0
	while idx not in sparse_sa.keys():
		c = bwt_x[idx]
		idx = C[c] + rank_query(wt, n, pointers, ranks, codes, c, idx)
		steps += 1
	return sparse_sa[idx] + steps


'''
Pattern match using wavelet tree of BWT(x)
'''
def bw_search(bwt_x, p, n, sparse_sa, C, wt, pointers, ranks, codes):
	L, R = 0, n # keeping n as arg, because SA will be changed to sparse, so cannot use n = len(sa)
	for c in reversed(p):
		if L < R:
			L = C[c] + rank_query(wt, n, pointers, ranks, codes, c, L)
			R = C[c] + rank_query(wt, n, pointers, ranks, codes, c, R)
		else:
			break
	matches = [lookup_sparse_sa(sparse_sa, i, bwt_x, C, wt, n, pointers, ranks, codes) for i in range(L, R)]
	return sorted(matches)


########################################################
# Code to run
########################################################

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




