import bitvectors as bv

x = "mississippi$"
n = len(x)
alpha = ["$", "i", "m", "p", "s"]
a_size = len(alpha)
d = bv.one_hot_encoding(x, n, alpha, a_size)
ranks = bv.preprocess_rank_one_hot(d, n, alpha)


def test_mississippi_m_0():
	assert bv.rank_one_hot(ranks, d, n, "i", 6)






'''
bv, d = one_hot_encoding(x, n, alpha, a_size)
ranks = preprocess_rank_one_hot(bv, d, n, alpha)
print(ranks, "\n")
print(rank_one_hot(ranks, bv, d, n, "p", 9))
'''

d = new_one_hot_encoding(x, n, alpha, a_size)
ranks = new_preprocess_rank_one_hot(d, n, alpha)
print(ranks)
print(d)

print(new_rank_one_hot(ranks, d, n, "i", 6))
