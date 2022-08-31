from bitarray import bitarray
from math import log2, floor


def new_one_hot_encoding(x, n, alpha, a_size):
	# Initiate dict {letter: bitarray} of all zeros
	# e.g., {'$': bitarray('000000000000'), 'i': bitarray('000000000000'), ...}
	d = {char: bitarray(n) for char in alpha}
	for bv in d.values():
		bv.setall(0)
	# Set bits corresponding to chars in x
	# e.g. {'$': bitarray('000000000001'), 'i': bitarray('010010010010'), ...}
	for i, char in enumerate(x):
		d[char][i] = 1
	return d

def new_preprocess_rank_one_hot(d, n, alpha):
	ranks = {char: [] for char in alpha}
	word_size = floor(log2(n))
	no_of_words = n // word_size
	for char in d.keys():
		for i in range(no_of_words):
			count = d[char][i*word_size : (i+1)*word_size].count(1)
			if i == 0:
				ranks[char].append(count)
			else:
				ranks[char].append(ranks[char][i-1] + count)
	return ranks


def new_rank_one_hot(ranks, d, n, c, i):
	if i == 0: return 0

	word_size = floor(log2(n))
	word_no = (i // word_size)
	scan_len = i % word_size

	if word_no == 0:
		print("case C")
		#print(scan_len)
		return d[c][0:scan_len].count(1)
	if scan_len == 0:
		print("case A")
		return ranks[c][word_no - 1]
	else:
		print("case B")
		start = word_no * word_size
		print("start", start)
		end = start + scan_len
		print("end", end)
		return ranks[c][word_no - 1] + d[c][start:end].count(1)





########## Code to run ##########

x = "mississippi$"
n = len(x)
alpha = ["$", "i", "m", "p", "s"]
a_size = len(alpha)


d = new_one_hot_encoding(x, n, alpha, a_size)
ranks = new_preprocess_rank_one_hot(d, n, alpha)
print(ranks)
print(d)

print(new_rank_one_hot(ranks, d, n, "i", 6))




