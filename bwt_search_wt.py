from shared import get_alphabet, letter_count

########################################################
# BWT search using wavelet tree
########################################################

'''
Pattern match using wavelet tree of BWT(x)
'''
def bw_search(p, bwt_x, SENTINEL_idx, sparse_sa, C, wt):
	L, R = 0, len(bwt_x)
	for c in reversed(p):
		if L < R:
			L = update_bwt_idx(L, SENTINEL_idx, C, c, wt)
			R = update_bwt_idx(R, SENTINEL_idx, C, c, wt)
		else:
			break
	matches = [lookup_sparse_sa(i, bwt_x, SENTINEL_idx, sparse_sa, C, wt) for i in range(L, R)] #[sa[i] for i in range(L, R)]
	return sorted(matches)


########################################################
# Helper functions
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
def lookup_sparse_sa(i, bwt_x, SENTINEL_idx, sparse_sa, C, wt):
	idx = i
	steps = 0
	while idx not in sparse_sa:
		c = bwt_x[idx]
		idx = update_bwt_idx(idx, SENTINEL_idx, C, c, wt)
		steps += 1
	return sparse_sa[idx] + steps


'''
Uses the FM-mapping to find row idx in the BW matrix corresponding to a
left-rotation of the row at idx
'''
def update_bwt_idx(idx, SENTINEL_idx, C, c, wt):
	if idx > SENTINEL_idx:
		return C[c] + wt.rank(c, idx-1)
	else:
		return C[c] + wt.rank(c, idx)


