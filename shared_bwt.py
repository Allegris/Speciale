import skew


'''
Constructs the suffix array of x, using the Skew algorithm; time O(n)
'''
def construct_sa_skew(x):
	alpha, indices = skew.map_string_to_ints(x)
	return skew.skew_rec(indices, len(alpha))

'''
Slow, naïve suffix array construction algorithm
'''
def construct_sa_slow(x):
	suffixes = [x[i:] for i in range(len(x))]
	suffixes_sorted = sorted(suffixes)
	sa = [len(x)-len(y) for y in suffixes_sorted]
	return sa


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
Constructs sparse SA as dict {idx: SA_val} for only some of the indices in
normal SA; indices: 0, k, 2k, 3k, etc.
'''
def construct_sparse_sa(sa, k):
	sparse_sa = {}
	for idx, val in enumerate(sa):
		if val % k == 0:
			sparse_sa[idx] = val
	return sparse_sa

'''
Finds the SA value for index i, using the sparse SA.
'''
def lookup_sparse_sa(sparse_sa, i, C, O, l_to_n, bwt_x):
	idx = i
	steps = 0
	while idx not in sparse_sa.keys():
		c = bwt_x[idx]
		a = l_to_n[c]
		idx = C[a] + O[a, idx]
		steps += 1
	return sparse_sa[idx] + steps