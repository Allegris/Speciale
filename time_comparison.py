from random import randrange
from one_hot_encoding import one_hot_encoding, preprocess_ranks


n = 100
title = f"simulated_data\\simulated_DNA_n{n}.txt"
file = open(title, "r")
x = file.read()
file.close()

queries = []

for _ in range(n):
	char_idx = randrange(0, n)
	char = x[char_idx]
	query_idx = randrange(0, n)
	queries.append((char, query_idx))


print(queries)


# One hot encoding
ohe_table = one_hot_encoding(x)
ohe_ranks = preprocess_ranks(ohe_table, len(x))
s = get_size(ohe_table) + get_size(ohe_ranks)
ohe_ls.append(s)
write_to_file("data_ohe.txt", n, s)

for c, i in queries:
