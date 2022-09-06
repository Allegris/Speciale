from bitarray import bitarray
from math import log2, floor


'''
Keep track of queue of x strings to partition and encode,
and encode them recursively. E.g. for x = "mississippi", the queue would be:
	mississippi    alpha0 = {i, m},  alpha1 = {p, s}
	miii           alpha0 = {i},     alpha1 = {m}
	sssspp         alpha0 = {p},     alpha1 = {s}
	iiii
	m
	pp
	ssss

Returns a level order representation of a wavelet tree of x (i.e., a bitvector),
e.g., bitarray('0011011011010000111100')
'''
def wavelet_queue(x):
	wt = bitarray()
	q = [x]
	while q:
		xx = q.pop(0)
		triple = construct_wavelet_tree(xx)
		if triple:
			wt += triple[0]
			q += [triple[1], triple[2]]
	return wt

def yield_wavelet_queue(x):
	q = [x]
	while q:
		xx = q.pop(0)
		triple = construct_wavelet_tree(xx)
		if triple:
			yield bitarray(triple[0])
			q += [triple[1], triple[2]]


'''
Assigns binary values to all chars of input string x, by splitting the alphabet
of x in half. Then splits x into substrings corresponding to only 0s vs only 1s.
Returns
	bin_x: a bitarray representation of x, e.g., bitarray('00110110110').
	x0: the 0 chars of x, e.g., miiii
	x1: the 1 chars of x, e.g., sssspp
'''
def construct_wavelet_tree(x):
	alpha = get_alphabet(x)
	a_size = len(alpha)
	if a_size == 1:
		return None
	# Assign binary value to each letter: d = {letter: binary},
	# (split alphabet in half)
	d = {letter: 0 for letter in alpha}
	for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
		d[letter] = 1
	# Update codes for letters
	for letter in alpha:
		codes[letter].append(d[letter])
	# Binary representation of x
	bin_x = bitarray()
	# The part of x corresponding to 0s and 1s, respectively
	x0, x1 = "", ""
	for char in x:
		bin_x.append(d[char])
		if d[char] == 0:
			x0 += char
		else:
			x1 += char
	return bin_x, x0, x1


def preprocess_rank_wavelet(wt, n, code, i):
	for node in wt:
		yield(node, preprocess_word_ranks(node, len(node)))



def preprocess_word_ranks(bv, n):
	ranks = {0: [], 1: []}
	word_size = floor(log2(n))
	for i in range(n // word_size):
		#print("word", bv[i*word_size: (i+1)*word_size])
		word = bv[i*word_size: (i+1)*word_size]
		if i == 0:
			ranks[0].append(word.count(0))
			ranks[1].append(word.count(1))
		else:
			ranks[0].append(ranks[0][i-1] + word.count(0))
			ranks[1].append(ranks[1][i-1] + word.count(1))
	return ranks


def rank_bitvector(bv, ranks, n, c, i):
	word_size = floor(log2(n))
	word_no = (i // word_size)
	scan_len = i % word_size
	# If in first word, just scan
	if word_no == 0:
		return bv[0:scan_len].count(c)
	# If we do not need to scan, look-up the rank directly in ranks
	if scan_len == 0:
		return ranks[c][word_no - 1]
	# If we both need to look-up in ranks and scan
	else:
		start = word_no * word_size
		end = start + scan_len
		return ranks[c][word_no - 1] + bv[start:end].count(c)


def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


########## Code to run ##########

x = "mississippi"
n = len(x)
alpha = get_alphabet(x) # ["i", "m", "p", "s"]
#a_size = len(alpha)

# Codes, e.g., {'i': bitarray('00'), 'm': bitarray('01'), 'p': bitarray('10'), 's': bitarray('11')}
global codes
codes = {letter: bitarray() for letter in alpha}
#print(codes)
wt = wavelet_queue(x)
#print(wt)
ranks = preprocess_word_ranks(wt, len(wt))
print(ranks)
r = rank_bitvector(wt, ranks, len(wt), 0, 22)
#print(r)
wt2 = yield_wavelet_queue(x)
#print(list(wt2))
preprocess_rank_wavelet(wt2, n, codes["i"], 8)

#print(list(preprocess_rank_wavelet(wt2, n, codes["i"], 8)))


