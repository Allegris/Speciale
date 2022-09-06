from bitarray import bitarray
from math import log2, floor

class WaveletTreeNode:
	def __init__(self, x, root):
		#print("Node", x)
		self.x = x
		self.n = len(x)
		self.alpha = self.get_alphabet(x)
		self.bitvector = None
		self.ranks = None
		self.left_child = None
		self.right_child = None

		if root:
			self.root = root
		else: # If node has no root: it IS the root
			self.root = self
			self.codes = {letter: bitarray() for letter in self.alpha}


		# Split alphabet to create children
		bv, left, right, leaf = self.split_node(x)
		if not leaf:
			self.bitvector = bv
			self.left_child = WaveletTreeNode(left, self)
			self.right_child = WaveletTreeNode(right, self)
		else:
			self.left_child = WaveletTreeLeaf(left[0])
			self.right_child = WaveletTreeLeaf(right[0])


	def get_alphabet(self, x):
		letters = ''.join(set(x))
		return sorted(letters)


	def split_node(self, x):
		alpha = self.alpha
		a_size = len(alpha)
		# Assign binary value to each letter: d = {letter: binary},
		# (split alphabet in half)
		d = {letter: 0 for letter in alpha}
		for letter in alpha[a_size // 2:]: # assign last half of alphabet to 1
			d[letter] = 1
		# Update codes for letters
		for letter in alpha:
			self.root.codes[letter].append(d[letter])
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
		# Are the child nodes leaves or not
		child_leaves = False if a_size > 2 else True
		return bin_x, x0, x1, child_leaves



class WaveletTreeLeaf:
	def __init__(self, letter):
		#print("Leaf", letter)
		self.letter = letter


##### Code to run #####
x = "mississippi"
wt = WaveletTreeNode(x, False)
print(wt.left_child.left_child.letter)


