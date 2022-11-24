from random import randrange
from one_hot_encoding import OneHotEncoding
import wavelet_tree as w1
import wavelet_tree_lvl as w2
from bwt_search import Occ
from shared import construct_sa_skew, bwt


n = 100
title = f"simulated_data\\simulated_DNA_n{n}.txt"
file = open(title, "r")
x = file.read()
file.close()

x += "0"
sa = construct_sa_skew(x)
bwt_x = bwt(x, sa)

queries = []

for _ in range(n):
	char_idx = randrange(0, n)
	char = x[char_idx]
	query_idx = randrange(0, n)
	queries.append((char, query_idx))



# One hot encoding
ohe = OneHotEncoding(bwt_x)

# WT
wt1 = w1.WaveletTree(bwt_x)

# WT level
wt2 = w2.WaveletTree(bwt_x)

# Occ
occ = Occ(x, sa)

for c, i in queries:
	print(ohe.rank(c, i), wt1.rank(c, i), wt2.rank(c, i), occ.rank(c, i))
