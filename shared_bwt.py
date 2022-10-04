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
			#bwt += "$"
			bwt += x[-1]
		else:
			bwt += x[sa[i]-1]
	return bwt

def bwt2(x, sa):
	bwt = x[-1]
	for i in range(len(x)):
		if sa[i] != 0:
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
x = "mississippi"
sa = construct_sa_skew(x)
print(bwt2(x, sa))
'''