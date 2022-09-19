import skew
import wavelet_tree_level_order as lo
import wavelet_tree_level_order_pointers as lop
from shared import get_alphabet
import tracemalloc


########################################################
# BWT search with wavelet trees
########################################################


'''
Construct BWT(x) using SA
'''
def bwt(x, sa):
	bwt = ""
	for i in range(len(x)):
		if sa[i] == 0:
			bwt += "$"
		else:
			bwt += x[sa[i]-1]
	return bwt


'''
Construct C table as a dict {letter: start_idx_of_letter_block}
'''
def construct_C_dict(x):
	alpha = get_alphabet(x)
	# Map between letters and ints
	letter_to_int = {}
	int_to_letter = {}
	for i in range(len(alpha)):
		letter_to_int[alpha[i]] = i
		int_to_letter[i] = alpha[i]
	# Count chars in x
	counts = [0] * len(alpha)
	for char in x:
		counts[letter_to_int[char]] += 1
	# Cumulated counts
	cum_counts = [0] * len(alpha)
	val = 0
	for i in range(len(counts)):
		cum_counts[i] = val
		val += counts[i]
	# Put cumulated counts into dict: {letter: start_idx_of_letter_block}
	d = {letter: 0 for letter in alpha}
	for i, val in enumerate(cum_counts):
		d[int_to_letter[i]] = val
	return d


'''
Pattern match using wavelet tree of BWT(x)
'''
def bw_search(p, n, sa, C, wt, ranks, codes):
	L, R = 0, n # keeping n as arg, because SA will be changed to sparse, so cannot use n = len(sa)
	for c in reversed(p):
		if L < R:
			L = C[c] + lo.rank_query(wt, n, ranks, codes, c, L)
			R = C[c] + lo.rank_query(wt, n, ranks, codes, c, R)
		else:
			break
	matches = [sa[i] for i in range(L, R)]
	return sorted(matches)


'''
Pattern match using wavelet tree of BWT(x)
'''
def bw_search2(p, n, sa, C, wt, pointers, ranks, codes):
	L, R = 0, n # keeping n as arg, because SA will be changed to sparse, so cannot use n = len(sa)
	for c in reversed(p):
		if L < R:
			L = C[c] + lop.rank_query(wt, n, pointers, ranks, codes, c, L)
			R = C[c] + lop.rank_query(wt, n, pointers, ranks, codes, c, R)
		else:
			break
	matches = [sa[i] for i in range(L, R)]
	return sorted(matches)

########################################################
# Helper functions
########################################################

'''
Constructs the suffix array of x, using the Skew algorithm; time O(n)
'''
def construct_sa_skew(x):
	alpha, indices = skew.map_string_to_ints(x)
	return skew.skew_rec(indices, len(alpha))


########################################################
# Code to run
########################################################

'''
tracemalloc.start()
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

print(tracemalloc.get_traced_memory()[1])
tracemalloc.stop()
'''




