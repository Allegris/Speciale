from bitarray import bitarray
from math import log2, floor

class WaveletTreeNode:
	def __init__(self, x, is_root):
		self.n = len(x)
		self.bv = None
		self.ranks = None
		self.leftChild = None
		self.rightChild = None
		self.alpha = get_alphabet(x)
		self.codes = None
		self.label = None
		if is_root: self.codes = {letter: bitarray() for letter in self.alpha}

		triple = self.split(x, is_root)
		if triple:
			#print("isroot", is_root, triple[3])
			self.bv = bitarray(triple[0])
			self.ranks = preprocess_word_ranks(self.bv, self.n)
			self.leftChild = WaveletTreeNode(triple[1], False)
			self.rightChild = WaveletTreeNode(triple[2], False)
			#if(is_root): self.codes = triple[3]
		else:
			self.label = x[0]

	def split(self, x, is_root):
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
		#if is_root:
		for letter in alpha:
			self.codes[letter].append(d[letter])
			print("update codes", letter, d[letter])
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

def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)


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


def node_rank(node, c, i):
	if node.label:
		return "LEAF NODE"
	bv = node.bv
	ranks = node.ranks
	n = node.n
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


def rank_query(root, c, i):
	code = root.codes[c]
	print(root.codes)
	node = root
	ii = i
	for char in code:
		print("char", char)
		print("ii", ii)
		print("node.bv", node.bv)
		ii = node_rank(node, char, ii)
		#node = node.leftChild if code == 0 else node.rightChild
		if char == 0:
			print("go left")
			node = node.leftChild
			print("NODE CODES", node.codes)
		else:
			print("go right")
			node = node.rightChild

	return ii




##### Code to run #####
x = "mississippi"
#n = len(x)
#alpha = get_alphabet(x) # ["i", "m", "p", "s"]
#global codes
#codes = {letter: bitarray() for letter in alpha}

wt = WaveletTreeNode(x, True)
print(wt.ranks)
#codes = wt.codes
#r = node_rank(wt.leftChild, 1, 5)
#print(codes)
#print(codes["i"])
print(rank_query(wt, "m", 11))





